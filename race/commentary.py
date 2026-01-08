"""
Race Commentary - Generate broadcast-style F1 commentary for race events
"""
from race.race_events import EventType


class CommentaryGenerator:
    """Generates F1 broadcast-style commentary for race events."""

    def __init__(self):
        """Initialize the commentary generator."""
        pass

    def generate_commentary(self, event):
        """
        Generate broadcast-style commentary for a race event.

        Args:
            event: RaceEvent instance with event_type, lap, timestamp, drivers, and message

        Returns:
            str: Formatted commentary text with F1 terminology
        """
        # Route to appropriate commentary generator based on event type
        if event.event_type == EventType.RACE_START:
            return self._generate_race_start_commentary(event)
        elif event.event_type == EventType.OVERTAKE:
            return self._generate_overtake_commentary(event)
        elif event.event_type == EventType.PIT_STOP:
            return self._generate_pit_stop_commentary(event)
        elif event.event_type == EventType.FASTEST_LAP:
            return self._generate_fastest_lap_commentary(event)
        elif event.event_type == EventType.RACE_END:
            return self._generate_race_end_commentary(event)
        elif event.event_type == EventType.BLUE_FLAG:
            return self._generate_blue_flag_commentary(event)
        else:
            # Fallback to basic message
            return event.message

    def _generate_race_start_commentary(self, event):
        """
        Generate commentary for race start event.

        Args:
            event: RaceEvent with RACE_START type

        Returns:
            str: Formatted race start commentary
        """
        # Use the iconic F1 race start phrase
        return "Lights out and away we go!"

    def _generate_overtake_commentary(self, event):
        """
        Generate commentary for overtake event.

        Args:
            event: RaceEvent with OVERTAKE type and two drivers

        Returns:
            str: Formatted overtake commentary
        """
        if len(event.drivers) >= 2:
            overtaker = event.drivers[0]
            overtaken = event.drivers[1]
            return f"{overtaker} makes a move on {overtaken}!"
        else:
            # Fallback if driver data is missing
            return "Overtake!"

    def _generate_pit_stop_commentary(self, event):
        """
        Generate commentary for pit stop event.

        Args:
            event: RaceEvent with PIT_STOP type

        Returns:
            str: Formatted pit stop commentary
        """
        if len(event.drivers) >= 1:
            driver = event.drivers[0]

            # Determine if entering or exiting pits based on message
            if "enters" in event.message.lower():
                return f"{driver} dives into the pit lane"
            elif "exits" in event.message.lower():
                # Extract tire compound from message if available
                if "SOFT" in event.message:
                    compound = "soft"
                elif "MEDIUM" in event.message:
                    compound = "medium"
                elif "HARD" in event.message:
                    compound = "hard"
                else:
                    compound = "fresh"
                return f"{driver} rejoins on {compound} tires"
            else:
                return f"{driver} in the pits"
        else:
            return "Pit stop"

    def _generate_fastest_lap_commentary(self, event):
        """
        Generate commentary for fastest lap event.

        Args:
            event: RaceEvent with FASTEST_LAP type

        Returns:
            str: Formatted fastest lap commentary
        """
        if len(event.drivers) >= 1:
            driver = event.drivers[0]
            # Extract lap time from message if available
            if ":" in event.message:
                # Message likely contains lap time
                return f"{driver} sets the fastest lap!"
            else:
                return f"{driver} goes purple!"
        else:
            return "New fastest lap!"

    def _generate_race_end_commentary(self, event):
        """
        Generate commentary for race end event.

        Args:
            event: RaceEvent with RACE_END type

        Returns:
            str: Formatted race end commentary
        """
        if len(event.drivers) >= 1:
            winner = event.drivers[0]
            return f"{winner} takes the checkered flag!"
        else:
            return "And that's the checkered flag!"

    def _generate_blue_flag_commentary(self, event):
        """
        Generate commentary for blue flag event.

        Args:
            event: RaceEvent with BLUE_FLAG type

        Returns:
            str: Formatted blue flag commentary
        """
        if len(event.drivers) >= 1:
            driver = event.drivers[0]
            return f"Blue flags for {driver}"
        else:
            return "Blue flags are out"

    def __repr__(self):
        """String representation for debugging."""
        return "CommentaryGenerator()"
