"""
Race Commentary - Generate broadcast-style F1 commentary for race events
"""
import random
from race.race_events import EventType


class CommentaryGenerator:
    """Generates F1 broadcast-style commentary for race events."""

    # Commentary templates for each event type
    RACE_START_TEMPLATES = [
        "Lights out and away we go!",
        "It's lights out and we are racing!",
        "And the race is underway!",
        "The lights go out and they're off!",
        "Green flag! The race has begun!"
    ]

    OVERTAKE_TEMPLATES = [
        "{overtaker} makes a move on {overtaken}!",
        "{overtaker} sweeps past {overtaken}!",
        "{overtaker} goes around the outside of {overtaken}!",
        "Brilliant move by {overtaker} on {overtaken}!",
        "{overtaker} with the DRS, passes {overtaken}!",
        "{overtaker} dives down the inside of {overtaken}!"
    ]

    PIT_ENTRY_TEMPLATES = [
        "{driver} dives into the pit lane",
        "{driver} comes in for fresh tires",
        "Box, box, box for {driver}",
        "{driver} heads into the pits",
        "Into the pit lane goes {driver}"
    ]

    PIT_EXIT_TEMPLATES = [
        "{driver} rejoins on {compound} tires",
        "{driver} back out on {compound} rubber",
        "{driver} exits the pits on {compound}s",
        "{driver} returns to the track on {compound}s",
        "Out comes {driver} on the {compound} compound"
    ]

    FASTEST_LAP_TEMPLATES = [
        "{driver} goes purple!",
        "{driver} sets the fastest lap!",
        "That's a purple sector for {driver}!",
        "{driver} with blistering pace!",
        "Fastest lap of the race for {driver}!",
        "{driver} puts in a purple lap!"
    ]

    RACE_END_TEMPLATES = [
        "{winner} takes the checkered flag!",
        "{winner} wins the race!",
        "And {winner} crosses the line to victory!",
        "It's {winner} who takes it!",
        "Checkered flag for {winner}!"
    ]

    BLUE_FLAG_TEMPLATES = [
        "Blue flags for {driver}",
        "{driver} shown the blue flags",
        "Blue flags waving for {driver}",
        "{driver} needs to let the leaders through",
        "Lapped traffic ahead - blue flags for {driver}"
    ]

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
        # Randomly select from race start templates
        return random.choice(self.RACE_START_TEMPLATES)

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
            # Randomly select from overtake templates
            template = random.choice(self.OVERTAKE_TEMPLATES)
            return template.format(overtaker=overtaker, overtaken=overtaken)
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
                # Randomly select from pit entry templates
                template = random.choice(self.PIT_ENTRY_TEMPLATES)
                return template.format(driver=driver)
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
                # Randomly select from pit exit templates
                template = random.choice(self.PIT_EXIT_TEMPLATES)
                return template.format(driver=driver, compound=compound)
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
            # Randomly select from fastest lap templates
            template = random.choice(self.FASTEST_LAP_TEMPLATES)
            return template.format(driver=driver)
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
            # Randomly select from race end templates
            template = random.choice(self.RACE_END_TEMPLATES)
            return template.format(winner=winner)
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
            # Randomly select from blue flag templates
            template = random.choice(self.BLUE_FLAG_TEMPLATES)
            return template.format(driver=driver)
        else:
            return "Blue flags are out"

    def __repr__(self):
        """String representation for debugging."""
        return "CommentaryGenerator()"
