"""
Commentary Panel - F1-style race commentary display
"""
import pygame
import time
import config
from assets.colors import get_team_color
from race.commentary import CommentaryGenerator
from race.race_events import EventType


class CommentaryPanel:
    """Renders F1-style race commentary panel"""

    # F1 broadcast-style event type colors
    EVENT_TYPE_COLORS = {
        EventType.RACE_START: (0, 200, 100),      # Green - Race start
        EventType.OVERTAKE: (255, 140, 0),        # Orange - Action/overtake
        EventType.PIT_STOP: (100, 150, 255),      # Blue - Strategic pit stop
        EventType.FASTEST_LAP: (200, 50, 200),    # Purple - Fastest lap (F1 purple sector)
        EventType.BLUE_FLAG: (100, 180, 255),     # Light blue - Blue flag
        EventType.RACE_END: (255, 215, 0),        # Gold - Race finish
    }

    def __init__(self, surface, x, y, width, height):
        """
        Initialize the commentary panel.

        Args:
            surface: Parent pygame surface to draw on
            x: X position of panel
            y: Y position of panel
            width: Width of panel
            height: Height of panel
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Create panel surface
        self.panel_surface = pygame.Surface((width, height))

        # Initialize commentary generator
        self.commentary_generator = CommentaryGenerator()

        # Fonts
        self.font_title = pygame.font.Font(None, 28)
        self.font_commentary = pygame.font.Font(None, 22)
        self.font_lap = pygame.font.Font(None, 18)
        self.font_pause = pygame.font.Font(None, 20)

        # Display settings
        self.max_events_shown = 5
        self.event_height = 70
        self.padding = 15

        # Scroll animation
        self.scroll_offset = 0.0
        self.target_scroll = 0.0
        self.scroll_speed = 0.15

        # Pause functionality
        self.is_paused = False
        self.manual_scroll_index = 0  # Index offset for manual scrolling
        self.last_interaction_time = 0
        self.auto_resume_delay = 5.0  # Seconds of inactivity before auto-resume

        # Cache for team lookup
        self.driver_to_team = {}

    def update_driver_team_map(self, cars):
        """
        Update mapping of driver names to team names for color coding.

        Args:
            cars: List of Car objects from race engine
        """
        self.driver_to_team.clear()
        for car in cars:
            self.driver_to_team[car.driver_name] = car.team

    def toggle_pause(self):
        """Toggle commentary pause state"""
        self.is_paused = not self.is_paused
        self.last_interaction_time = time.time()
        if not self.is_paused:
            # Reset manual scroll when resuming
            self.manual_scroll_index = 0

    def scroll_up(self):
        """Scroll up through commentary (show older events)"""
        if self.is_paused:
            self.manual_scroll_index = min(self.manual_scroll_index + 1, 20)
            self.last_interaction_time = time.time()

    def scroll_down(self):
        """Scroll down through commentary (show newer events)"""
        if self.is_paused:
            self.manual_scroll_index = max(self.manual_scroll_index - 1, 0)
            self.last_interaction_time = time.time()

    def render(self, event_manager):
        """
        Render the commentary panel.

        Args:
            event_manager: EventManager instance with race events
        """
        # Check for auto-resume after inactivity
        if self.is_paused and self.last_interaction_time > 0:
            if time.time() - self.last_interaction_time > self.auto_resume_delay:
                self.is_paused = False
                self.manual_scroll_index = 0

        # Clear panel surface
        self.panel_surface.fill(config.TIMING_BG_COLOR)

        # Draw panel border
        pygame.draw.rect(
            self.panel_surface,
            config.TRACK_LINE_COLOR,
            (0, 0, self.width, self.height),
            2
        )

        # Draw header
        self._draw_header()

        # Draw separator line below header (subtle separation)
        separator_y = 40
        pygame.draw.line(
            self.panel_surface,
            (60, 60, 60),
            (0, separator_y),
            (self.width, separator_y),
            2
        )

        # Get recent events based on pause state
        if self.is_paused:
            # When paused, get more events and offset by manual scroll
            all_events = event_manager.get_recent_events(self.max_events_shown + self.manual_scroll_index)
            recent_events = all_events[self.manual_scroll_index:self.manual_scroll_index + self.max_events_shown]
        else:
            # Normal auto-scroll behavior
            recent_events = event_manager.get_recent_events(self.max_events_shown)

        # Update scroll animation (disabled when paused)
        if not self.is_paused:
            self._update_scroll()

        # Draw commentary messages
        self._draw_events(recent_events)

        # Blit to main surface
        self.surface.blit(self.panel_surface, (self.x, self.y))

    def _draw_header(self):
        """Draw F1 broadcast-style commentary panel header"""
        # Title background bar
        header_height = 40
        pygame.draw.rect(
            self.panel_surface,
            (30, 30, 30),
            (0, 0, self.width, header_height)
        )

        # Accent line at top (F1 broadcast style)
        # Orange when paused, red when active
        accent_color = (255, 140, 0) if self.is_paused else (255, 0, 0)
        pygame.draw.rect(
            self.panel_surface,
            accent_color,
            (0, 0, self.width, 3)
        )

        # Title text
        title_text = self.font_title.render("RACE COMMENTARY", True, config.TEXT_COLOR)
        self.panel_surface.blit(title_text, (self.padding, 10))

        # Draw pause indicator if paused
        if self.is_paused:
            pause_text = self.font_pause.render("PAUSED (C to resume)", True, (255, 140, 0))
            pause_x = self.width - pause_text.get_width() - self.padding
            self.panel_surface.blit(pause_text, (pause_x, 12))

    def _update_scroll(self):
        """Update smooth scroll animation"""
        # Smoothly interpolate current scroll to target
        if abs(self.scroll_offset - self.target_scroll) > 0.1:
            self.scroll_offset += (self.target_scroll - self.scroll_offset) * self.scroll_speed
        else:
            self.scroll_offset = self.target_scroll

    def _draw_events(self, events):
        """
        Draw commentary event messages.

        Args:
            events: List of RaceEvent instances to display
        """
        start_y = 50  # Start just below header separator

        for i, event in enumerate(events):
            y_pos = start_y + i * self.event_height + int(self.scroll_offset)

            # Skip if outside visible area
            if y_pos + self.event_height < start_y or y_pos > self.height:
                continue

            # Calculate fade for older messages
            fade_factor = 1.0 - (i * 0.15)
            fade_factor = max(0.4, min(1.0, fade_factor))

            # Get event type color
            event_color = self.EVENT_TYPE_COLORS.get(event.event_type, (150, 150, 150))

            # Draw event background (alternating)
            bg_y = y_pos
            bg_height = self.event_height - 5

            if i % 2 == 0:
                bg_rect = pygame.Rect(
                    self.padding,
                    bg_y,
                    self.width - self.padding * 2,
                    bg_height
                )
                pygame.draw.rect(
                    self.panel_surface,
                    (25, 25, 25),
                    bg_rect,
                    border_radius=3
                )

            # Draw event type color accent bar (F1 broadcast style)
            accent_width = 4
            accent_color = self._apply_fade(event_color, fade_factor)
            pygame.draw.rect(
                self.panel_surface,
                accent_color,
                (self.padding, bg_y, accent_width, bg_height),
                border_radius=2
            )

            # Draw lap badge with event type color
            self._draw_lap_badge(event, self.padding + 10, y_pos + 10, fade_factor, event_color)

            # Draw commentary text with color-coded driver names
            self._draw_commentary_text(event, self.padding + 65, y_pos + 8, fade_factor)

    def _draw_lap_badge(self, event, x, y, fade_factor, event_color):
        """
        Draw lap number badge with F1 broadcast styling.

        Args:
            event: RaceEvent instance
            x: X position
            y: Y position
            fade_factor: Opacity factor (0.0-1.0)
            event_color: RGB tuple for event type color
        """
        # Enhanced badge dimensions
        badge_width = 45
        badge_height = 26

        # Apply fade to colors
        bg_color = tuple(int(c * fade_factor) for c in (35, 35, 35))
        border_color = self._apply_fade(event_color, fade_factor * 0.8)

        # Draw badge background with subtle gradient effect
        pygame.draw.rect(
            self.panel_surface,
            bg_color,
            (x, y, badge_width, badge_height),
            border_radius=4
        )

        # Draw colored border (thicker for more prominence)
        pygame.draw.rect(
            self.panel_surface,
            border_color,
            (x, y, badge_width, badge_height),
            2,
            border_radius=4
        )

        # Lap text with bright event color
        lap_color = self._apply_fade(event_color, min(fade_factor * 1.1, 1.0))
        lap_text = self.font_lap.render(f"L{event.lap}", True, lap_color)
        lap_rect = lap_text.get_rect(center=(x + badge_width // 2, y + badge_height // 2))
        self.panel_surface.blit(lap_text, lap_rect)

    def _draw_commentary_text(self, event, x, y, fade_factor):
        """
        Draw commentary text with color-coded driver names.

        Args:
            event: RaceEvent instance
            x: X position
            y: Y position
            fade_factor: Opacity factor (0.0-1.0)
        """
        # Generate commentary from event
        commentary = self.commentary_generator.generate_commentary(event)

        # Word wrap the commentary to fit panel width
        available_width = self.width - x - self.padding
        wrapped_lines = self._wrap_text(commentary, available_width)

        # Draw each line
        for i, line in enumerate(wrapped_lines[:2]):  # Max 2 lines per event
            line_y = y + i * 22

            # Try to color-code driver names if present
            self._draw_colored_line(line, event.drivers, x, line_y, fade_factor)

    def _draw_colored_line(self, text, drivers, x, y, fade_factor):
        """
        Draw text line with color-coded driver names.

        Args:
            text: Text to draw
            drivers: List of driver names in this event
            x: X position
            y: Y position
            fade_factor: Opacity factor (0.0-1.0)
        """
        current_x = x
        words = text.split()

        for word in words:
            # Check if word matches a driver name (case insensitive)
            word_color = config.TEXT_COLOR

            for driver in drivers:
                # Check if driver name is in the word (handles partial matches)
                if driver.lower() in word.lower():
                    # Get team color for this driver
                    team = self.driver_to_team.get(driver)
                    if team:
                        word_color = get_team_color(team)
                    break

            # Apply fade
            word_color = self._apply_fade(word_color, fade_factor)

            # Render word
            word_surface = self.font_commentary.render(word + " ", True, word_color)
            self.panel_surface.blit(word_surface, (current_x, y))
            current_x += word_surface.get_width()

    def _wrap_text(self, text, max_width):
        """
        Word wrap text to fit within max width.

        Args:
            text: Text to wrap
            max_width: Maximum width in pixels

        Returns:
            list: List of text lines
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            # Test if adding this word exceeds max width
            test_line = " ".join(current_line + [word])
            test_surface = self.font_commentary.render(test_line, True, (255, 255, 255))

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        # Add remaining words
        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def _apply_fade(self, color, fade_factor):
        """
        Apply fade factor to a color.

        Args:
            color: RGB tuple (r, g, b)
            fade_factor: Opacity factor (0.0-1.0)

        Returns:
            tuple: Faded RGB color (clamped to 0-255)
        """
        return tuple(max(0, min(255, int(c * fade_factor))) for c in color)

    def trigger_scroll(self):
        """Trigger smooth scroll animation when new event appears"""
        # This can be called when a new event is added to animate the scroll
        # For now, we keep the view fixed at the top
        pass
