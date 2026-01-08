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


class EventManager:
    """Manages race events with history limit and retrieval methods."""

    def __init__(self, max_events=50):
        """
        Initialize the event manager.

        Args:
            max_events: Maximum number of events to store (default: 50)
        """
        self.max_events = max_events
        self.events = []

    def add_event(self, event):
        """
        Add a new event to the manager.

        Args:
            event: RaceEvent instance to add

        The event is added to the front of the list (newest first).
        If max_events is exceeded, oldest events are removed.
        """
        # Add event to front (newest first)
        self.events.insert(0, event)

        # Trim to max size if needed
        if len(self.events) > self.max_events:
            self.events = self.events[:self.max_events]

    def get_recent_events(self, count=None):
        """
        Get the most recent events.

        Args:
            count: Number of events to return (default: all events)

        Returns:
            list: List of RaceEvent instances, sorted newest first
        """
        if count is None:
            return self.events[:]
        return self.events[:count]

    def clear_events(self):
        """Clear all stored events."""
        self.events = []

    def __len__(self):
        """Return number of stored events."""
        return len(self.events)

    def __repr__(self):
        """String representation for debugging."""
        return f"EventManager({len(self.events)} events, max={self.max_events})"
