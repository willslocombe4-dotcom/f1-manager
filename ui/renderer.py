"""
Track Renderer - Visualizes the F1 circuit and cars
"""
import pygame
import math
import random
import config
from assets.colors import get_team_color


class TrackRenderer:
    """Renders the F1 track and cars"""

    def __init__(self, surface):
        self.surface = surface
        self.track_surface = pygame.Surface((config.TRACK_VIEW_WIDTH, config.SCREEN_HEIGHT))
        self.static_surface = None  # Cache for static track elements

    def render(self, race_engine):
        """Render the track and all cars"""
        # Clear track surface
        self.track_surface.fill(config.TRACK_BG_COLOR)

        # Draw track
        self._draw_track(race_engine.track)

        # Draw cars
        self._draw_cars(race_engine)

        # Draw race status
        self._draw_race_status(race_engine)

        # Blit to main surface
        self.surface.blit(self.track_surface, (0, 0))

    def _draw_track(self, track):
        """Draw the track circuit using waypoints with broadcast-quality visuals"""
        # Use cached static surface if available
        if self.static_surface is None:
            self.static_surface = self._create_static_track_surface(track)

        # Blit cached static elements
        self.track_surface.blit(self.static_surface, (0, 0))

    def _create_static_track_surface(self, track):
        """Create cached surface with all static track elements"""
        surface = pygame.Surface((config.TRACK_VIEW_WIDTH, config.SCREEN_HEIGHT))
        waypoints = track.waypoints
        track_width = 35

        if len(waypoints) < 3:
            return surface

        # Get track boundaries
        outer_points, inner_points = track.get_track_boundaries(track_width)

        # LAYER 1: Two-tone grass background
        surface.fill(config.GRASS_BASE_COLOR)

        # Add lighter grass patches for visual variety (fixed seed for consistency)
        random.seed(42)
        for _ in range(5):
            patch_points = []
            center_x = random.randint(100, config.TRACK_VIEW_WIDTH - 100)
            center_y = random.randint(200, config.SCREEN_HEIGHT - 200)
            radius = random.randint(80, 150)
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                px = center_x + math.cos(rad) * radius
                py = center_y + math.sin(rad) * radius
                patch_points.append((px, py))
            if len(patch_points) >= 3:
                pygame.draw.polygon(surface, config.GRASS_LIGHT_COLOR, patch_points)

        # LAYER 2: Gravel traps at corners
        corner_indices = track.get_corner_indices(curvature_threshold=15)
        for corner_idx in corner_indices:
            self._draw_gravel_trap(surface, waypoints, outer_points, corner_idx, track_width)

        # LAYER 3: Track surface
        if len(outer_points) >= 3 and len(inner_points) >= 3:
            track_polygon = outer_points + inner_points[::-1]
            pygame.draw.polygon(surface, config.TRACK_COLOR, track_polygon)

            # Track edges (white lines)
            pygame.draw.lines(surface, (200, 200, 200), True, outer_points, 2)
            pygame.draw.lines(surface, (200, 200, 200), True, inner_points, 2)

        # LAYER 4: Kerbs at corners
        for corner_idx in corner_indices:
            self._draw_kerbs(surface, waypoints, inner_points, corner_idx)

        # LAYER 5: Checkered start/finish line
        self._draw_checkered_start_line(surface, waypoints, track_width)

        # LAYER 6: Racing line (dashed center line)
        for i in range(0, len(waypoints) - 1, 2):
            pygame.draw.line(
                surface,
                config.TRACK_LINE_COLOR,
                waypoints[i],
                waypoints[min(i + 1, len(waypoints) - 1)],
                1
            )

        return surface

    def _draw_gravel_trap(self, surface, waypoints, outer_points, corner_idx, track_width):
        """Draw gravel trap on outside of corner"""
        gravel_points = []
        extend_range = 4  # Waypoints before/after corner

        for offset in range(-extend_range, extend_range + 1):
            idx = (corner_idx + offset) % len(waypoints)

            # Get outer point and extend it further outward
            if idx < len(outer_points):
                ox, oy = outer_points[idx]
                wx, wy = waypoints[idx]

                # Calculate direction from waypoint to outer point
                dx = ox - wx
                dy = oy - wy
                length = math.sqrt(dx * dx + dy * dy)

                if length > 0:
                    # Extend 25 pixels beyond outer edge
                    extension = 25
                    gravel_x = ox + (dx / length) * extension
                    gravel_y = oy + (dy / length) * extension
                    gravel_points.append((gravel_x, gravel_y))

        if len(gravel_points) >= 3:
            # Draw gravel fill
            pygame.draw.polygon(surface, config.GRAVEL_COLOR, gravel_points)
            # Draw border
            pygame.draw.lines(surface, config.GRAVEL_BORDER_COLOR, False, gravel_points, 3)

    def _draw_kerbs(self, surface, waypoints, inner_points, corner_idx):
        """Draw red and white striped kerbs at corner"""
        extend_range = 3  # Waypoints before/after corner
        stripe_count = 0

        for offset in range(-extend_range, extend_range + 1):
            idx = (corner_idx + offset) % len(waypoints)
            next_idx = (idx + 1) % len(waypoints)

            if idx < len(inner_points) and next_idx < len(inner_points):
                # Get inner edge points
                x1, y1 = inner_points[idx]
                x2, y2 = inner_points[next_idx]

                # Alternate red and white
                color = config.KERB_RED if stripe_count % 2 == 0 else config.KERB_WHITE

                # Draw kerb stripe along inner edge
                pygame.draw.line(surface, color, (x1, y1), (x2, y2), config.KERB_WIDTH)

                stripe_count += 1

    def _draw_checkered_start_line(self, surface, waypoints, track_width):
        """Draw checkered flag pattern at start/finish line"""
        if len(waypoints) < 2:
            return

        start_x, start_y = waypoints[0]
        next_x, next_y = waypoints[1]

        # Get perpendicular direction
        dx = next_x - start_x
        dy = next_y - start_y
        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            return

        perp_x = -dy / length
        perp_y = dx / length

        # Draw 8 squares across track width
        num_squares = 8
        square_width = (track_width * 2) / num_squares

        for i in range(num_squares):
            # Calculate position along start line
            t = (i - num_squares / 2) * square_width
            square_x = start_x + perp_x * t
            square_y = start_y + perp_y * t

            # Alternate black and white
            color = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)

            # Draw square
            square_end_x = square_x + perp_x * square_width
            square_end_y = square_y + perp_y * square_width

            # Draw thick line for each square
            pygame.draw.line(
                surface,
                color,
                (square_x, square_y),
                (square_end_x, square_end_y),
                6
            )

    def _draw_cars(self, race_engine):
        """Draw all cars on the track"""
        for car in race_engine.cars:
            x, y = car.get_position_on_track(race_engine.track)
            color = get_team_color(car.team)

            # Draw car shadow
            pygame.draw.circle(
                self.track_surface,
                (20, 20, 20),
                (int(x) + 2, int(y) + 2),
                config.CAR_SIZE
            )

            # Draw car as a circle with position number
            pygame.draw.circle(
                self.track_surface,
                color,
                (int(x), int(y)),
                config.CAR_SIZE
            )

            # Draw outline
            pygame.draw.circle(
                self.track_surface,
                (255, 255, 255),
                (int(x), int(y)),
                config.CAR_SIZE,
                2
            )

            # Draw position number
            font = pygame.font.Font(None, 18)
            pos_text = font.render(str(car.position), True, (255, 255, 255))
            text_rect = pos_text.get_rect(center=(int(x), int(y)))
            self.track_surface.blit(pos_text, text_rect)

    def _draw_race_status(self, race_engine):
        """Draw race status at top of track view"""
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)

        # Race status (LAP X/Y)
        status_text = font_large.render(
            race_engine.get_race_status(),
            True,
            config.TEXT_COLOR
        )
        status_rect = status_text.get_rect(center=(config.TRACK_VIEW_WIDTH // 2, 40))
        self.track_surface.blit(status_text, status_rect)

        # Race time
        minutes = int(race_engine.race_time // 60)
        seconds = int(race_engine.race_time % 60)
        time_text = font_small.render(
            f"{minutes:02d}:{seconds:02d}",
            True,
            config.TEXT_GRAY
        )
        time_rect = time_text.get_rect(center=(config.TRACK_VIEW_WIDTH // 2, 75))
        self.track_surface.blit(time_text, time_rect)

        # Instructions at bottom
        if not race_engine.race_started:
            inst_font = pygame.font.Font(None, 28)
            inst_text = inst_font.render(
                "Press SPACE to start race",
                True,
                config.TEXT_COLOR
            )
            inst_rect = inst_text.get_rect(
                center=(config.TRACK_VIEW_WIDTH // 2, config.SCREEN_HEIGHT - 40)
            )
            self.track_surface.blit(inst_text, inst_rect)
