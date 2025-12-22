"""
F1 Car - Individual car with movement and state
"""
import random
import config

class Car:
    """Represents a single F1 car in the race"""

    def __init__(self, driver_data, team_name, starting_position):
        self.driver_number = driver_data["number"]
        self.driver_name = driver_data["name"]
        self.driver_short = driver_data["short"]
        self.team = team_name

        # Race state
        self.position = starting_position  # Grid position (1-20)
        self.starting_position = starting_position
        self.progress = 0.0  # Progress around track (0.0 to 1.0)
        self.lap = 1
        self.total_laps = 0

        # Performance
        base_speed = config.BASE_SPEED
        # Add some variation (faster cars at front, slower at back)
        speed_modifier = 1.0 + (random.random() * config.SPEED_VARIANCE - config.SPEED_VARIANCE / 2)
        # Slight advantage to better starting positions
        position_modifier = 1.0 - (starting_position - 1) * 0.01
        self.speed = base_speed * speed_modifier * position_modifier

        # Tire state
        self.tire_compound = self._choose_starting_tire(starting_position)
        self.tire_age = 0

        # Timing
        self.lap_time = 0.0
        self.best_lap_time = None
        self.last_lap_time = None
        self.gap_to_leader = 0.0
        self.gap_to_ahead = 0.0

        # Visual
        self.lateral_offset = 0  # For positioning multiple cars on same progress

    def _choose_starting_tire(self, position):
        """Choose starting tire based on grid position"""
        # Top 10 start on softs, rest can choose
        if position <= 10:
            return config.TIRE_SOFT
        else:
            return random.choice([config.TIRE_MEDIUM, config.TIRE_SOFT])

    def update(self, track, dt=1.0):
        """
        Update car position
        dt: delta time (frames)
        """
        # Move car forward
        speed_per_frame = self.speed / track.track_length
        self.progress += speed_per_frame * dt

        # Handle lap completion
        if self.progress >= 1.0:
            self.progress -= 1.0
            self.lap += 1
            self.total_laps += 1
            self.tire_age += 1

            # Record lap time
            if self.last_lap_time is not None:
                if self.best_lap_time is None or self.last_lap_time < self.best_lap_time:
                    self.best_lap_time = self.last_lap_time

            self.last_lap_time = self.lap_time
            self.lap_time = 0.0

        # Increment lap time
        self.lap_time += dt / config.FPS

        # Tire degradation (slight speed loss over time)
        if self.tire_age > 5:
            degradation = (self.tire_age - 5) * 0.002
            self.speed = max(self.speed * (1 - degradation), config.BASE_SPEED * 0.8)

    def get_position_on_track(self, track):
        """Get x, y coordinates on track"""
        return track.get_offset_position(self.progress, self.lateral_offset)

    def get_total_progress(self):
        """Get total progress including laps"""
        return self.lap - 1 + self.progress

    def __repr__(self):
        return f"Car({self.driver_short}, P{self.position}, Lap {self.lap})"
