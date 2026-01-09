"""
Race Engine - Manages the race simulation with all 20 cars
"""
import random
from race.track import Track
from race.car import Car
from data.teams import TEAMS_DATA
from race.race_events import EventManager, RaceEvent, EventType
import config
from settings.runtime_config import runtime_config

class RaceEngine:
    """Manages the entire race simulation"""

    def __init__(self, waypoints=None, decorations=None):
        self.track = Track(waypoints=waypoints, decorations=decorations)
        self.cars = []
        self.race_started = False
        self.race_time = 0.0
        self.total_laps = runtime_config.race_laps  # Use runtime config

        # Simulation speed control
        self.simulation_speed = runtime_config.simulation_speed

        # Event management
        self.event_manager = EventManager()
        self.fastest_lap_time = None
        self.fastest_lap_driver = None
        self.race_end_event_generated = False

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

        # Detect race events
        self._detect_events()

        # Update previous positions for next frame's overtake detection
        for car in self.cars:
            car.previous_position = car.position

        # Update race time (scaled by simulation speed)
        self.race_time += self.simulation_speed / config.FPS

    def _detect_events(self):
        """Detect and record race events like overtakes, pit stops, and fastest laps."""
        leader = self.get_leader()
        if not leader:
            return

        current_lap = leader.lap

        # Detect overtakes - check cars that moved up in position
        for car in self.cars:
            if car.position_changed():
                # Car changed position - check if it's an overtake (moved up)
                if car.position < car.previous_position:
                    # Find who was overtaken (currently directly behind)
                    if car.position < len(self.cars):
                        overtaken_car = self.cars[car.position]  # Car that's now behind

                        # Create overtake event
                        message = f"{car.driver_short} overtakes {overtaken_car.driver_short}"
                        event = RaceEvent(
                            event_type=EventType.OVERTAKE,
                            lap=current_lap,
                            timestamp=self.race_time,
                            drivers=[car.driver_name, overtaken_car.driver_name],
                            message=message
                        )
                        self.event_manager.add_event(event)

        # Detect pit stops - check cars entering or exiting pits
        for car in self.cars:
            # Pit stop start: car just started pitting this frame
            # We detect this when is_pitting is True and pit_time_remaining is close to the full pit time
            if car.is_pitting and car.pit_time_remaining > (runtime_config.pit_stop_base_time - 0.1):
                message = f"{car.driver_short} enters the pits"
                event = RaceEvent(
                    event_type=EventType.PIT_STOP,
                    lap=current_lap,
                    timestamp=self.race_time,
                    drivers=[car.driver_name],
                    message=message
                )
                self.event_manager.add_event(event)

            # Pit stop end: car just completed pit stop (tire_age == 0 and not pitting)
            # This happens right after _complete_pit_stop() is called
            elif not car.is_pitting and car.tire_age == 0 and car.pit_stops > 0:
                # Check if this is a fresh exit (within first few frames of new tires)
                if car.progress < 0.05:  # Near start of lap
                    message = f"{car.driver_short} exits the pits on {car.tire_compound}s"
                    event = RaceEvent(
                        event_type=EventType.PIT_STOP,
                        lap=current_lap,
                        timestamp=self.race_time,
                        drivers=[car.driver_name],
                        message=message
                    )
                    self.event_manager.add_event(event)

        # Detect fastest laps - check cars that just completed a lap
        for car in self.cars:
            if car.last_lap_time and car.last_lap_time > 0:
                # Check if this is a new overall fastest lap
                if self.fastest_lap_time is None or car.last_lap_time < self.fastest_lap_time:
                    # Only create event if lap time has changed (not on initialization)
                    if self.fastest_lap_time is not None:
                        self.fastest_lap_time = car.last_lap_time
                        self.fastest_lap_driver = car.driver_name

                        # Format lap time as MM:SS.mmm
                        minutes = int(car.last_lap_time // 60)
                        seconds = car.last_lap_time % 60
                        time_str = f"{minutes}:{seconds:06.3f}"

                        message = f"{car.driver_short} sets fastest lap: {time_str}"
                        event = RaceEvent(
                            event_type=EventType.FASTEST_LAP,
                            lap=current_lap,
                            timestamp=self.race_time,
                            drivers=[car.driver_name],
                            message=message
                        )
                        self.event_manager.add_event(event)
                    else:
                        # First lap completed, just record it without event
                        self.fastest_lap_time = car.last_lap_time
                        self.fastest_lap_driver = car.driver_name

        # Detect race end - generate event when leader crosses the finish line
        if not self.race_end_event_generated and self.is_race_finished():
            winner = self.cars[0]

            # Calculate margin to second place
            if len(self.cars) > 1:
                second_place = self.cars[1]
                margin = second_place.gap_to_leader_time
            else:
                margin = 0.0

            # Find notable position changes (top 3 biggest gainers)
            position_changes = []
            for car in self.cars:
                change = car.starting_position - car.position
                if change > 0:  # Only gainers
                    position_changes.append((car, change))

            # Sort by biggest gains and take top 3
            position_changes.sort(key=lambda x: x[1], reverse=True)
            notable_changes = position_changes[:3] if position_changes else []

            # Build message with winner, margin, and notable changes
            message = f"{winner.driver_short} wins"
            if margin > 0:
                message += f" by {margin:.1f}s"

            # Add notable position changes to message
            notable_drivers = []
            if notable_changes:
                for car, change in notable_changes:
                    notable_drivers.append(f"{car.driver_short} (+{change})")

            # Create race end event
            event = RaceEvent(
                event_type=EventType.RACE_END,
                lap=current_lap,
                timestamp=self.race_time,
                drivers=[winner.driver_name],
                message=message
            )
            # Store notable changes as additional data in the message for commentary
            if notable_drivers:
                event.notable_changes = notable_drivers

            self.event_manager.add_event(event)
            self.race_end_event_generated = True

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

        # Generate RACE_START event
        leader = self.get_leader()
        if leader:
            message = f"Lights out and away we go!"
            event = RaceEvent(
                event_type=EventType.RACE_START,
                lap=1,
                timestamp=0.0,
                drivers=[],
                message=message
            )
            self.event_manager.add_event(event)
