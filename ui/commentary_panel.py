"""
Commentary Panel - F1-style race commentary display
"""
import pygame
import config
from assets.colors import get_team_color
from race.commentary import CommentaryGenerator


class CommentaryPanel:
    """Renders F1-style race commentary panel"""

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

        # Display settings
        self.max_events_shown = 5
        self.event_height = 70
        self.padding = 15

        # Scroll animation
        self.scroll_offset = 0.0
        self.target_scroll = 0.0
        self.scroll_speed = 0.15

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

    def render(self, event_manager):
        """
        Render the commentary panel.

        Args:
            event_manager: EventManager instance with race events
        """
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

        # Draw separator line
        pygame.draw.line(
            self.panel_surface,
            config.TRACK_LINE_COLOR,
            (self.padding, 45),
            (self.width - self.padding, 45),
            1
        )

        # Get recent events and generate commentary
        recent_events = event_manager.get_recent_events(self.max_events_shown)

        # Update scroll animation
        self._update_scroll()

        # Draw commentary messages
        self._draw_events(recent_events)

        # Blit to main surface
        self.surface.blit(self.panel_surface, (self.x, self.y))

    def _draw_header(self):
        """Draw commentary panel header"""
        title_text = self.font_title.render("RACE COMMENTARY", True, config.TEXT_COLOR)
        self.panel_surface.blit(title_text, (self.padding, 12))

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
        start_y = 55

        for i, event in enumerate(events):
            y_pos = start_y + i * self.event_height + int(self.scroll_offset)

            # Skip if outside visible area
            if y_pos + self.event_height < start_y or y_pos > self.height:
                continue

            # Calculate fade for older messages
            fade_factor = 1.0 - (i * 0.15)
            fade_factor = max(0.4, min(1.0, fade_factor))

            # Draw event background (alternating)
            if i % 2 == 0:
                bg_rect = pygame.Rect(
                    self.padding,
                    y_pos,
                    self.width - self.padding * 2,
                    self.event_height - 5
                )
                pygame.draw.rect(
                    self.panel_surface,
                    (25, 25, 25),
                    bg_rect
                )

            # Draw lap badge
            self._draw_lap_badge(event, self.padding + 5, y_pos + 10, fade_factor)

            # Draw commentary text with color-coded driver names
            self._draw_commentary_text(event, self.padding + 60, y_pos + 8, fade_factor)

    def _draw_lap_badge(self, event, x, y, fade_factor):
        """
        Draw lap number badge.

        Args:
            event: RaceEvent instance
            x: X position
            y: Y position
            fade_factor: Opacity factor (0.0-1.0)
        """
        # Badge background
        badge_width = 45
        badge_height = 24

        # Apply fade to color
        bg_color = tuple(int(c * fade_factor) for c in (50, 50, 50))
        border_color = tuple(int(c * fade_factor) for c in config.TRACK_LINE_COLOR)

        pygame.draw.rect(
            self.panel_surface,
            bg_color,
            (x, y, badge_width, badge_height),
            border_radius=3
        )
        pygame.draw.rect(
            self.panel_surface,
            border_color,
            (x, y, badge_width, badge_height),
            1,
            border_radius=3
        )

        # Lap text
        lap_text = self.font_lap.render(f"L{event.lap}", True, self._apply_fade(config.TEXT_COLOR, fade_factor))
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
            tuple: Faded RGB color
        """
        return tuple(int(c * fade_factor) for c in color)

    def trigger_scroll(self):
        """Trigger smooth scroll animation when new event appears"""
        # This can be called when a new event is added to animate the scroll
        # For now, we keep the view fixed at the top
        pass
