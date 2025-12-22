"""
Results Screen - F1-style race results display with scrolling
"""
import pygame
import config
from assets.colors import get_team_color, get_team_short_name


class ResultsScreen:
    """Displays F1-style race results after race completion"""

    def __init__(self, surface):
        self.surface = surface
        self.results_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.font_title = pygame.font.Font(None, 64)
        self.font_header = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        self.font_instruction = pygame.font.Font(None, 28)

        # Scroll state
        self.scroll_offset = 0
        self.row_height = 32
        self.visible_rows = 15  # Number of rows visible at once
        self.max_scroll = 0  # Will be calculated based on number of drivers

    def handle_scroll(self, event):
        """Handle scroll events (keyboard and mouse wheel)"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.key == pygame.K_DOWN:
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 1)
        elif event.type == pygame.MOUSEWHEEL:
            # Mouse wheel: positive y is scroll up, negative is scroll down
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y))

    def reset_scroll(self):
        """Reset scroll position to top"""
        self.scroll_offset = 0

    def render(self, race_engine):
        """Render the results screen"""
        # Clear results surface with dark background
        self.results_surface.fill(config.BG_COLOR)

        # Draw header
        self._draw_header(race_engine)

        # Draw results table
        self._draw_results_table(race_engine)

        # Draw instructions
        self._draw_instructions()

        # Blit to main surface
        self.surface.blit(self.results_surface, (0, 0))

    def _draw_header(self, race_engine):
        """Draw results screen header"""
        # Title with F1 style
        title_text = self.font_title.render("RACE RESULTS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 60))
        self.results_surface.blit(title_text, title_rect)

        # Subtitle with race info
        subtitle = f"{race_engine.total_laps} LAPS COMPLETE"
        subtitle_text = self.font_small.render(subtitle, True, config.TEXT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(config.SCREEN_WIDTH // 2, 110))
        self.results_surface.blit(subtitle_text, subtitle_rect)

        # Draw separator line
        pygame.draw.line(
            self.results_surface,
            config.TRACK_LINE_COLOR,
            (150, 140),
            (config.SCREEN_WIDTH - 150, 140),
            2
        )

    def _draw_results_table(self, race_engine):
        """Draw the results table with all finishing positions"""
        # Table start position
        start_x = 200
        start_y = 180
        row_height = self.row_height

        # Column positions
        pos_x = start_x
        driver_x = start_x + 80
        team_x = start_x + 320
        gap_x = start_x + 600

        # Draw column headers
        header_y = start_y
        headers = [
            ("POS", pos_x),
            ("DRIVER", driver_x),
            ("TEAM", team_x),
            ("GAP", gap_x)
        ]

        for header, x_pos in headers:
            text = self.font_small.render(header, True, config.TEXT_GRAY)
            self.results_surface.blit(text, (x_pos, header_y))

        # Draw separator line under headers
        pygame.draw.line(
            self.results_surface,
            config.TRACK_LINE_COLOR,
            (start_x - 30, header_y + 30),
            (gap_x + 200, header_y + 30),
            1
        )

        # Get all cars and calculate max scroll
        cars = race_engine.get_cars_by_position()
        total_drivers = len(cars)
        self.max_scroll = max(0, total_drivers - self.visible_rows)

        # Define scrollable area (between header and instructions)
        scroll_area_top = start_y + 50
        scroll_area_bottom = config.SCREEN_HEIGHT - 110  # Leave room for instructions

        # Calculate which rows to render based on scroll offset
        first_visible_row = self.scroll_offset
        last_visible_row = min(total_drivers, first_visible_row + self.visible_rows)

        # Draw results for visible drivers only
        for i in range(first_visible_row, last_visible_row):
            car = cars[i]
            # Calculate y position adjusted for scroll
            display_index = i - first_visible_row
            y_pos = scroll_area_top + display_index * row_height

            # Alternating row background for better readability
            if i % 2 == 0:
                pygame.draw.rect(
                    self.results_surface,
                    (25, 25, 25),
                    (start_x - 30, y_pos - 5, gap_x + 200 - start_x + 30, row_height - 2)
                )

            # Highlight podium positions
            if i == 0:
                # Winner - gold
                pygame.draw.rect(
                    self.results_surface,
                    (255, 215, 0, 50),
                    (start_x - 30, y_pos - 5, gap_x + 200 - start_x + 30, row_height - 2)
                )
            elif i == 1:
                # Second - silver
                pygame.draw.rect(
                    self.results_surface,
                    (192, 192, 192, 30),
                    (start_x - 30, y_pos - 5, gap_x + 200 - start_x + 30, row_height - 2)
                )
            elif i == 2:
                # Third - bronze
                pygame.draw.rect(
                    self.results_surface,
                    (205, 127, 50, 30),
                    (start_x - 30, y_pos - 5, gap_x + 200 - start_x + 30, row_height - 2)
                )

            # Team color bar
            team_color = get_team_color(car.team)
            pygame.draw.rect(
                self.results_surface,
                team_color,
                (start_x - 30, y_pos - 5, 6, row_height - 2)
            )

            # Position number
            pos_text = self.font_medium.render(str(car.position), True, config.TEXT_COLOR)
            self.results_surface.blit(pos_text, (pos_x, y_pos))

            # Driver name
            driver_text = self.font_medium.render(car.driver_name, True, config.TEXT_COLOR)
            self.results_surface.blit(driver_text, (driver_x, y_pos))

            # Team name
            team_text = self.font_small.render(car.team, True, config.TEXT_GRAY)
            self.results_surface.blit(team_text, (team_x, y_pos + 3))

            # Gap to winner
            if car.position == 1:
                gap_text = self.font_medium.render("WINNER", True, (0, 255, 100))
            else:
                # Calculate time gap in seconds (approximate)
                gap_seconds = car.gap_to_leader * 60  # Rough conversion
                if gap_seconds >= 1.0:
                    if car.gap_to_leader >= 1.0:
                        # More than a lap down
                        laps_down = int(car.gap_to_leader)
                        gap_str = f"+{laps_down} LAP" if laps_down == 1 else f"+{laps_down} LAPS"
                        gap_text = self.font_medium.render(gap_str, True, (255, 100, 100))
                    else:
                        gap_str = f"+{gap_seconds:.1f}s"
                        gap_text = self.font_medium.render(gap_str, True, config.TEXT_GRAY)
                else:
                    gap_str = f"+{gap_seconds:.2f}s"
                    gap_text = self.font_medium.render(gap_str, True, config.TEXT_GRAY)

            self.results_surface.blit(gap_text, (gap_x, y_pos))

        # Draw scroll indicators if needed
        if total_drivers > self.visible_rows:
            self._draw_scroll_indicators(start_x, scroll_area_top, scroll_area_bottom)

    def _draw_scroll_indicators(self, start_x, scroll_area_top, scroll_area_bottom):
        """Draw scroll indicators to show there's more content"""
        indicator_x = config.SCREEN_WIDTH - 100

        # Up arrow if not at top
        if self.scroll_offset > 0:
            up_text = self.font_large.render("▲", True, (255, 255, 255))
            self.results_surface.blit(up_text, (indicator_x, scroll_area_top + 10))

        # Down arrow if not at bottom
        if self.scroll_offset < self.max_scroll:
            down_text = self.font_large.render("▼", True, (255, 255, 255))
            self.results_surface.blit(down_text, (indicator_x, scroll_area_bottom - 40))

        # Position indicator (e.g., "1-15 of 20")
        first_shown = self.scroll_offset + 1
        last_shown = min(self.scroll_offset + self.visible_rows, self.max_scroll + self.visible_rows)
        total = self.max_scroll + self.visible_rows
        position_text = f"{first_shown}-{last_shown} of {total}"
        pos_render = self.font_small.render(position_text, True, config.TEXT_GRAY)
        pos_rect = pos_render.get_rect(center=(indicator_x + 10, (scroll_area_top + scroll_area_bottom) // 2))
        self.results_surface.blit(pos_render, pos_rect)

    def _draw_instructions(self):
        """Draw instructions for user actions"""
        instructions_y = config.SCREEN_HEIGHT - 80

        # Draw semi-transparent background bar
        pygame.draw.rect(
            self.results_surface,
            (30, 30, 30),
            (0, instructions_y - 10, config.SCREEN_WIDTH, 100)
        )

        # Instructions text - now includes scroll instructions
        instruction1 = "↑↓ or Mouse Wheel to scroll"
        instruction2 = "R to restart | SPACE for new race"
        instruction3 = "ESC to quit"

        inst1_text = self.font_instruction.render(instruction1, True, config.TEXT_COLOR)
        inst2_text = self.font_instruction.render(instruction2, True, config.TEXT_COLOR)
        inst3_text = self.font_instruction.render(instruction3, True, config.TEXT_GRAY)

        # Center align all instructions
        inst1_rect = inst1_text.get_rect(center=(config.SCREEN_WIDTH // 2 - 350, instructions_y + 10))
        inst2_rect = inst2_text.get_rect(center=(config.SCREEN_WIDTH // 2, instructions_y + 10))
        inst3_rect = inst3_text.get_rect(center=(config.SCREEN_WIDTH // 2 + 350, instructions_y + 10))

        self.results_surface.blit(inst1_text, inst1_rect)
        self.results_surface.blit(inst2_text, inst2_rect)
        self.results_surface.blit(inst3_text, inst3_rect)

        # Draw separator line above instructions
        pygame.draw.line(
            self.results_surface,
            config.TRACK_LINE_COLOR,
            (0, instructions_y - 10),
            (config.SCREEN_WIDTH, instructions_y - 10),
            2
        )
