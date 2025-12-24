"""
Race Engine - Manages the race simulation with all 20 cars
"""
import random
from race.track import Track
from race.car import Car
from data.teams import TEAMS_DATA
import config
from settings.runtime_config import runtime_config

class RaceEngine:
    """Manages the entire race simulation"""

    def __init__(self, waypoints=None):
        self.track = Track(waypoints=waypoints)
        self.cars = []
        self.race_started = False
        self.race_time = 0.0
        self.total_laps = runtime_config.race_laps  # Use runtime config
        
        # Simulation speed control
        self.simulation_speed = runtime_config.simulation_speed

        # Initialize cars
        self._initialize_cars()

    def _initialize_cars(self):
        """Create all 20 cars from team data with full performance stats."""
        position = 1

        # Build entries with full team data
        all_entries = []
        for team_data in TEAMS_DATA:
            team_info = {
                "name": team_data["name"],
                "tier": team_data.get("tier", "B"),
                "characteristics": team_data.get("characteristics", {
                    "balance": 0,
                    "cornering": 0,
                    "traction": 3,
                }),
            }
            for driver in team_data["drivers"]:
                all_entries.append({
                    "driver": driver,
                    "team": team_info,
                })

        # Shuffle for random grid
        random.shuffle(all_entries)

        # Create cars with full data - F1 Grid Formation
        for entry in all_entries:
            car = Car(entry["driver"], entry["team"], position)
            
            # F1 Grid Formation: 2-wide rows with proper spacing
            # Row number (0-9 for 20 cars, 2 cars per row)
            row = (position - 1) // 2
            
            # Progress stagger: ~0.015 per row = ~1.2 seconds gap between rows
            car.progress = -0.015 * row
            
            # Lateral offset: odd positions left (pole side), even positions right
            if position % 2 == 1:
                car.lateral_offset = -10  # Left/inside (pole side)
            else:
                car.lateral_offset = 10   # Right/outside
                car.progress -= 0.005     # Slightly behind (staggered grid)
            
            self.cars.append(car)
            position += 1

    def set_simulation_speed(self, speed):
        """Set simulation speed multiplier"""
        if speed in config.SIMULATION_SPEED_OPTIONS:
            self.simulation_speed = speed

    def cycle_speed(self):
        """Cycle to next speed option"""
        options = config.SIMULATION_SPEED_OPTIONS
        current_idx = options.index(self.simulation_speed) if self.simulation_speed in options else 0
        next_idx = (current_idx + 1) % len(options)
        self.simulation_speed = options[next_idx]

    def update(self):
        """Update all cars and race state"""
        # Apply simulation speed to delta time
        dt = self.simulation_speed
        
        # Update each car with race context
        for car in self.cars:
            car.update(self.track, dt=dt, total_race_laps=self.total_laps)

        # Sort cars by race position (total progress)
        self.cars.sort(key=lambda c: c.get_total_progress(), reverse=True)

        # Update positions and gaps
        leader = self.cars[0]
        leader_progress = leader.get_total_progress()

        # Calculate seconds_per_lap from ACTUAL lap data (not theoretical)
        # This accounts for all speed modifiers (tier, skill, fuel, etc.)
        if leader.last_lap_time and leader.last_lap_time > 0:
            # Use leader's actual completed lap time
            seconds_per_lap = leader.last_lap_time
        elif leader.lap_time > 0 and leader.progress > 0.1:
            # Estimate from current lap progress (at least 10% into lap)
            seconds_per_lap = leader.lap_time / leader.progress
        else:
            # Fallback to theoretical only at very start of race
            speed_prog_per_sec = (config.BASE_SPEED / self.track.track_length) * config.FPS
            seconds_per_lap = 1.0 / speed_prog_per_sec if speed_prog_per_sec > 0 else 4.0

        for i, car in enumerate(self.cars):
            # Update position
            car.position = i + 1

            # Calculate gaps (in progress units)
            car.gap_to_leader = leader_progress - car.get_total_progress()

            if i > 0:
                ahead = self.cars[i - 1]
                car.gap_to_ahead = ahead.get_total_progress() - car.get_total_progress()
            else:
                car.gap_to_ahead = 0.0

            # Convert progress gaps to time gaps
            car.gap_to_leader_time = car.gap_to_leader * seconds_per_lap
            car.gap_to_ahead_time = car.gap_to_ahead * seconds_per_lap

            # Set lateral offset for cars close together
            if i > 0:
                ahead = self.cars[i - 1]
                progress_diff = abs(ahead.progress - car.progress)

                # If cars are very close on same lap, offset them visually
                if ahead.lap == car.lap and progress_diff < 0.05:
                    car.lateral_offset = 15 if i % 2 == 0 else -15
                else:
                    car.lateral_offset = 0
            else:
                car.lateral_offset = 0

        # Update race time (scaled by simulation speed)
        self.race_time += self.simulation_speed / config.FPS

    def get_cars_by_position(self):
        """Get cars sorted by current position"""
        return self.cars

    def get_leader(self):
        """Get the race leader"""
        return self.cars[0] if self.cars else None

    def is_race_finished(self):
        """Check if the race is finished"""
        leader = self.get_leader()
        return leader and leader.lap > self.total_laps

    def get_race_status(self):
        """Get current race status string"""
        if not self.race_started:
            return "READY"
        elif self.is_race_finished():
            return "FINISHED"
        else:
            leader = self.get_leader()
            return f"LAP {leader.lap}/{self.total_laps}"

    def start_race(self):
        """Start the race"""
        self.race_started = True
