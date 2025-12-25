#!/usr/bin/env python3
"""
Track Boundary Visual Test Tool

Tests track boundary generation and highlights problem areas.
Run: python tools/test_track_boundaries.py [track_file.json]

Controls:
- Click: Select waypoint to see detailed info
- N: Cycle through problem areas
- S: Save screenshot
- Q/Esc: Quit
- +/-: Zoom in/out
- Arrow keys: Pan view
"""

import sys
import os
import math
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from race.track import Track, get_angle_between_segments
from race.track_loader import load_track_waypoints, get_default_waypoints
import config

# Window settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60

# Colors for visualization
COLOR_BG = (30, 30, 30)
COLOR_TRACK = (60, 60, 60)
COLOR_WAYPOINT = (255, 255, 255)
COLOR_OUTER = (100, 100, 255)      # Blue for outer/left boundary
COLOR_INNER = (255, 100, 100)      # Red for inner/right boundary
COLOR_CORNER = (255, 255, 0)       # Yellow for corners
COLOR_PROBLEM = (255, 0, 255)      # Magenta for problems
COLOR_CROSSED = (255, 165, 0)      # Orange for crossed boundaries
COLOR_COLLAPSED = (255, 50, 50)    # Bright red for collapsed
COLOR_SELECTED = (0, 255, 255)     # Cyan for selected waypoint
COLOR_CONNECTION = (80, 80, 80)    # Gray for connection lines
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_PANEL = (25, 25, 25)

# Sizes
WAYPOINT_RADIUS = 4
BOUNDARY_RADIUS = 3
CORNER_RADIUS = 6
PROBLEM_RADIUS = 8
TRACK_WIDTH = 35  # Default track width for boundary generation


class BoundaryProblem:
    """Represents a detected boundary problem"""
    
    def __init__(self, index, problem_type, details=None):
        self.index = index
        self.problem_type = problem_type
        self.details = details or {}
    
    def __repr__(self):
        return f"Problem({self.index}, {self.problem_type})"


