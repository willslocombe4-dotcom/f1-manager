"""
Timing Screen - F1-style live timing display
"""
import pygame
import config
from assets.colors import get_team_color, get_team_short_name
from ui.commentary_panel import CommentaryPanel

class TimingScreen:
    """Renders F1-style live timing screen"""

    def __init__(self, surface):
        self.surface = surface
        self.timing_surface = pygame.Surface((config.TIMING_VIEW_WIDTH, config.SCREEN_HEIGHT))
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)

        # Initialize commentary panel below timing rows
        # Commentary starts at y=650, giving 250 pixels for commentary (fits 3 events)
        commentary_y = 650
        commentary_height = config.SCREEN_HEIGHT - commentary_y
        self.commentary_panel = CommentaryPanel(
            self.timing_surface,
            x=0,
            y=commentary_y,
            width=config.TIMING_VIEW_WIDTH,
            height=commentary_height
        )
        # Adjust max events to fit available space (250px - 40px header) / 70px per event ≈ 3 events
        self.commentary_panel.max_events_shown = 3

    def render(self, race_engine):
        """Render the timing screen"""
        # Clear timing surface
        self.timing_surface.fill(config.TIMING_BG_COLOR)

        # Draw header
        self._draw_header()

        # Draw timing rows
        self._draw_timing_rows(race_engine)

        # Draw commentary panel
        # Update driver-team mapping for color coding
        self.commentary_panel.update_driver_team_map(race_engine.cars)
        # Render commentary with events from race engine
        self.commentary_panel.render(race_engine.event_manager)

        # Blit to main surface
        self.surface.blit(self.timing_surface, (config.TIMING_VIEW_X, 0))

    def _draw_header(self):
        """Draw timing screen header"""
        # Title
        title_text = self.font_large.render("LIVE TIMING", True, config.TEXT_COLOR)
        self.timing_surface.blit(title_text, (20, 20))

        # Column headers
        y_pos = 70
        headers = [
            ("POS", 20),
            ("DRIVER", 70),
            ("GAP", 280),
            ("LAP", 380),
            ("TIRE", 450)
        ]

        for header, x_pos in headers:
            text = self.font_small.render(header, True, config.TEXT_GRAY)
            self.timing_surface.blit(text, (x_pos, y_pos))

        # Draw separator line
        pygame.draw.line(
            self.timing_surface,
            config.TRACK_LINE_COLOR,
            (10, 95),
            (config.TIMING_VIEW_WIDTH - 10, 95),
            1
        )

    def _draw_timing_rows(self, race_engine):
        """Draw timing information for all cars"""
        start_y = 105
        row_height = 38

        cars = race_engine.get_cars_by_position()

        for i, car in enumerate(cars):
            y_pos = start_y + i * row_height

            # Alternating row background
            if i % 2 == 0:
                pygame.draw.rect(
                    self.timing_surface,
                    (25, 25, 25),
                    (10, y_pos - 3, config.TIMING_VIEW_WIDTH - 20, row_height - 2)
                )

            # Team color bar
            team_color = get_team_color(car.team)
            pygame.draw.rect(
                self.timing_surface,
                team_color,
                (10, y_pos - 3, 5, row_height - 2)
            )

            # Position
            pos_text = self.font_medium.render(str(car.position), True, config.TEXT_COLOR)
            self.timing_surface.blit(pos_text, (25, y_pos))

            # Driver name (short)
            driver_text = self.font_medium.render(car.driver_short, True, config.TEXT_COLOR)
            self.timing_surface.blit(driver_text, (70, y_pos))

            # Team (short name)
            team_short = get_team_short_name(car.team)
            team_text = self.font_small.render(team_short, True, config.TEXT_GRAY)
            self.timing_surface.blit(team_text, (130, y_pos + 2))

            # Gap to leader or ahead
            if car.position == 1:
                gap_text = self.font_medium.render("LEADER", True, config.TEXT_COLOR)
            elif car.gap_to_leader >= 1.0:
                # Show lapped indicator if a full lap behind (progress-based check)
                laps_down = int(car.gap_to_leader)
                gap_str = f"+{laps_down}L"
                gap_text = self.font_medium.render(gap_str, True, (255, 100, 100))
            else:
                # Show time gap to car ahead (in seconds)
                gap_str = f"+{car.gap_to_ahead_time:.3f}"
                gap_text = self.font_medium.render(gap_str, True, config.TEXT_GRAY)

            self.timing_surface.blit(gap_text, (280, y_pos))

            # Current lap
            lap_text = self.font_medium.render(str(car.lap), True, config.TEXT_COLOR)
            self.timing_surface.blit(lap_text, (380, y_pos))

            # Tire compound
            self._draw_tire_indicator(car, 450, y_pos + 5)

    def _draw_tire_indicator(self, car, x, y):
        """Draw tire compound indicator"""
        tire_color = config.TIRE_COLORS.get(car.tire_compound, (255, 255, 255))

        # Draw tire circle
        pygame.draw.circle(
            self.timing_surface,
            tire_color,
            (x + 10, y + 10),
            8
        )
        pygame.draw.circle(
            self.timing_surface,
            (255, 255, 255),
            (x + 10, y + 10),
            8,
            1
        )

        # Draw tire age
        age_text = self.font_small.render(str(car.tire_age), True, config.TEXT_GRAY)
        self.timing_surface.blit(age_text, (x + 25, y + 3))
