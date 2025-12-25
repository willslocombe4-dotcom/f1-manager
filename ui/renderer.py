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
        
        # Cache fonts for performance (avoid creating fonts every frame)
        self.font_car_position = pygame.font.Font(None, 18)
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        self.font_instructions = pygame.font.Font(None, 28)
        self.font_speed = pygame.font.Font(None, 20)
        
        # Speed control button dimensions
        self.speed_button_width = 35
        self.speed_button_height = 25
        self.speed_button_margin = 5

    def reset_cache(self):
        """Clear cached static track surface when track changes"""
        self.static_surface = None

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
        
        # Draw speed controls
        self._draw_speed_controls(race_engine)

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
        left_boundary, right_boundary = track.get_track_boundaries(track_width)

        # LAYER 1: Background - plain dark, no auto-decorations
        # All decorations are now explicit via track_decorator tool
        surface.fill(config.TRACK_BG_COLOR)

        # LAYER 1.5: Grass (only if track has explicit decorations)
        # Grass is drawn first (behind gravel) so it appears as background
        if hasattr(track, 'decorations') and track.decorations:
            for grass in track.decorations.get('grass', []):
                self._draw_grass_range(
                    surface, track, grass['boundary'],
                    grass['start'], grass['end'], track_width
                )

        # LAYER 2: Gravel traps (only if track has explicit decorations)
        # Auto-generation disabled - use track_decorator tool to add decorations
        if hasattr(track, 'decorations') and track.decorations:
            for gravel in track.decorations.get('gravel', []):
                self._draw_gravel_range(
                    surface, track, gravel['boundary'],
                    gravel['start'], gravel['end'], track_width
                )

        # LAYER 3: Track surface
        # Simple quad rendering - bevel joins don't need validation
        if len(left_boundary) >= 3 and len(right_boundary) >= 3:
            num_points = len(left_boundary)
            for i in range(num_points):
                next_i = (i + 1) % num_points
                quad = [left_boundary[i], left_boundary[next_i], right_boundary[next_i], right_boundary[i]]
                pygame.draw.polygon(surface, config.TRACK_COLOR, quad)
            
            # Track edges (white lines)
            pygame.draw.lines(surface, (200, 200, 200), True, left_boundary, 2)
            pygame.draw.lines(surface, (200, 200, 200), True, right_boundary, 2)

        # LAYER 4: Kerbs at corners (only if track has explicit decorations)
        # Auto-generation disabled - use track_decorator tool to add decorations
        if hasattr(track, 'decorations') and track.decorations:
            for kerb in track.decorations.get('kerbs', []):
                self._draw_kerb_range(
                    surface, track, kerb['boundary'],
                    kerb['start'], kerb['end'], track_width
                )

        # LAYER 5: Checkered start/finish line (only if track has explicit start_line decoration)
        if hasattr(track, 'decorations') and track.decorations.get('start_line'):
            start_line = track.decorations['start_line']
            self._draw_checkered_start_line(surface, waypoints, track_width, start_line.get('segment', 0))
        # If no explicit start_line, don't draw one - user controls everything

        # LAYER 6: Racing line - only if explicitly enabled in decorations
        if hasattr(track, 'decorations') and track.decorations.get('racing_line'):
            for i in range(0, len(waypoints) - 1, 2):
                pygame.draw.line(
                    surface,
                    config.TRACK_LINE_COLOR,
                    waypoints[i],
                    waypoints[min(i + 1, len(waypoints) - 1)],
                    1
                )

        return surface

    def _draw_gravel_trap(self, surface, waypoints, left_boundary, right_boundary, corner_idx, track_width):
        """Draw gravel trap on outside of corner (correct side based on turn direction)"""
        # Determine turn direction at this corner using cross product
        prev_idx = (corner_idx - 1) % len(waypoints)
        next_idx = (corner_idx + 1) % len(waypoints)
        
        x1, y1 = waypoints[prev_idx]
        x2, y2 = waypoints[corner_idx]
        x3, y3 = waypoints[next_idx]
        
        # Cross product: positive = left turn (CCW), negative = right turn (CW)
        cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
        
        # Choose which boundary is the OUTSIDE of the turn
        # For a clockwise track: left_boundary = outer loop, right_boundary = inner loop
        # Left turn (cross > 0): outside is toward OUTER loop = left_boundary
        # Right turn (cross < 0): outside is toward INNER loop = right_boundary
        if cross > 0:
            boundary_points = left_boundary   # Left turn: outside toward outer loop
        else:
            boundary_points = right_boundary  # Right turn: outside toward inner loop
        
        gravel_outer_points = []  # Extended points (outer edge of gravel)
        gravel_inner_points = []  # Track boundary edge (inner edge of gravel)
        extend_range = 4  # Waypoints before/after corner

        for offset in range(-extend_range, extend_range + 1):
            idx = (corner_idx + offset) % len(waypoints)

            # Get boundary point and extend it further outward
            if idx < len(boundary_points):
                bx, by = boundary_points[idx]
                wx, wy = waypoints[idx]

                # Calculate direction from waypoint to boundary point
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx * dx + dy * dy)

                if length > 0:
                    # Store the track boundary edge point (inner boundary of gravel)
                    gravel_inner_points.append((bx, by))

                    # Extend 25 pixels beyond boundary edge for gravel outer boundary
                    extension = 25
                    gravel_x = bx + (dx / length) * extension
                    gravel_y = by + (dy / length) * extension
                    gravel_outer_points.append((gravel_x, gravel_y))

        if len(gravel_outer_points) >= 3 and len(gravel_inner_points) >= 3:
            # Create closed polygon: outer edge forward, then inner edge backward
            # This creates a band/strip shape between track edge and gravel outer edge
            gravel_polygon = gravel_outer_points + gravel_inner_points[::-1]

            # Draw gravel fill
            pygame.draw.polygon(surface, config.GRAVEL_COLOR, gravel_polygon)
            # Draw border only on outer edge
            pygame.draw.lines(surface, config.GRAVEL_BORDER_COLOR, False, gravel_outer_points, 3)

    def _draw_kerbs(self, surface, waypoints, left_boundary, right_boundary, corner_idx):
        """
        Draw kerb segments on the INSIDE (apex) of corners.
        
        Left turn (positive angle): apex is on LEFT side (left_boundary)
        Right turn (negative angle): apex is on RIGHT side (right_boundary)
        """
        from race.track import get_angle_between_segments
        
        # Check if this is a significant corner
        prev_idx = (corner_idx - 1) % len(waypoints)
        next_idx = (corner_idx + 1) % len(waypoints)
        
        corner_angle = get_angle_between_segments(
            waypoints[prev_idx], waypoints[corner_idx], waypoints[next_idx]
        )
        
        # Only draw kerbs for significant corners (> 30 degrees)
        if abs(corner_angle) < math.radians(30):
            return
        
        # Choose the INSIDE boundary (apex side)
        # For a clockwise track (which this is, based on boundary test):
        # - Left turn (angle > 0): apex is on RIGHT side (toward inner loop)
        # - Right turn (angle < 0): apex is on LEFT side (toward outer loop)
        # This matches the gravel trap logic which uses cross product correctly.
        if corner_angle > 0:
            boundary_points = right_boundary  # Left turn: apex on RIGHT (inner)
        else:
            boundary_points = left_boundary   # Right turn: apex on LEFT (outer)
        
        stripe_count = 0
        for offset in range(0, 2):  # Just 2 segments
            idx = (corner_idx + offset) % len(waypoints)
            next_wp_idx = (idx + 1) % len(waypoints)
            
            if idx >= len(boundary_points) or next_wp_idx >= len(boundary_points):
                continue
            
            bx1, by1 = boundary_points[idx]
            bx2, by2 = boundary_points[next_wp_idx]
            
            # Alternate red and white
            color = config.KERB_RED if stripe_count % 2 == 0 else config.KERB_WHITE
            pygame.draw.line(surface, color, (bx1, by1), (bx2, by2), config.KERB_WIDTH)
            stripe_count += 1

    def _draw_kerb_range(self, surface, track, boundary, start, end, track_width=35):
        """
        Draw alternating red/white kerb stripes for an explicit segment range.
        
        Args:
            surface: pygame surface to draw on
            track: Track object
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
            track_width: Width of track from center to boundary
        """
        boundary_points = track.get_boundary_points_for_range(boundary, start, end, track_width)
        
        if len(boundary_points) < 2:
            return
        
        # Draw alternating stripes
        for i in range(len(boundary_points) - 1):
            p1 = boundary_points[i]
            p2 = boundary_points[i + 1]
            
            # Alternate red and white
            color = config.KERB_RED if i % 2 == 0 else config.KERB_WHITE
            pygame.draw.line(surface, color, p1, p2, config.KERB_WIDTH)

    def _draw_gravel_range(self, surface, track, boundary, start, end, track_width=35):
        """
        Draw gravel strip polygon for an explicit segment range.
        
        Args:
            surface: pygame surface to draw on
            track: Track object
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
            track_width: Width of track from center to boundary
        """
        inner_points, outer_points = track.get_gravel_strip_points(
            boundary, start, end, track_width, extension=25
        )
        
        if len(outer_points) < 3 or len(inner_points) < 3:
            return
        
        # Create closed polygon: outer edge forward, then inner edge backward
        gravel_polygon = outer_points + inner_points[::-1]
        
        # Draw gravel fill
        pygame.draw.polygon(surface, config.GRAVEL_COLOR, gravel_polygon)
        # Draw border only on outer edge
        pygame.draw.lines(surface, config.GRAVEL_BORDER_COLOR, False, outer_points, 3)

    def _draw_grass_range(self, surface, track, boundary, start, end, track_width=35):
        """
        Draw grass strip polygon for an explicit segment range.
        
        Args:
            surface: pygame surface to draw on
            track: Track object
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
            track_width: Width of track from center to boundary
        """
        # Grass extends further than gravel (50px vs 25px)
        inner_points, outer_points = track.get_gravel_strip_points(
            boundary, start, end, track_width, extension=50
        )
        
        if len(outer_points) < 3 or len(inner_points) < 3:
            return
        
        # Create closed polygon: outer edge forward, then inner edge backward
        grass_polygon = outer_points + inner_points[::-1]
        
        # Draw grass fill (no border for grass - it blends naturally)
        pygame.draw.polygon(surface, config.GRASS_COLOR, grass_polygon)

    def _draw_checkered_start_line(self, surface, waypoints, track_width, segment=0):
        """Draw checkered flag pattern at start/finish line"""
        if len(waypoints) < 2:
            return

        # Use specified segment for start line position
        idx = segment % len(waypoints)
        next_idx = (idx + 1) % len(waypoints)
        
        start_x, start_y = waypoints[idx]
        next_x, next_y = waypoints[next_idx]

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
        """Draw all cars on the track with smooth motion"""
        for car in race_engine.cars:
            # Use smoothed display position (no int() - pygame-ce supports floats)
            x, y = car.get_display_position(race_engine.track)
            color = get_team_color(car.team)

            # Draw car shadow
            pygame.draw.circle(
                self.track_surface,
                (20, 20, 20),
                (x + 2, y + 2),
                config.CAR_SIZE
            )

            # Draw car as a circle with position number
            pygame.draw.circle(
                self.track_surface,
                color,
                (x, y),
                config.CAR_SIZE
            )

            # Draw outline
            pygame.draw.circle(
                self.track_surface,
                (255, 255, 255),
                (x, y),
                config.CAR_SIZE,
                2
            )

            # Draw position number
            pos_text = self.font_car_position.render(str(car.position), True, (255, 255, 255))
            text_rect = pos_text.get_rect(center=(x, y))
            self.track_surface.blit(pos_text, text_rect)

    def _draw_race_status(self, race_engine):
        """Draw race status at top of track view"""
        # Race status (LAP X/Y)
        status_text = self.font_large.render(
            race_engine.get_race_status(),
            True,
            config.TEXT_COLOR
        )
        status_rect = status_text.get_rect(center=(config.TRACK_VIEW_WIDTH // 2, 40))
        self.track_surface.blit(status_text, status_rect)

        # Race time
        minutes = int(race_engine.race_time // 60)
        seconds = int(race_engine.race_time % 60)
        time_text = self.font_small.render(
            f"{minutes:02d}:{seconds:02d}",
            True,
            config.TEXT_GRAY
        )
        time_rect = time_text.get_rect(center=(config.TRACK_VIEW_WIDTH // 2, 75))
        self.track_surface.blit(time_text, time_rect)

        # Instructions at bottom
        if not race_engine.race_started:
            inst_text = self.font_instructions.render(
                "Press SPACE to start race",
                True,
                config.TEXT_COLOR
            )
            inst_rect = inst_text.get_rect(
                center=(config.TRACK_VIEW_WIDTH // 2, config.SCREEN_HEIGHT - 40)
            )
            self.track_surface.blit(inst_text, inst_rect)

    def _draw_speed_controls(self, race_engine):
        """Draw speed control buttons in top right"""
        options = config.SIMULATION_SPEED_OPTIONS
        current_speed = race_engine.simulation_speed
        
        # Position in top right
        start_x = config.TRACK_VIEW_WIDTH - (len(options) * (self.speed_button_width + self.speed_button_margin)) - 10
        y = 10
        
        for i, speed in enumerate(options):
            x = start_x + i * (self.speed_button_width + self.speed_button_margin)
            
            # Button background
            is_active = (speed == current_speed)
            bg_color = (0, 150, 0) if is_active else (60, 60, 60)
            pygame.draw.rect(self.track_surface, bg_color, (x, y, self.speed_button_width, self.speed_button_height))
            pygame.draw.rect(self.track_surface, (100, 100, 100), (x, y, self.speed_button_width, self.speed_button_height), 1)
            
            # Button text
            text = self.font_speed.render(f"{speed}x", True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + self.speed_button_width // 2, y + self.speed_button_height // 2))
            self.track_surface.blit(text, text_rect)
