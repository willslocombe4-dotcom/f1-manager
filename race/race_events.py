"""
Race Events - Track key race moments for commentary and highlights
"""
from enum import Enum


class EventType(Enum):
    """Enum representing different types of race events."""
    OVERTAKE = "overtake"
    PIT_STOP = "pit_stop"
    FASTEST_LAP = "fastest_lap"
    RACE_START = "race_start"
    RACE_END = "race_end"
    BLUE_FLAG = "blue_flag"


class RaceEvent:
    """Represents a single race event with all relevant information."""

    def __init__(self, event_type, lap, timestamp, drivers, message):
        """
        Initialize a race event.

        Args:
            event_type: EventType enum value
            lap: Current lap number when event occurred
            timestamp: Race time in seconds when event occurred
            drivers: List of driver names involved in the event
            message: Human-readable description of the event
        """
        self.event_type = event_type
        self.lap = lap
        self.timestamp = timestamp
        self.drivers = drivers if isinstance(drivers, list) else [drivers]
        self.message = message

    def __repr__(self):
        """String representation for debugging."""
        drivers_str = ", ".join(self.drivers)
        return f"RaceEvent({self.event_type.value}, Lap {self.lap}, [{drivers_str}]: {self.message})"
