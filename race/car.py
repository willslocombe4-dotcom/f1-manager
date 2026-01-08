"""
F1 Car - Individual car with dynamic pace calculation
Phase 1: Foundation - Fuel, Tires, Synergy, Pit Stops
"""
import random
import config
from settings.runtime_config import runtime_config


class Car:
    """Represents a single F1 car in the race with dynamic performance."""

    def __init__(self, driver_data, team_data, starting_position):
        """
        Initialize a car with driver and team data.
        
        Args:
            driver_data: Dict with driver info (number, name, short, skill, etc.)
            team_data: Dict with team info (name, tier, characteristics)
            starting_position: Grid position (1-20)
        """
        # Driver info
        self.driver_number = driver_data["number"]
        self.driver_name = driver_data["name"]
        self.driver_short = driver_data["short"]
        self.driver_skill = driver_data.get("skill", 80)
        self.driver_consistency = driver_data.get("consistency", 3)
        self.driver_racecraft = driver_data.get("racecraft", 3)
        self.driver_style = driver_data.get("style", "adaptive")
        self.is_rookie = driver_data.get("rookie", False)
        
        # Team info
        self.team = team_data["name"]
        self.team_tier = team_data.get("tier", "B")
        self.car_balance = team_data.get("characteristics", {}).get("balance", 0)
        self.car_cornering = team_data.get("characteristics", {}).get("cornering", 0)
        self.car_traction = team_data.get("characteristics", {}).get("traction", 3)

        # Race state
        self.position = starting_position
        self.starting_position = starting_position
        self.progress = 0.0
        self.lap = 1
        self.total_laps = 0
        self.race_finished = False

        # Fuel state (1.0 = full, 0.0 = empty)
        self.fuel_load = 1.0
        
        # Tire state
        self.tire_compound = self._choose_starting_tire(starting_position)
        self.tire_age = 0
        self.pit_stops = 0
        self.is_pitting = False
        self.pit_time_remaining = 0.0

        # Synergy (calculated once at init)
        self.synergy_level = self._calculate_synergy()

        # Track characteristics (updated during race)
        self.track_tire_deg_multiplier = 1.0  # Default multiplier for custom tracks

        # DRS (Drag Reduction System)
        self.is_drs_available = False  # True if within 1 second of car ahead
        self.is_drs_active = False     # True if DRS available AND in DRS zone

        # Dynamic speed (recalculated each frame)
        self.current_pace = config.BASE_SPEED

        # Timing
        self.lap_time = 0.0
        self.best_lap_time = None
        self.last_lap_time = None
        self.gap_to_leader = 0.0
        self.gap_to_ahead = 0.0
        self.gap_to_leader_time = 0.0
        self.gap_to_ahead_time = 0.0

        # Visual
        self.lateral_offset = 0

        # Smooth display position (for rendering)
        self.display_x = None  # Initialized on first render
        self.display_y = None
        self.current_lap_variance = 1.0  # Variance calculated once per lap

    def _choose_starting_tire(self, position):
        """Choose starting tire based on grid position."""
        # Top 10 start on softs, rest can choose
        if position <= 10:
            return config.TIRE_SOFT
        else:
            return random.choice([config.TIRE_MEDIUM, config.TIRE_SOFT])

    def _calculate_synergy(self):
        """
        Calculate driver-car synergy based on style and car characteristics.
        
        Returns:
            str: 'high', 'neutral', or 'low'
        """
        # Get style preferences from config
        style_prefs = config.STYLE_PREFERENCES.get(
            self.driver_style, 
            {"traction": 3, "balance": 0}
        )
        
        # Calculate match score
        # Traction match: how close car traction is to driver preference
        traction_diff = abs(self.car_traction - style_prefs["traction"])
        
        # Balance match: how close car balance is to driver preference
        balance_diff = abs(self.car_balance - style_prefs["balance"])
        
        # Total mismatch score (lower is better)
        mismatch = traction_diff + balance_diff
        
        # Determine synergy level
        if mismatch <= 1:
            return "high"
        elif mismatch <= 3:
            return "neutral"
        else:
            return "low"

    def _calculate_current_pace(self):
        """
        Calculate current pace based on all performance factors.
        
        Formula:
            PACE = BASE × TIER × SKILL × SYNERGY × FUEL × TIRE × VARIANCE
        
        Returns:
            float: Current pace (speed per frame)
        """
        # 1. Base pace from config
        pace = config.BASE_SPEED
        
        # 2. Team tier modifier (+4% to -5%)
        tier_mod = runtime_config.tier_modifiers.get(self.team_tier, 1.0)
        pace *= tier_mod
        
        # 3. Driver skill (70-99 → normalized to 0.85-1.00 range)
        # This ensures skill matters but doesn't dominate
        skill_range = config.SKILL_MAX - config.SKILL_MIN
        skill_factor = config.SKILL_MIN_FACTOR + (self.driver_skill - config.SKILL_MIN) * (config.SKILL_FACTOR_RANGE / skill_range)
        pace *= skill_factor
        
        # 4. Synergy modifier
        synergy_mod = runtime_config.synergy_modifiers.get(self.synergy_level, 1.0)
        pace *= synergy_mod
        
        # 5. Fuel load penalty (full tank = -4%, empty = 0%)
        fuel_penalty = self.fuel_load * runtime_config.fuel_start_penalty
        pace *= (1.0 - fuel_penalty)
        
        # 6. Tire degradation (with track-specific multiplier)
        deg_rate = runtime_config.tire_deg_rates.get(self.tire_compound, 0.002)
        # Apply track characteristics: circuits like Suzuka (1.4x) wear tires faster than Monaco (0.7x)
        tire_penalty = self.tire_age * deg_rate * self.track_tire_deg_multiplier

        # Check for tire cliff
        cliff_lap = runtime_config.tire_cliff_laps.get(self.tire_compound, 20)
        if self.tire_age >= cliff_lap:
            tire_penalty += runtime_config.tire_cliff_penalty

        # Cap tire penalty at maximum
        pace *= (1.0 - min(tire_penalty, runtime_config.max_tire_penalty))

        # 7. Lap-to-lap variance (calculated once per lap in update())
        pace *= self.current_lap_variance

        # 8. DRS boost (if available and in DRS zone)
        if self.is_drs_active:
            pace *= (1.0 + config.DRS_SPEED_BOOST)

        return pace

    def should_pit(self, total_race_laps):
        """
        Determine if car should pit based on tire age and race progress.
        
        Args:
            total_race_laps: Total laps in the race
            
        Returns:
            bool: True if car should pit
        """
        # Don't pit if already pitting
        if self.is_pitting:
            return False
        
        # Don't pit on first lap or last few laps
        if self.lap <= 1 or self.lap >= total_race_laps - runtime_config.last_laps_no_pit:
            return False
        
        # Check if past tire cliff
        cliff_lap = runtime_config.tire_cliff_laps.get(self.tire_compound, 20)
        
        # Pit if at or past cliff, with some randomness
        if self.tire_age >= cliff_lap:
            return random.random() < runtime_config.pit_chance_after_cliff
        
        # Pit if very close to cliff (within window) with lower probability
        if self.tire_age >= cliff_lap - runtime_config.pit_window_laps:
            return random.random() < runtime_config.pit_chance_near_cliff
        
        return False

    def start_pit_stop(self):
        """Initiate a pit stop."""
        self.is_pitting = True
        
        # Calculate pit stop time with variance
        base_time = runtime_config.pit_stop_base_time
        variance = (random.random() * 2 - 1) * runtime_config.pit_stop_variance
        self.pit_time_remaining = base_time + variance
        
        self.pit_stops += 1

    def _complete_pit_stop(self):
        """Complete pit stop: reset tires and state."""
        self.is_pitting = False
        self.pit_time_remaining = 0.0
        
        # Choose new tire compound (simple strategy)
        if self.tire_compound == config.TIRE_SOFT:
            # Soft → Medium or Hard
            self.tire_compound = random.choice([config.TIRE_MEDIUM, config.TIRE_HARD])
        elif self.tire_compound == config.TIRE_MEDIUM:
            # Medium → Hard or Soft
            self.tire_compound = random.choice([config.TIRE_HARD, config.TIRE_SOFT])
        else:
            # Hard → Medium or Soft
            self.tire_compound = random.choice([config.TIRE_MEDIUM, config.TIRE_SOFT])
        
        # Reset tire age
        self.tire_age = 0

    def update(self, track, dt=1.0, total_race_laps=20):
        """
        Update car position with dynamic pace calculation.

        Args:
            track: Track object for position calculation
            dt: Delta time in frames
            total_race_laps: Total laps in the race (for pit strategy)
        """
        # Get track-specific tire degradation multiplier
        # This allows circuits to have different tire wear characteristics
        # (e.g., Suzuka 1.4x harder on tires than Monaco 0.7x)
        self.track_tire_deg_multiplier = track.get_tire_degradation_multiplier()

        # DRS Detection and Activation
        # DRS is available if within 1 second of car ahead (from previous frame)
        # and is active if available AND currently in a DRS zone
        self.is_drs_available = (
            self.position > 1 and  # Not the leader
            self.lap > 1 and  # Not on first lap (DRS enabled from lap 2)
            self.gap_to_ahead_time <= config.DRS_DETECTION_TIME
        )
        self.is_drs_active = (
            self.is_drs_available and
            track.is_in_drs_zone(self.progress)
        )

        # Handle pit stop timing
        if self.is_pitting:
            self.pit_time_remaining -= dt / config.FPS
            if self.pit_time_remaining <= 0:
                self._complete_pit_stop()

        # Calculate current pace (dynamic each frame)
        self.current_pace = self._calculate_current_pace()
        
        # Apply pit stop penalty (reduced speed while "pitting")
        effective_pace = self.current_pace
        if self.is_pitting:
            effective_pace *= runtime_config.pit_speed_penalty  # Slow down during pit
        
        # Move car forward
        speed_per_frame = effective_pace / track.track_length
        self.progress += speed_per_frame * dt

        # Handle lap completion
        if self.progress >= 1.0:
            self.progress -= 1.0
            self.lap += 1
            self.total_laps += 1
            self.tire_age += 1
            
            # Burn fuel (linear over race distance)
            fuel_burn = 1.0 / total_race_laps
            self.fuel_load = max(0.0, self.fuel_load - fuel_burn)

            # Calculate new lap variance for next lap
            variance_factor = runtime_config.lap_variance_base * (6 - self.driver_consistency) / 5
            self.current_lap_variance = 1.0 + (random.random() * 2 - 1) * variance_factor

            # Record lap time
            if self.last_lap_time is not None:
                if self.best_lap_time is None or self.last_lap_time < self.best_lap_time:
                    self.best_lap_time = self.last_lap_time

            self.last_lap_time = self.lap_time
            self.lap_time = 0.0
            
            # Check if should pit (at start of new lap)
            if self.should_pit(total_race_laps):
                self.start_pit_stop()

        # Increment lap time
        self.lap_time += dt / config.FPS

    def get_position_on_track(self, track):
        """Get x, y coordinates on track."""
        return track.get_offset_position(self.progress, self.lateral_offset)

    def get_display_position(self, track):
        """Get smoothed x, y coordinates for rendering."""
        # Get actual position
        target_x, target_y = track.get_offset_position(self.progress, self.lateral_offset)
        
        # Initialize display position on first call
        if self.display_x is None:
            self.display_x = target_x
            self.display_y = target_y
            return target_x, target_y
        
        # Lerp toward target position
        self.display_x += (target_x - self.display_x) * config.CAR_SMOOTHING
        self.display_y += (target_y - self.display_y) * config.CAR_SMOOTHING
        
        return self.display_x, self.display_y

    def get_total_progress(self):
        """Get total progress including laps."""
        return self.lap - 1 + self.progress

    def get_status(self):
        """
        Get current car status for display.
        
        Returns:
            str: Status indicator ('PIT', 'OUT', or '')
        """
        if self.is_pitting:
            return "PIT"
        elif self.pit_stops > 0 and self.tire_age <= 2:
            return "OUT"  # Just exited pits
        return ""

    def __repr__(self):
        return f"Car({self.driver_short}, P{self.position}, Lap {self.lap}, {self.team_tier}-tier)"
