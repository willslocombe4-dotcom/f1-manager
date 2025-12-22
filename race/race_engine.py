"""
Race Engine - Manages the race simulation with all 20 cars
"""
import random
from race.track import Track
from race.car import Car
from data.teams import TEAMS_DATA
import config

class RaceEngine:
    """Manages the entire race simulation"""

    def __init__(self):
        self.track = Track()
        self.cars = []
        self.race_started = False
        self.race_time = 0.0
        self.total_laps = 20  # Sprint race

        # Initialize cars
        self._initialize_cars()

    def _initialize_cars(self):
        """Create all 20 cars from team data"""
        position = 1

        # Randomize starting grid
        all_entries = []
        for team_data in TEAMS_DATA:
            for driver in team_data["drivers"]:
                all_entries.append({
                    "driver": driver,
                    "team": team_data["name"]
                })

        # Shuffle for random grid
        random.shuffle(all_entries)

        # Create cars
        for entry in all_entries:
            car = Car(entry["driver"], entry["team"], position)
            # Set initial progress based on grid position
            # Cars start slightly staggered
            car.progress = -0.001 * (position - 1)
            self.cars.append(car)
            position += 1

    def update(self):
        """Update all cars and race state"""
        # Update each car
        for car in self.cars:
            car.update(self.track)

        # Sort cars by race position (total progress)
        self.cars.sort(key=lambda c: c.get_total_progress(), reverse=True)

        # Update positions and gaps
        leader = self.cars[0]
        leader_progress = leader.get_total_progress()

        for i, car in enumerate(self.cars):
            # Update position
            car.position = i + 1

            # Calculate gaps
            car.gap_to_leader = leader_progress - car.get_total_progress()

            if i > 0:
                ahead = self.cars[i - 1]
                car.gap_to_ahead = ahead.get_total_progress() - car.get_total_progress()
            else:
                car.gap_to_ahead = 0.0

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

        # Update race time
        self.race_time += 1.0 / config.FPS

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