class TrackBoundaryTester:
    """Visual test tool for track boundary generation"""
    
    def __init__(self, track_file=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Track Boundary Test Tool")
        self.clock = pygame.time.Clock()
        
        # Fonts (cached in __init__ for performance)
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        self.font_title = pygame.font.Font(None, 40)
        
        # Load track
        self.track_file = track_file
        self.track = self._load_track(track_file)
        self.waypoints = self.track.waypoints
        
        # Generate boundaries
        self.track_width = TRACK_WIDTH
        self.left_boundary, self.right_boundary = self.track.get_track_boundaries(self.track_width)
        self.corner_indices = self.track.get_corner_indices(curvature_threshold=15)
        
        # Analyze for problems
        self.problems = self._analyze_boundaries()
        self.current_problem_index = 0
        
        # UI state
        self.selected_waypoint = None
        self.hover_waypoint = None
        self.show_connections = True
        self.show_distances = False
        
        # View transform (for pan/zoom)
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        
        # Print initial analysis
        self._print_analysis()
    
    def _load_track(self, track_file):
        """Load track from file or use default"""
        if track_file:
            # Try to load from file
            if os.path.exists(track_file):
                waypoints = load_track_waypoints(track_file)
                if waypoints:
                    print(f"Loaded track from: {track_file}")
                    return Track(waypoints)
            
            # Try in tracks directory
            tracks_path = os.path.join(config.TRACKS_DIRECTORY, track_file)
            if os.path.exists(tracks_path):
                waypoints = load_track_waypoints(tracks_path)
                if waypoints:
                    print(f"Loaded track from: {tracks_path}")
                    return Track(waypoints)
            
            print(f"Warning: Could not load '{track_file}', using default track")
        
        print("Using default track")
        return Track()
    
    def _analyze_boundaries(self):
        """Analyze track boundaries and return list of problems"""
        problems = []
        waypoints = self.waypoints
        outer_points = self.left_boundary
        inner_points = self.right_boundary
        
        if len(waypoints) < 3 or len(outer_points) < 3 or len(inner_points) < 3:
            return problems
        
        for i in range(len(waypoints)):
            wx, wy = waypoints[i]
            ox, oy = outer_points[i]
            ix, iy = inner_points[i]
            
            # Distance from waypoint to each boundary
            outer_dist = math.sqrt((ox - wx)**2 + (oy - wy)**2)
            inner_dist = math.sqrt((ix - wx)**2 + (iy - wy)**2)
            
            # Check 1: Collapsed boundaries (too close to racing line)
            if outer_dist < self.track_width * 0.5 or inner_dist < self.track_width * 0.5:
                problems.append(BoundaryProblem(i, 'collapsed', {
                    'outer_dist': outer_dist,
                    'inner_dist': inner_dist,
                    'expected': self.track_width
                }))
                continue
            
            # Check 2: Wrong side detection using cross product
            # Get direction of track at this point
            prev_i = (i - 1) % len(waypoints)
            next_i = (i + 1) % len(waypoints)
            dx = waypoints[next_i][0] - waypoints[prev_i][0]
            dy = waypoints[next_i][1] - waypoints[prev_i][1]
            
            # Cross product to determine which side each boundary is on
            # Outer should be on LEFT (positive cross), inner on RIGHT (negative cross)
            outer_cross = dx * (oy - wy) - dy * (ox - wx)
            inner_cross = dx * (iy - wy) - dy * (ix - wx)
            
            if outer_cross < 0 or inner_cross > 0:
                problems.append(BoundaryProblem(i, 'wrong_side', {
                    'outer_cross': outer_cross,
                    'inner_cross': inner_cross,
                    'outer_should_be': 'positive (left)',
                    'inner_should_be': 'negative (right)'
                }))
                continue
            
            # Check 3: Boundaries too close to each other (crossing)
            boundary_dist = math.sqrt((ox - ix)**2 + (oy - iy)**2)
            expected_boundary_dist = self.track_width * 2
            if boundary_dist < expected_boundary_dist * 0.3:
                problems.append(BoundaryProblem(i, 'crossed', {
                    'boundary_dist': boundary_dist,
                    'expected': expected_boundary_dist
                }))
        
        return problems
    
    def _print_analysis(self):
        """Print analysis to console"""
        print("\n" + "=" * 60)
        print("TRACK BOUNDARY ANALYSIS")
        print("=" * 60)
        print(f"Track file: {self.track_file or 'default'}")
        print(f"Total waypoints: {len(self.waypoints)}")
        print(f"Total corners: {len(self.corner_indices)}")
        print(f"Track width: {self.track_width}px")
        print(f"Problem areas: {len(self.problems)}")
        print("-" * 60)
        
        if self.problems:
            print("\nPROBLEM DETAILS:")
            for p in self.problems:
                print(f"\n  [{p.index:3d}] {p.problem_type.upper()}")
                for key, value in p.details.items():
                    if isinstance(value, float):
                        print(f"        {key}: {value:.2f}")
                    else:
                        print(f"        {key}: {value}")
        else:
            print("\n  No problems detected!")
        
        print("\n" + "=" * 60)
        print("CORNER ANALYSIS:")
        print("-" * 60)
        for idx in self.corner_indices[:10]:  # Show first 10 corners
            prev_i = (idx - 1) % len(self.waypoints)
            next_i = (idx + 1) % len(self.waypoints)
            angle = get_angle_between_segments(
                self.waypoints[prev_i],
                self.waypoints[idx],
                self.waypoints[next_i]
            )
            angle_deg = math.degrees(angle)
            direction = "LEFT" if angle > 0 else "RIGHT"
            print(f"  Corner at [{idx:3d}]: {abs(angle_deg):5.1f}° {direction}")
        
        if len(self.corner_indices) > 10:
            print(f"  ... and {len(self.corner_indices) - 10} more corners")
        
        print("=" * 60 + "\n")
    
    def run(self):
        """Main loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self._handle_keypress(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event.pos, event.button)
                elif event.type == pygame.MOUSEMOTION:
                    self._handle_mouse_motion(event.pos)
            
            self._draw()
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def _handle_keypress(self, key):
        """Handle keyboard input"""
        if key == pygame.K_ESCAPE or key == pygame.K_q:
            return False
        elif key == pygame.K_n:
            # Cycle to next problem
            if self.problems:
                self.current_problem_index = (self.current_problem_index + 1) % len(self.problems)
                problem = self.problems[self.current_problem_index]
                self.selected_waypoint = problem.index
                print(f"Problem {self.current_problem_index + 1}/{len(self.problems)}: "
                      f"[{problem.index}] {problem.problem_type}")
        elif key == pygame.K_s:
            self._save_screenshot()
        elif key == pygame.K_c:
            self.show_connections = not self.show_connections
        elif key == pygame.K_d:
            self.show_distances = not self.show_distances
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.zoom = min(3.0, self.zoom * 1.2)
        elif key == pygame.K_MINUS:
            self.zoom = max(0.3, self.zoom / 1.2)
        elif key == pygame.K_LEFT:
            self.offset_x += 50
        elif key == pygame.K_RIGHT:
            self.offset_x -= 50
        elif key == pygame.K_UP:
            self.offset_y += 50
        elif key == pygame.K_DOWN:
            self.offset_y -= 50
        elif key == pygame.K_r:
            # Reset view
            self.offset_x = 0
            self.offset_y = 0
            self.zoom = 1.0
        return True
    
    def _handle_mouse_click(self, pos, button):
        """Handle mouse click"""
        if button == 1:  # Left click
            # Find closest waypoint
            closest_idx = self._get_waypoint_at_pos(pos)
            if closest_idx is not None:
                self.selected_waypoint = closest_idx
                self._print_waypoint_info(closest_idx)
    
    def _handle_mouse_motion(self, pos):
        """Handle mouse movement"""
        self.hover_waypoint = self._get_waypoint_at_pos(pos)
    
    def _get_waypoint_at_pos(self, pos):
        """Get waypoint index at screen position"""
        mx, my = pos
        closest_idx = None
        closest_dist = 20  # Max click distance
        
        for i, (wx, wy) in enumerate(self.waypoints):
            sx, sy = self._world_to_screen(wx, wy)
            dist = math.sqrt((mx - sx)**2 + (my - sy)**2)
            if dist < closest_dist:
                closest_dist = dist
                closest_idx = i
        
        return closest_idx
    
    def _world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates"""
        sx = (x + self.offset_x) * self.zoom + SCREEN_WIDTH * 0.3
        sy = (y + self.offset_y) * self.zoom + 50
        return int(sx), int(sy)
    
    def _print_waypoint_info(self, idx):
        """Print detailed info about a waypoint"""
        wx, wy = self.waypoints[idx]
        ox, oy = self.left_boundary[idx]
        ix, iy = self.right_boundary[idx]
        
        outer_dist = math.sqrt((ox - wx)**2 + (oy - wy)**2)
        inner_dist = math.sqrt((ix - wx)**2 + (iy - wy)**2)
        boundary_dist = math.sqrt((ox - ix)**2 + (oy - iy)**2)
        
        prev_i = (idx - 1) % len(self.waypoints)
        next_i = (idx + 1) % len(self.waypoints)
        angle = get_angle_between_segments(
            self.waypoints[prev_i],
            self.waypoints[idx],
            self.waypoints[next_i]
        )
        
        is_corner = idx in self.corner_indices
        is_problem = any(p.index == idx for p in self.problems)
        
        print(f"\n--- Waypoint [{idx}] ---")
        print(f"Position: ({wx}, {wy})")
        print(f"Outer boundary: ({ox:.1f}, {oy:.1f}) - dist: {outer_dist:.1f}px")
        print(f"Inner boundary: ({ix:.1f}, {iy:.1f}) - dist: {inner_dist:.1f}px")
        print(f"Boundary separation: {boundary_dist:.1f}px (expected: {self.track_width * 2}px)")
        print(f"Angle change: {math.degrees(angle):.1f}°")
        print(f"Is corner: {is_corner}")
        print(f"Has problem: {is_problem}")
        
        if is_problem:
            for p in self.problems:
                if p.index == idx:
                    print(f"Problem type: {p.problem_type}")
                    for key, value in p.details.items():
                        print(f"  {key}: {value}")
    
    def _save_screenshot(self):
        """Save screenshot to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"boundary_test_{timestamp}.png"
        filepath = os.path.join("tools", "tracks", filename)
        
        try:
            pygame.image.save(self.screen, filepath)
            print(f"Screenshot saved: {filepath}")
        except Exception as e:
            print(f"Failed to save screenshot: {e}")
    
    def _draw(self):
        """Draw everything"""
        self.screen.fill(COLOR_BG)
        
        # Draw track surface (filled polygon between boundaries)
        self._draw_track_surface()
        
        # Draw connection lines (waypoint to boundaries)
        if self.show_connections:
            self._draw_connections()
        
        # Draw boundaries
        self._draw_boundaries()
        
        # Draw waypoints
        self._draw_waypoints()
        
        # Draw corners
        self._draw_corners()
        
        # Draw problems
        self._draw_problems()
        
        # Draw selected waypoint info
        if self.selected_waypoint is not None:
            self._draw_selected_info()
        
        # Draw UI panel
        self._draw_ui_panel()
        
        pygame.display.flip()
    
    def _draw_track_surface(self):
        """Draw the track surface as filled quads"""
        if len(self.left_boundary) < 3 or len(self.right_boundary) < 3:
            return
        
        num_points = len(self.left_boundary)
        for i in range(num_points):
            next_i = (i + 1) % num_points
            
            o1 = self._world_to_screen(*self.left_boundary[i])
            o2 = self._world_to_screen(*self.left_boundary[next_i])
            i1 = self._world_to_screen(*self.right_boundary[i])
            i2 = self._world_to_screen(*self.right_boundary[next_i])
            
            quad = [o1, o2, i2, i1]
            pygame.draw.polygon(self.screen, COLOR_TRACK, quad)
    
    def _draw_connections(self):
        """Draw lines from waypoints to their boundary points"""
        for i in range(len(self.waypoints)):
            wx, wy = self._world_to_screen(*self.waypoints[i])
            ox, oy = self._world_to_screen(*self.left_boundary[i])
            ix, iy = self._world_to_screen(*self.right_boundary[i])
            
            pygame.draw.line(self.screen, COLOR_CONNECTION, (wx, wy), (ox, oy), 1)
            pygame.draw.line(self.screen, COLOR_CONNECTION, (wx, wy), (ix, iy), 1)
    
    def _draw_boundaries(self):
        """Draw outer and inner boundary points"""
        # Draw boundary lines
        if len(self.left_boundary) >= 2:
            outer_screen = [self._world_to_screen(*p) for p in self.left_boundary]
            pygame.draw.lines(self.screen, COLOR_OUTER, True, outer_screen, 2)
        
        if len(self.right_boundary) >= 2:
            inner_screen = [self._world_to_screen(*p) for p in self.right_boundary]
            pygame.draw.lines(self.screen, COLOR_INNER, True, inner_screen, 2)
        
        # Draw boundary points
        for i, (ox, oy) in enumerate(self.left_boundary):
            sx, sy = self._world_to_screen(ox, oy)
            pygame.draw.circle(self.screen, COLOR_OUTER, (sx, sy), BOUNDARY_RADIUS)
        
        for i, (ix, iy) in enumerate(self.right_boundary):
            sx, sy = self._world_to_screen(ix, iy)
            pygame.draw.circle(self.screen, COLOR_INNER, (sx, sy), BOUNDARY_RADIUS)
    
    def _draw_waypoints(self):
        """Draw racing line waypoints"""
        # Draw racing line
        if len(self.waypoints) >= 2:
            waypoint_screen = [self._world_to_screen(*p) for p in self.waypoints]
            pygame.draw.lines(self.screen, (100, 100, 100), True, waypoint_screen, 1)
        
        # Draw waypoint dots
        for i, (wx, wy) in enumerate(self.waypoints):
            sx, sy = self._world_to_screen(wx, wy)
            
            color = COLOR_WAYPOINT
            radius = WAYPOINT_RADIUS
            
            if i == self.selected_waypoint:
                color = COLOR_SELECTED
                radius = WAYPOINT_RADIUS + 3
            elif i == self.hover_waypoint:
                color = (200, 200, 255)
                radius = WAYPOINT_RADIUS + 2
            
            pygame.draw.circle(self.screen, color, (sx, sy), radius)
            
            # Draw index for selected/hover
            if i == self.selected_waypoint or i == self.hover_waypoint:
                text = self.font_small.render(str(i), True, COLOR_TEXT)
                self.screen.blit(text, (sx + 10, sy - 5))
    
    def _draw_corners(self):
        """Draw corner indicators"""
        for idx in self.corner_indices:
            if idx >= len(self.waypoints):
                continue
            
            wx, wy = self.waypoints[idx]
            sx, sy = self._world_to_screen(wx, wy)
            
            # Draw yellow ring around corner waypoints
            pygame.draw.circle(self.screen, COLOR_CORNER, (sx, sy), CORNER_RADIUS, 2)
    
    def _draw_problems(self):
        """Draw problem indicators"""
        for problem in self.problems:
            idx = problem.index
            if idx >= len(self.waypoints):
                continue
            
            wx, wy = self.waypoints[idx]
            sx, sy = self._world_to_screen(wx, wy)
            
            # Choose color based on problem type
            if problem.problem_type == 'collapsed':
                color = COLOR_COLLAPSED
            elif problem.problem_type == 'wrong_side':
                color = COLOR_PROBLEM
            elif problem.problem_type == 'crossed':
                color = COLOR_CROSSED
            else:
                color = COLOR_PROBLEM
            
            # Draw large ring around problem waypoints
            pygame.draw.circle(self.screen, color, (sx, sy), PROBLEM_RADIUS, 3)
            
            # Draw X marker
            pygame.draw.line(self.screen, color, (sx - 5, sy - 5), (sx + 5, sy + 5), 2)
            pygame.draw.line(self.screen, color, (sx - 5, sy + 5), (sx + 5, sy - 5), 2)
    
    def _draw_selected_info(self):
        """Draw info panel for selected waypoint"""
        idx = self.selected_waypoint
        if idx is None or idx >= len(self.waypoints):
            return
        
        wx, wy = self.waypoints[idx]
        ox, oy = self.left_boundary[idx]
        ix, iy = self.right_boundary[idx]
        
        outer_dist = math.sqrt((ox - wx)**2 + (oy - wy)**2)
        inner_dist = math.sqrt((ix - wx)**2 + (iy - wy)**2)
        
        prev_i = (idx - 1) % len(self.waypoints)
        next_i = (idx + 1) % len(self.waypoints)
        angle = get_angle_between_segments(
            self.waypoints[prev_i],
            self.waypoints[idx],
            self.waypoints[next_i]
        )
        
        # Draw info box
        box_x = 10
        box_y = SCREEN_HEIGHT - 150
        box_w = 250
        box_h = 140
        
        pygame.draw.rect(self.screen, COLOR_PANEL, (box_x, box_y, box_w, box_h))
        pygame.draw.rect(self.screen, COLOR_TEXT_DIM, (box_x, box_y, box_w, box_h), 1)
        
        y = box_y + 10
        lines = [
            f"Waypoint [{idx}]",
            f"Position: ({wx}, {wy})",
            f"Outer dist: {outer_dist:.1f}px",
            f"Inner dist: {inner_dist:.1f}px",
            f"Angle: {math.degrees(angle):.1f}°",
            f"Corner: {'Yes' if idx in self.corner_indices else 'No'}",
        ]
        
        for line in lines:
            text = self.font_small.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (box_x + 10, y))
            y += 20
    
    def _draw_ui_panel(self):
        """Draw UI panel with controls and stats"""
        panel_x = SCREEN_WIDTH - 220
        panel_w = 210
        panel_h = SCREEN_HEIGHT
        
        pygame.draw.rect(self.screen, COLOR_PANEL, (panel_x, 0, panel_w, panel_h))
        
        y = 20
        
        # Title
        title = self.font_title.render("Boundary Test", True, COLOR_TEXT)
        self.screen.blit(title, (panel_x + 10, y))
        y += 50
        
        # Stats
        stats = [
            f"Waypoints: {len(self.waypoints)}",
            f"Corners: {len(self.corner_indices)}",
            f"Problems: {len(self.problems)}",
            f"Track width: {self.track_width}px",
            f"Zoom: {self.zoom:.1f}x",
        ]
        
        for stat in stats:
            text = self.font_small.render(stat, True, COLOR_TEXT_DIM)
            self.screen.blit(text, (panel_x + 10, y))
            y += 22
        
        y += 20
        
        # Problem summary
        if self.problems:
            pygame.draw.line(self.screen, COLOR_TEXT_DIM, 
                           (panel_x + 10, y), (panel_x + panel_w - 10, y), 1)
            y += 10
            
            header = self.font_medium.render("Problems", True, COLOR_PROBLEM)
            self.screen.blit(header, (panel_x + 10, y))
            y += 30
            
            # Count by type
            type_counts = {}
            for p in self.problems:
                type_counts[p.problem_type] = type_counts.get(p.problem_type, 0) + 1
            
            for ptype, count in type_counts.items():
                if ptype == 'collapsed':
                    color = COLOR_COLLAPSED
                elif ptype == 'wrong_side':
                    color = COLOR_PROBLEM
                elif ptype == 'crossed':
                    color = COLOR_CROSSED
                else:
                    color = COLOR_TEXT_DIM
                
                text = self.font_small.render(f"{ptype}: {count}", True, color)
                self.screen.blit(text, (panel_x + 10, y))
                y += 20
        
        y += 20
        
        # Controls
        pygame.draw.line(self.screen, COLOR_TEXT_DIM, 
                        (panel_x + 10, y), (panel_x + panel_w - 10, y), 1)
        y += 10
        
        controls_header = self.font_medium.render("Controls", True, COLOR_TEXT)
        self.screen.blit(controls_header, (panel_x + 10, y))
        y += 30
        
        controls = [
            ("Click", "Select waypoint"),
            ("N", "Next problem"),
            ("S", "Screenshot"),
            ("C", "Toggle connections"),
            ("D", "Toggle distances"),
            ("+/-", "Zoom"),
            ("Arrows", "Pan"),
            ("R", "Reset view"),
            ("Q/Esc", "Quit"),
        ]
        
        for key, action in controls:
            key_text = self.font_small.render(key, True, COLOR_CORNER)
            action_text = self.font_small.render(action, True, COLOR_TEXT_DIM)
            self.screen.blit(key_text, (panel_x + 10, y))
            self.screen.blit(action_text, (panel_x + 60, y))
            y += 18
        
        # Legend
        y += 20
        pygame.draw.line(self.screen, COLOR_TEXT_DIM, 
                        (panel_x + 10, y), (panel_x + panel_w - 10, y), 1)
        y += 10
        
        legend_header = self.font_medium.render("Legend", True, COLOR_TEXT)
        self.screen.blit(legend_header, (panel_x + 10, y))
        y += 30
        
        legend = [
            (COLOR_OUTER, "Left boundary"),
            (COLOR_INNER, "Right boundary"),
            (COLOR_CORNER, "Corner"),
            (COLOR_COLLAPSED, "Collapsed"),
            (COLOR_PROBLEM, "Wrong side"),
            (COLOR_CROSSED, "Crossed"),
        ]
        
        for color, label in legend:
            pygame.draw.circle(self.screen, color, (panel_x + 15, y + 6), 5)
            text = self.font_small.render(label, True, COLOR_TEXT_DIM)
            self.screen.blit(text, (panel_x + 30, y))
            y += 18


def main():
    """Entry point"""
    # Parse command line arguments
    track_file = None
    if len(sys.argv) > 1:
        track_file = sys.argv[1]
    
    # Create and run tester
    tester = TrackBoundaryTester(track_file)
    tester.run()


if __name__ == "__main__":
    main()
