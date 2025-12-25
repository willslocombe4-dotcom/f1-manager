"""
F1 Track Decorator - Create tracks and paint decorations

VISUAL MODE:
    python tools/track_decorator.py [track_file.json]

    Controls:
    - D: Draw mode (place/move waypoints)
    - P: Decorate mode (paint kerbs/gravel)
    - K: Kerb tool (decorate mode)
    - G: Gravel tool (decorate mode)
    - E: Eraser tool (decorate mode)
    - L: Left boundary
    - R: Right boundary
    - T: Set start line at hover segment
    - Left-click + drag: Paint/place
    - Right-click: Erase/delete
    - Z: Undo
    - C: Clear (waypoints in draw mode, decorations in decorate mode)
    - S: Save
    - O: Open track
    - N: Toggle segment numbers
    - Esc: Exit

API MODE (for AI agents):
    from tools.track_decorator import TrackDecorator
    
    # Create new track from scratch
    decorator = TrackDecorator()
    decorator.create_new_track("My Circuit")
    
    # Add waypoints
    decorator.add_waypoint(100, 200)
    decorator.add_waypoint(200, 200)
    decorator.add_waypoint(300, 250)
    # ... add more waypoints to form circuit
    
    # Or load existing track
    decorator = TrackDecorator("existing_track.json")
    
    # Analyze track for decoration suggestions
    analysis = decorator.analyze_segments()
    suggestions = decorator.suggest_decorations()
    
    # Add decorations explicitly
    decorator.add_kerb(boundary="right", start=15, end=18)
    decorator.add_gravel(boundary="left", start=13, end=20)
    decorator.set_start_line(segment=0)
    decorator.set_racing_line(enabled=True)
    
    # Modify waypoints
    decorator.move_waypoint(5, new_x=150, new_y=220)
    decorator.remove_waypoint(10)
    
    # Validate and save
    errors = decorator.validate()
    decorator.save("my_track.json")
"""

import sys
import os
import math
import json
import copy
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if we're being imported or run directly
_HEADLESS_MODE = False

def _init_pygame():
    """Initialize pygame only when needed (not for API-only usage)"""
    global pygame, _HEADLESS_MODE
    try:
        import pygame as pg
        pygame = pg
        return True
    except ImportError:
        _HEADLESS_MODE = True
        return False


# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60

# Track view area
TRACK_VIEW_WIDTH = 950
TRACK_VIEW_HEIGHT = 900

# UI Panel
PANEL_WIDTH = 250
PANEL_X = TRACK_VIEW_WIDTH

# Colors
BG_COLOR = (15, 15, 15)
TRACK_BG_COLOR = (20, 20, 20)
PANEL_BG_COLOR = (25, 25, 25)
TRACK_COLOR = (50, 50, 50)
TRACK_LINE_COLOR = (80, 80, 80)
TEXT_COLOR = (255, 255, 255)
TEXT_DIM_COLOR = (150, 150, 150)
ACCENT_COLOR = (100, 149, 237)

# Boundary colors
LEFT_BOUNDARY_COLOR = (100, 100, 255)   # Blue for left
RIGHT_BOUNDARY_COLOR = (255, 100, 100)  # Red for right

# Decoration colors
KERB_RED = (200, 0, 0)
KERB_WHITE = (255, 255, 255)
GRAVEL_COLOR = (194, 178, 128)
GRAVEL_BORDER_COLOR = (170, 155, 110)

# Tool colors
TOOL_KERB_COLOR = (200, 0, 0)
TOOL_GRAVEL_COLOR = (194, 178, 128)
TOOL_ERASER_COLOR = (255, 100, 100)

# Selection colors
CURSOR_COLOR = (255, 255, 0)  # Yellow for cursor
PREVIEW_ALPHA = 180  # Slight transparency for preview

# Sizes
WAYPOINT_RADIUS = 4
BOUNDARY_RADIUS = 3
TRACK_WIDTH = 35
MAX_SNAP_DISTANCE = 30  # How close mouse must be to boundary to snap


class PaintState:
    """Paint state machine states"""
    IDLE = "idle"
    PAINTING = "painting"
    ERASING = "erasing"


class TrackDecorator:
    """
    Track decoration tool with visual paint mode and API mode.
    
    Visual Mode: Run as script to open pygame window with paint interface
    API Mode: Import and use programmatically (no pygame window)
    """
    
    def __init__(self, track_path=None, waypoints=None):
        """
        Initialize the decorator.
        
        Args:
            track_path: Path to JSON track file (optional)
            waypoints: List of (x, y) tuples (optional, used if no track_path)
        """
        self.track_path = track_path
        self.track_name = "Untitled Track"
        self.waypoints = []
        self.decorations = {
            'kerbs': [],
            'gravel': [],
            'grass': [],           # Grass areas (polygon regions)
            'start_line': None,    # Start/finish line position {'segment': int}
            'racing_line': False,  # Whether to show racing line
        }
        self.undo_stack = []
        
        # Load track if path provided
        if track_path:
            self._load_track(track_path)
        elif waypoints:
            self.waypoints = list(waypoints)
        
        # Calculate boundaries if we have waypoints
        self.left_boundary = []
        self.right_boundary = []
        if self.waypoints:
            self._calculate_boundaries()
        
        # Visual mode state (only used when running as script)
        self._visual_mode = False
        self._pygame_initialized = False
    
    def _load_track(self, filepath):
        """Load track from JSON file"""
        try:
            # Handle relative paths
            if not os.path.isabs(filepath):
                # Try relative to tools/tracks first
                tracks_dir = os.path.join(os.path.dirname(__file__), 'tracks')
                full_path = os.path.join(tracks_dir, filepath)
                if not os.path.exists(full_path):
                    full_path = filepath
            else:
                full_path = filepath
            
            with open(full_path, 'r') as f:
                data = json.load(f)
            
            # Extract waypoints
            self.waypoints = [tuple(wp) for wp in data.get('waypoints', [])]
            
            # Extract existing decorations if present
            if 'decorations' in data:
                self.decorations = data['decorations']
            
            # Extract name
            if 'name' in data:
                self.track_name = data['name']
            else:
                self.track_name = os.path.basename(filepath).replace('.json', '')
            
            self.track_path = full_path
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading track: {e}")
            self.waypoints = []
    
    def _calculate_boundaries(self):
        """Calculate left and right track boundaries"""
        if len(self.waypoints) < 3:
            self.left_boundary = []
            self.right_boundary = []
            return
        
        self.left_boundary = []
        self.right_boundary = []
        
        for i in range(len(self.waypoints)):
            prev_i = (i - 1) % len(self.waypoints)
            next_i = (i + 1) % len(self.waypoints)
            
            p_prev = self.waypoints[prev_i]
            p_curr = self.waypoints[i]
            p_next = self.waypoints[next_i]
            
            # Direction vectors
            dx1 = p_curr[0] - p_prev[0]
            dy1 = p_curr[1] - p_prev[1]
            dx2 = p_next[0] - p_curr[0]
            dy2 = p_next[1] - p_curr[1]
            
            # Normalize
            len1 = math.sqrt(dx1*dx1 + dy1*dy1)
            len2 = math.sqrt(dx2*dx2 + dy2*dy2)
            if len1 > 0:
                dx1, dy1 = dx1/len1, dy1/len1
            if len2 > 0:
                dx2, dy2 = dx2/len2, dy2/len2
            
            # Perpendiculars (pointing LEFT)
            perp1_x, perp1_y = -dy1, dx1
            perp2_x, perp2_y = -dy2, dx2
            
            # Average perpendicular (bevel join)
            avg_x = perp1_x + perp2_x
            avg_y = perp1_y + perp2_y
            avg_len = math.sqrt(avg_x*avg_x + avg_y*avg_y)
            
            if avg_len > 0.001:
                avg_x, avg_y = avg_x/avg_len, avg_y/avg_len
            else:
                avg_x, avg_y = perp1_x, perp1_y
            
            # Offset points
            self.left_boundary.append((
                p_curr[0] + avg_x * TRACK_WIDTH,
                p_curr[1] + avg_y * TRACK_WIDTH
            ))
            self.right_boundary.append((
                p_curr[0] - avg_x * TRACK_WIDTH,
                p_curr[1] - avg_y * TRACK_WIDTH
            ))
    
    # =========================================================================
    # API Methods (for AI agents)
    # =========================================================================
    
    def analyze_segments(self):
        """
        Analyze each segment and return turn information.
        
        Returns:
            dict: Segment index -> {
                'angle_deg': float,      # Angle change in degrees (positive = left turn)
                'turn_direction': str,   # 'left', 'right', or 'straight'
                'apex_side': str,        # 'left' or 'right' (inside of turn)
                'runoff_side': str,      # 'left' or 'right' (outside of turn)
            }
        """
        analysis = {}
        
        for i in range(len(self.waypoints)):
            prev_i = (i - 1) % len(self.waypoints)
            next_i = (i + 1) % len(self.waypoints)
            
            p1 = self.waypoints[prev_i]
            p2 = self.waypoints[i]
            p3 = self.waypoints[next_i]
            
            # Calculate angle change
            angle = self._get_angle_between_segments(p1, p2, p3)
            angle_deg = math.degrees(angle)
            
            # Determine turn direction
            if abs(angle_deg) < 5:
                turn_direction = 'straight'
                apex_side = None
                runoff_side = None
            elif angle_deg > 0:
                turn_direction = 'left'
                apex_side = 'right'   # Apex on inside (right for left turn)
                runoff_side = 'left'  # Runoff on outside
            else:
                turn_direction = 'right'
                apex_side = 'left'    # Apex on inside (left for right turn)
                runoff_side = 'right' # Runoff on outside
            
            analysis[i] = {
                'angle_deg': angle_deg,
                'turn_direction': turn_direction,
                'apex_side': apex_side,
                'runoff_side': runoff_side,
            }
        
        return analysis
    
    def suggest_decorations(self, min_corner_angle=30):
        """
        Suggest kerb and gravel placements based on corner analysis.
        
        Args:
            min_corner_angle: Minimum angle (degrees) to consider as a corner
            
        Returns:
            dict: {
                'kerbs': [{'boundary': str, 'start': int, 'end': int}, ...],
                'gravel': [{'boundary': str, 'start': int, 'end': int}, ...]
            }
        """
        suggestions = {'kerbs': [], 'gravel': []}
        analysis = self.analyze_segments()
        
        # Find corners
        corners = []
        for idx, info in analysis.items():
            if abs(info['angle_deg']) >= min_corner_angle:
                corners.append((idx, info))
        
        # Group consecutive corners
        corner_groups = []
        current_group = []
        
        for idx, info in corners:
            if not current_group:
                current_group = [(idx, info)]
            elif idx - current_group[-1][0] <= 3:  # Within 3 segments
                current_group.append((idx, info))
            else:
                corner_groups.append(current_group)
                current_group = [(idx, info)]
        
        if current_group:
            corner_groups.append(current_group)
        
        # Generate suggestions for each corner group
        for group in corner_groups:
            start_idx = group[0][0]
            end_idx = group[-1][0]
            
            # Extend range slightly
            start_idx = (start_idx - 1) % len(self.waypoints)
            end_idx = (end_idx + 2) % len(self.waypoints)
            
            # Use the dominant turn direction
            left_count = sum(1 for _, info in group if info['turn_direction'] == 'left')
            right_count = sum(1 for _, info in group if info['turn_direction'] == 'right')
            
            if left_count > right_count:
                apex_side = 'right'
                runoff_side = 'left'
            else:
                apex_side = 'left'
                runoff_side = 'right'
            
            # Suggest kerb on apex side
            suggestions['kerbs'].append({
                'boundary': apex_side,
                'start': start_idx,
                'end': end_idx
            })
            
            # Suggest gravel on runoff side
            suggestions['gravel'].append({
                'boundary': runoff_side,
                'start': start_idx,
                'end': end_idx
            })
        
        return suggestions
    
    def add_kerb(self, boundary, start, end):
        """
        Add a kerb decoration.
        
        Args:
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
        """
        self._save_undo_state()
        self.decorations['kerbs'].append({
            'boundary': boundary,
            'start': start,
            'end': end
        })
    
    def add_gravel(self, boundary, start, end):
        """
        Add a gravel trap decoration.
        
        Args:
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
        """
        self._save_undo_state()
        self.decorations['gravel'].append({
            'boundary': boundary,
            'start': start,
            'end': end
        })
    
    def remove_decoration(self, decoration_type, boundary, start):
        """
        Remove a specific decoration.
        
        Args:
            decoration_type: 'kerb' or 'gravel'
            boundary: 'left' or 'right'
            start: Starting segment index
        """
        self._save_undo_state()
        
        key = 'kerbs' if decoration_type == 'kerb' else 'gravel'
        self.decorations[key] = [
            d for d in self.decorations[key]
            if not (d['boundary'] == boundary and d['start'] == start)
        ]
    
    def clear_decorations(self):
        """Remove all decorations (keeps waypoints)"""
        self._save_undo_state()
        self.decorations = {
            'kerbs': [],
            'gravel': [],
            'grass': [],
            'start_line': None,
            'racing_line': False,
        }
    
    def set_start_line(self, segment):
        """
        Set the start/finish line position.
        
        Args:
            segment: Waypoint index for start line
        """
        self._save_undo_state()
        self.decorations['start_line'] = {'segment': segment}
    
    def remove_start_line(self):
        """Remove the start/finish line"""
        self._save_undo_state()
        self.decorations['start_line'] = None
    
    def set_racing_line(self, enabled=True):
        """
        Enable or disable racing line display.
        
        Args:
            enabled: Whether to show racing line
        """
        self._save_undo_state()
        self.decorations['racing_line'] = enabled
    
    def add_waypoint(self, x, y, index=None):
        """
        Add a waypoint to the track.
        
        Args:
            x: X coordinate
            y: Y coordinate
            index: Insert at this index (default: append to end)
        
        Returns:
            int: Index of the new waypoint
        """
        self._save_undo_state()
        
        if index is None:
            self.waypoints.append((int(x), int(y)))
            new_index = len(self.waypoints) - 1
        else:
            self.waypoints.insert(index, (int(x), int(y)))
            new_index = index
        
        self._calculate_boundaries()
        return new_index
    
    def remove_waypoint(self, index):
        """
        Remove a waypoint from the track.
        
        Args:
            index: Index of waypoint to remove
        
        Returns:
            bool: True if removed, False if invalid index
        """
        if index < 0 or index >= len(self.waypoints):
            return False
        
        self._save_undo_state()
        self.waypoints.pop(index)
        self._calculate_boundaries()
        return True
    
    def move_waypoint(self, index, x, y):
        """
        Move a waypoint to a new position.
        
        Args:
            index: Index of waypoint to move
            x: New X coordinate
            y: New Y coordinate
        
        Returns:
            bool: True if moved, False if invalid index
        """
        if index < 0 or index >= len(self.waypoints):
            return False
        
        self._save_undo_state()
        self.waypoints[index] = (int(x), int(y))
        self._calculate_boundaries()
        return True
    
    def clear_waypoints(self):
        """Remove all waypoints"""
        self._save_undo_state()
        self.waypoints = []
        self.left_boundary = []
        self.right_boundary = []
    
    def get_waypoints(self):
        """
        Get all waypoints.
        
        Returns:
            list: List of (x, y) tuples
        """
        return list(self.waypoints)
    
    def create_new_track(self, name="New Track"):
        """
        Start a new empty track.
        
        Args:
            name: Name for the new track
        """
        self._save_undo_state()
        self.track_name = name
        self.track_path = None
        self.waypoints = []
        self.decorations = {
            'kerbs': [],
            'gravel': [],
            'grass': [],
            'start_line': None,
            'racing_line': False,
        }
        self.left_boundary = []
        self.right_boundary = []
    
    def validate(self):
        """
        Validate decorations for errors.
        
        Returns:
            list: List of error strings (empty if valid)
        """
        errors = []
        num_waypoints = len(self.waypoints)
        
        # Check each decoration
        for dtype in ['kerbs', 'gravel']:
            for i, dec in enumerate(self.decorations[dtype]):
                # Check boundary
                if dec['boundary'] not in ['left', 'right']:
                    errors.append(f"{dtype}[{i}]: Invalid boundary '{dec['boundary']}'")
                
                # Check indices
                if dec['start'] < 0 or dec['start'] >= num_waypoints:
                    errors.append(f"{dtype}[{i}]: Invalid start index {dec['start']}")
                if dec['end'] < 0 or dec['end'] >= num_waypoints:
                    errors.append(f"{dtype}[{i}]: Invalid end index {dec['end']}")
        
        # Check for overlapping decorations of same type on same boundary
        for dtype in ['kerbs', 'gravel']:
            for boundary in ['left', 'right']:
                ranges = []
                for dec in self.decorations[dtype]:
                    if dec['boundary'] == boundary:
                        ranges.append((dec['start'], dec['end']))
                
                # Check for overlaps
                for i, (s1, e1) in enumerate(ranges):
                    for j, (s2, e2) in enumerate(ranges):
                        if i < j:
                            if self._ranges_overlap(s1, e1, s2, e2, num_waypoints):
                                errors.append(
                                    f"{dtype}: Overlapping ranges on {boundary} boundary "
                                    f"({s1}-{e1}) and ({s2}-{e2})"
                                )
        
        return errors
    
    def get_decorations(self):
        """
        Get current decorations.
        
        Returns:
            dict: {'kerbs': [...], 'gravel': [...]}
        """
        return self.decorations.copy()
    
    def save(self, filepath=None):
        """
        Save track with decorations to JSON file.
        
        Args:
            filepath: Output path (optional, uses original path if not provided)
        """
        if filepath is None:
            filepath = self.track_path
        
        if filepath is None:
            raise ValueError("No filepath specified and no original track path")
        
        data = {
            'name': self.track_name,
            'waypoints': self.waypoints,
            'decorations': self.decorations,
            'created': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'num_waypoints': len(self.waypoints)
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved: {filepath}")
    
    # =========================================================================
    # Internal helpers
    # =========================================================================
    
    def _get_angle_between_segments(self, p1, p2, p3):
        """Calculate signed angle change at p2 between segments p1->p2 and p2->p3"""
        dx1 = p2[0] - p1[0]
        dy1 = p2[1] - p1[1]
        dx2 = p3[0] - p2[0]
        dy2 = p3[1] - p2[1]
        
        angle1 = math.atan2(dy1, dx1)
        angle2 = math.atan2(dy2, dx2)
        
        diff = angle2 - angle1
        while diff > math.pi:
            diff -= 2 * math.pi
        while diff < -math.pi:
            diff += 2 * math.pi
        
        return diff
    
    def _ranges_overlap(self, s1, e1, s2, e2, num_waypoints):
        """Check if two segment ranges overlap (handling wrap-around)"""
        # Convert to sets of indices
        def get_indices(start, end, n):
            indices = set()
            i = start
            while True:
                indices.add(i)
                if i == end:
                    break
                i = (i + 1) % n
            return indices
        
        set1 = get_indices(s1, e1, num_waypoints)
        set2 = get_indices(s2, e2, num_waypoints)
        
        return bool(set1 & set2)
    
    def _save_undo_state(self):
        """Save current state for undo"""
        state = {
            'decorations': copy.deepcopy(self.decorations),
            'waypoints': copy.deepcopy(self.waypoints),
        }
        self.undo_stack.append(state)
        # Limit undo stack size
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)
    
    def undo(self):
        """Undo last change"""
        if self.undo_stack:
            state = self.undo_stack.pop()
            self.decorations = state['decorations']
            self.waypoints = state['waypoints']
            self._calculate_boundaries()
            return True
        return False
    
    # =========================================================================
    # Visual Mode (pygame) - PAINT MODE
    # =========================================================================
    
    def run_visual(self):
        """Run the visual editor with paint mode (pygame window)"""
        if not _init_pygame():
            print("Error: pygame not available for visual mode")
            return
        
        self._visual_mode = True
        self._pygame_initialized = True
        
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("F1 Track Decorator - Paint Mode")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Mode: 'decorate' or 'draw'
        self.editor_mode = 'decorate'  # 'decorate' = paint decorations, 'draw' = draw waypoints
        
        # Paint state (for decoration mode)
        self.paint_state = PaintState.IDLE
        self.current_tool = 'kerb'      # 'kerb', 'gravel', 'eraser', 'start_line'
        self.current_boundary = 'left'  # 'left', 'right'
        
        # Current stroke (while dragging)
        self.stroke_start_segment = None
        self.stroke_end_segment = None
        
        # Draw mode state
        self.selected_waypoint = None
        self.dragging_waypoint = False
        
        # Visual state
        self.running = True
        self.show_segment_numbers = False
        self.hover_segment = None
        self.message = "Press [D] to draw track, [P] to paint decorations, [O] to load"
        self.message_timer = 0
        
        # View transform
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        
        # Main loop
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
            elif event.type == pygame.MOUSEWHEEL:
                self._handle_scroll(event)
    
    def _handle_keypress(self, event):
        """Handle keyboard input"""
        key = event.key
        mods = pygame.key.get_mods()
        
        if key == pygame.K_ESCAPE:
            self.running = False
        
        # Mode switching
        elif key == pygame.K_d:
            self.editor_mode = 'draw'
            self._show_message("DRAW MODE: Click to place waypoints, drag to move")
        
        elif key == pygame.K_p:
            self.editor_mode = 'decorate'
            self._show_message("DECORATE MODE: Paint kerbs/gravel on boundaries")
        
        # Tool selection (decorate mode)
        elif key == pygame.K_k and self.editor_mode == 'decorate':
            self.current_tool = 'kerb'
            self._show_message("Tool: KERB (red/white stripes)")
        
        elif key == pygame.K_g and self.editor_mode == 'decorate':
            self.current_tool = 'gravel'
            self._show_message("Tool: GRAVEL (tan runoff)")
        
        elif key == pygame.K_e and self.editor_mode == 'decorate':
            self.current_tool = 'eraser'
            self._show_message("Tool: ERASER")
        
        elif key == pygame.K_t and self.editor_mode == 'decorate':
            # Set start line at current hover segment
            if self.hover_segment is not None:
                self._save_undo_state()
                self.decorations['start_line'] = {'segment': self.hover_segment}
                self._show_message(f"Start line set at segment {self.hover_segment}")
            else:
                self._show_message("Hover over a segment first")
        
        # Boundary selection
        elif key == pygame.K_l:
            self.current_boundary = 'left'
            self._show_message("Boundary: LEFT (blue)")
        
        elif key == pygame.K_r:
            self.current_boundary = 'right'
            self._show_message("Boundary: RIGHT (red)")
        
        # Actions
        elif key == pygame.K_z:
            if self.undo():
                self._show_message("Undo")
            else:
                self._show_message("Nothing to undo")
        
        elif key == pygame.K_c:
            if self.editor_mode == 'draw':
                self.clear_waypoints()
                self._show_message("All waypoints cleared")
            else:
                self.clear_decorations()
                self._show_message("All decorations cleared")
        
        elif key == pygame.K_s:
            if self.track_path:
                self.save()
                self._show_message(f"Saved: {os.path.basename(self.track_path)}")
            elif len(self.waypoints) >= 3:
                # New track - open save dialog
                self._save_track_dialog()
            else:
                self._show_message("Need at least 3 waypoints to save")
        
        elif key == pygame.K_o:
            self._load_track_dialog()
        
        elif key == pygame.K_n:
            self.show_segment_numbers = not self.show_segment_numbers
            self._show_message(f"Segment numbers: {'ON' if self.show_segment_numbers else 'OFF'}")
        
        elif key == pygame.K_a:
            # Auto-suggest decorations
            suggestions = self.suggest_decorations()
            for kerb in suggestions['kerbs']:
                self.add_kerb(kerb['boundary'], kerb['start'], kerb['end'])
            for gravel in suggestions['gravel']:
                self.add_gravel(gravel['boundary'], gravel['start'], gravel['end'])
            self._show_message(f"Added {len(suggestions['kerbs'])} kerbs, {len(suggestions['gravel'])} gravel traps")
        
        # Zoom controls
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.zoom = min(3.0, self.zoom * 1.2)
        elif key == pygame.K_MINUS:
            self.zoom = max(0.3, self.zoom / 1.2)
        
        # Pan controls
        elif key == pygame.K_LEFT:
            self.offset_x += 50
        elif key == pygame.K_RIGHT:
            self.offset_x -= 50
        elif key == pygame.K_UP:
            self.offset_y += 50
        elif key == pygame.K_DOWN:
            self.offset_y -= 50
    
    def _handle_mouse_down(self, event):
        """Handle mouse button press"""
        if event.pos[0] >= TRACK_VIEW_WIDTH:
            return  # Click in panel area
        
        if self.editor_mode == 'draw':
            self._handle_draw_mouse_down(event)
        else:
            self._handle_decorate_mouse_down(event)
    
    def _handle_draw_mouse_down(self, event):
        """Handle mouse down in draw mode"""
        mx, my = event.pos
        world_x, world_y = self._screen_to_world(mx, my)
        
        if event.button == 1:  # Left click
            # Check if clicking existing waypoint
            clicked_idx = self._get_waypoint_at_screen_pos(event.pos)
            
            if clicked_idx is not None:
                # Select and start dragging
                self.selected_waypoint = clicked_idx
                self.dragging_waypoint = True
            else:
                # Place new waypoint
                self._save_undo_state()
                self.waypoints.append((int(world_x), int(world_y)))
                self._calculate_boundaries()
                self.selected_waypoint = len(self.waypoints) - 1
                self._show_message(f"Waypoint {len(self.waypoints)} placed")
        
        elif event.button == 3:  # Right click - delete waypoint
            clicked_idx = self._get_waypoint_at_screen_pos(event.pos)
            if clicked_idx is not None:
                self._save_undo_state()
                self.waypoints.pop(clicked_idx)
                self._calculate_boundaries()
                self.selected_waypoint = None
                self._show_message(f"Waypoint deleted ({len(self.waypoints)} remaining)")
    
    def _handle_decorate_mouse_down(self, event):
        """Handle mouse down in decorate mode - start painting"""
        segment = self._get_segment_at_pos(event.pos)
        
        if event.button == 1:  # Left click - paint
            if segment is not None:
                self.paint_state = PaintState.PAINTING
                self.stroke_start_segment = segment
                self.stroke_end_segment = segment
        
        elif event.button == 3:  # Right click - erase
            self.paint_state = PaintState.ERASING
            if segment is not None:
                self._erase_at_segment(segment)
    
    def _handle_mouse_up(self, event):
        """Handle mouse button release"""
        if self.editor_mode == 'draw':
            if event.button == 1:
                self.dragging_waypoint = False
        else:
            if event.button == 1 and self.paint_state == PaintState.PAINTING:
                self._commit_stroke()
                self.paint_state = PaintState.IDLE
            elif event.button == 3:
                self.paint_state = PaintState.IDLE
    
    def _handle_mouse_motion(self, event):
        """Handle mouse movement"""
        if event.pos[0] >= TRACK_VIEW_WIDTH:
            self.hover_segment = None
            return
        
        if self.editor_mode == 'draw':
            self._handle_draw_mouse_motion(event)
        else:
            self._handle_decorate_mouse_motion(event)
    
    def _handle_draw_mouse_motion(self, event):
        """Handle mouse motion in draw mode"""
        # Handle dragging waypoint
        if self.dragging_waypoint and self.selected_waypoint is not None:
            mx, my = event.pos
            world_x, world_y = self._screen_to_world(mx, my)
            self.waypoints[self.selected_waypoint] = (int(world_x), int(world_y))
            self._calculate_boundaries()
    
    def _handle_decorate_mouse_motion(self, event):
        """Handle mouse motion in decorate mode"""
        segment = self._get_segment_at_pos(event.pos)
        self.hover_segment = segment
        
        if self.paint_state == PaintState.PAINTING:
            if segment is not None:
                self.stroke_end_segment = segment
        
        elif self.paint_state == PaintState.ERASING:
            if segment is not None:
                self._erase_at_segment(segment)
    
    def _handle_scroll(self, event):
        """Handle mouse scroll for zoom"""
        if event.y > 0:
            self.zoom = min(3.0, self.zoom * 1.1)
        elif event.y < 0:
            self.zoom = max(0.3, self.zoom / 1.1)
    
    def _get_segment_at_pos(self, pos):
        """
        Find the closest segment on the current boundary to the mouse.
        Returns segment index or None if mouse is too far from boundary.
        """
        mx, my = pos
        
        # Get boundary points
        if self.current_boundary == 'left':
            boundary_points = self.left_boundary
        else:
            boundary_points = self.right_boundary
        
        if not boundary_points:
            return None
        
        # Find closest boundary point
        closest_segment = None
        closest_dist = float('inf')
        
        for i, (bx, by) in enumerate(boundary_points):
            # Convert to screen coordinates
            sx, sy = self._world_to_screen(bx, by)
            dist = math.sqrt((mx - sx)**2 + (my - sy)**2)
            if dist < closest_dist:
                closest_dist = dist
                closest_segment = i
        
        if closest_dist <= MAX_SNAP_DISTANCE:
            return closest_segment
        return None
    
    def _commit_stroke(self):
        """Add the current stroke to decorations"""
        if self.stroke_start_segment is None or self.stroke_end_segment is None:
            return
        
        if self.current_tool == 'eraser':
            # Eraser doesn't commit strokes
            return
        
        start = min(self.stroke_start_segment, self.stroke_end_segment)
        end = max(self.stroke_start_segment, self.stroke_end_segment)
        
        # Only add if there's at least one segment
        if start == end:
            # Single segment - still valid
            pass
        
        if self.current_tool == 'kerb':
            self.add_kerb(self.current_boundary, start, end)
            self._show_message(f"Added kerb: {self.current_boundary} {start}-{end}")
        elif self.current_tool == 'gravel':
            self.add_gravel(self.current_boundary, start, end)
            self._show_message(f"Added gravel: {self.current_boundary} {start}-{end}")
        
        # Reset stroke
        self.stroke_start_segment = None
        self.stroke_end_segment = None
    
    def _erase_at_segment(self, segment):
        """Erase any decoration at the given segment on current boundary"""
        erased = False
        
        for dtype in ['kerbs', 'gravel']:
            for dec in self.decorations[dtype][:]:  # Copy list for safe iteration
                if dec['boundary'] == self.current_boundary:
                    if self._segment_in_range(segment, dec['start'], dec['end']):
                        self.remove_decoration(
                            'kerb' if dtype == 'kerbs' else 'gravel',
                            dec['boundary'],
                            dec['start']
                        )
                        erased = True
                        break
            if erased:
                break
    
    def _segment_in_range(self, segment, start, end):
        """Check if segment is in range (handling wrap-around)"""
        n = len(self.waypoints)
        i = start
        while True:
            if i == segment:
                return True
            if i == end:
                break
            i = (i + 1) % n
        return False
    
    def _world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates"""
        sx = (x + self.offset_x) * self.zoom + 100
        sy = (y + self.offset_y) * self.zoom + 50
        return int(sx), int(sy)
    
    def _screen_to_world(self, sx, sy):
        """Convert screen coordinates to world coordinates"""
        x = (sx - 100) / self.zoom - self.offset_x
        y = (sy - 50) / self.zoom - self.offset_y
        return x, y
    
    def _get_waypoint_at_screen_pos(self, pos):
        """Get index of waypoint at screen position, or None"""
        mx, my = pos
        
        for i, (wx, wy) in enumerate(self.waypoints):
            sx, sy = self._world_to_screen(wx, wy)
            dist = math.sqrt((mx - sx) ** 2 + (my - sy) ** 2)
            if dist <= 15:  # Click radius
                return i
        
        return None
    
    def _load_track_dialog(self):
        """Open file dialog to load track"""
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            
            tracks_dir = os.path.join(os.path.dirname(__file__), 'tracks')
            filepath = filedialog.askopenfilename(
                title="Select Track",
                initialdir=tracks_dir,
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            root.destroy()
            
            if filepath:
                self._load_track(filepath)
                self._calculate_boundaries()
                self._show_message(f"Loaded: {os.path.basename(filepath)}")
        except Exception as e:
            self._show_message(f"Load failed: {e}")
    
    def _save_track_dialog(self):
        """Open file dialog to save new track"""
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            
            tracks_dir = os.path.join(os.path.dirname(__file__), 'tracks')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"track_{timestamp}.json"
            
            filepath = filedialog.asksaveasfilename(
                title="Save Track",
                initialdir=tracks_dir,
                initialfile=default_name,
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            root.destroy()
            
            if filepath:
                self.track_path = filepath
                self.track_name = os.path.basename(filepath).replace('.json', '')
                self.save()
                self._show_message(f"Saved: {os.path.basename(filepath)}")
        except Exception as e:
            self._show_message(f"Save failed: {e}")
    
    def _show_message(self, text):
        """Display a temporary message"""
        self.message = text
        self.message_timer = 180  # 3 seconds at 60 FPS
    
    def _update(self):
        """Update visual state"""
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def _draw(self):
        """Draw everything"""
        self.screen.fill(BG_COLOR)
        
        # Draw track view background
        pygame.draw.rect(self.screen, TRACK_BG_COLOR, (0, 0, TRACK_VIEW_WIDTH, TRACK_VIEW_HEIGHT))
        
        # Draw track
        self._draw_track()
        
        # Draw committed decorations
        self._draw_decorations()
        
        # Draw stroke preview (while painting in decorate mode)
        if self.editor_mode == 'decorate' and self.paint_state == PaintState.PAINTING:
            self._draw_stroke_preview()
        
        # Draw boundaries
        self._draw_boundaries()
        
        # Draw waypoints with segment numbers
        self._draw_waypoints()
        
        # Draw cursor indicator (mode-dependent)
        if self.editor_mode == 'decorate':
            self._draw_cursor()
        else:
            self._draw_draw_mode_cursor()
        
        # Draw UI panel
        self._draw_ui_panel()
        
        pygame.display.flip()
    
    def _draw_track(self):
        """Draw track surface"""
        if len(self.left_boundary) < 3 or len(self.right_boundary) < 3:
            return
        
        # Draw track quads
        num_points = len(self.left_boundary)
        for i in range(num_points):
            next_i = (i + 1) % num_points
            
            l1 = self._world_to_screen(*self.left_boundary[i])
            l2 = self._world_to_screen(*self.left_boundary[next_i])
            r1 = self._world_to_screen(*self.right_boundary[i])
            r2 = self._world_to_screen(*self.right_boundary[next_i])
            
            quad = [l1, l2, r2, r1]
            pygame.draw.polygon(self.screen, TRACK_COLOR, quad)
    
    def _draw_boundaries(self):
        """Draw left and right boundaries with distinct colors"""
        if len(self.left_boundary) < 2:
            return
        
        # Draw left boundary (blue) - thicker if selected
        left_screen = [self._world_to_screen(*p) for p in self.left_boundary]
        left_width = 4 if self.current_boundary == 'left' else 2
        pygame.draw.lines(self.screen, LEFT_BOUNDARY_COLOR, True, left_screen, left_width)
        
        # Draw right boundary (red) - thicker if selected
        right_screen = [self._world_to_screen(*p) for p in self.right_boundary]
        right_width = 4 if self.current_boundary == 'right' else 2
        pygame.draw.lines(self.screen, RIGHT_BOUNDARY_COLOR, True, right_screen, right_width)
    
    def _draw_waypoints(self):
        """Draw waypoints with optional segment numbers"""
        for i, (wx, wy) in enumerate(self.waypoints):
            sx, sy = self._world_to_screen(wx, wy)
            
            # Determine color based on mode and state
            if self.editor_mode == 'draw' and i == self.selected_waypoint:
                color = (100, 255, 100)  # Green for selected in draw mode
                radius = WAYPOINT_RADIUS + 3
            elif i == self.hover_segment:
                color = CURSOR_COLOR
                radius = WAYPOINT_RADIUS + 2
            else:
                color = TEXT_DIM_COLOR
                radius = WAYPOINT_RADIUS
            
            pygame.draw.circle(self.screen, color, (sx, sy), radius)
            
            # Draw segment number if enabled or on hover/selected
            if self.show_segment_numbers or i == self.hover_segment or (self.editor_mode == 'draw' and i == self.selected_waypoint):
                if i % 5 == 0 or i == self.hover_segment or i == self.selected_waypoint:
                    text = self.font_small.render(str(i), True, TEXT_COLOR)
                    self.screen.blit(text, (sx + 8, sy - 5))
    
    def _draw_decorations(self):
        """Draw all committed decorations"""
        # Draw gravel first (behind kerbs)
        for gravel in self.decorations['gravel']:
            self._draw_gravel_decoration(gravel)
        
        # Draw kerbs
        for kerb in self.decorations['kerbs']:
            self._draw_kerb_decoration(kerb)
        
        # Draw start line if set
        if self.decorations.get('start_line'):
            self._draw_start_line_decoration()
    
    def _draw_start_line_decoration(self):
        """Draw the start/finish line"""
        if not self.decorations.get('start_line') or len(self.waypoints) < 2:
            return
        
        segment = self.decorations['start_line'].get('segment', 0)
        idx = segment % len(self.waypoints)
        next_idx = (idx + 1) % len(self.waypoints)
        
        wx1, wy1 = self.waypoints[idx]
        wx2, wy2 = self.waypoints[next_idx]
        
        # Get perpendicular direction
        dx = wx2 - wx1
        dy = wy2 - wy1
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return
        
        perp_x = -dy / length
        perp_y = dx / length
        
        # Draw checkered pattern
        num_squares = 8
        square_width = (TRACK_WIDTH * 2) / num_squares
        
        for i in range(num_squares):
            t = (i - num_squares / 2) * square_width
            sx1 = wx1 + perp_x * t
            sy1 = wy1 + perp_y * t
            sx2 = sx1 + perp_x * square_width
            sy2 = sy1 + perp_y * square_width
            
            color = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)
            
            p1 = self._world_to_screen(sx1, sy1)
            p2 = self._world_to_screen(sx2, sy2)
            pygame.draw.line(self.screen, color, p1, p2, 6)
    
    def _draw_stroke_preview(self):
        """Draw the decoration being painted (not yet committed)"""
        if self.stroke_start_segment is None or self.stroke_end_segment is None:
            return
        
        if self.current_tool == 'eraser':
            return
        
        start = min(self.stroke_start_segment, self.stroke_end_segment)
        end = max(self.stroke_start_segment, self.stroke_end_segment)
        
        if self.current_tool == 'kerb':
            self._draw_kerb_range_preview(self.current_boundary, start, end)
        elif self.current_tool == 'gravel':
            self._draw_gravel_range_preview(self.current_boundary, start, end)
    
    def _draw_kerb_decoration(self, kerb):
        """Draw a kerb decoration"""
        boundary = self.left_boundary if kerb['boundary'] == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        start = kerb['start']
        end = kerb['end']
        
        # Draw alternating red/white stripes
        stripe_count = 0
        i = start
        while True:
            next_i = (i + 1) % len(self.waypoints)
            
            if i < len(boundary) and next_i < len(boundary):
                p1 = self._world_to_screen(*boundary[i])
                p2 = self._world_to_screen(*boundary[next_i])
                
                color = KERB_RED if stripe_count % 2 == 0 else KERB_WHITE
                pygame.draw.line(self.screen, color, p1, p2, 6)
                stripe_count += 1
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
    
    def _draw_kerb_range_preview(self, boundary_name, start, end):
        """Draw kerb stripes for preview (same as final, with slight visual difference)"""
        boundary = self.left_boundary if boundary_name == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        # Draw alternating red/white stripes with outline to show it's a preview
        stripe_count = 0
        i = start
        while True:
            next_i = (i + 1) % len(self.waypoints)
            
            if i < len(boundary) and next_i < len(boundary):
                p1 = self._world_to_screen(*boundary[i])
                p2 = self._world_to_screen(*boundary[next_i])
                
                # Draw outline first (yellow to show preview)
                pygame.draw.line(self.screen, CURSOR_COLOR, p1, p2, 8)
                
                color = KERB_RED if stripe_count % 2 == 0 else KERB_WHITE
                pygame.draw.line(self.screen, color, p1, p2, 6)
                stripe_count += 1
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
    
    def _draw_gravel_decoration(self, gravel):
        """Draw a gravel trap decoration"""
        boundary = self.left_boundary if gravel['boundary'] == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        start = gravel['start']
        end = gravel['end']
        
        # Collect boundary points and extended points
        inner_points = []
        outer_points = []
        
        i = start
        while True:
            if i < len(boundary) and i < len(self.waypoints):
                bx, by = boundary[i]
                wx, wy = self.waypoints[i]
                
                # Direction from waypoint to boundary
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    inner_points.append(self._world_to_screen(bx, by))
                    
                    # Extend 25 pixels beyond boundary
                    extension = 25
                    gx = bx + (dx / length) * extension
                    gy = by + (dy / length) * extension
                    outer_points.append(self._world_to_screen(gx, gy))
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        if len(outer_points) >= 3 and len(inner_points) >= 3:
            # Create polygon: outer forward, inner backward
            polygon = outer_points + inner_points[::-1]
            pygame.draw.polygon(self.screen, GRAVEL_COLOR, polygon)
            pygame.draw.lines(self.screen, GRAVEL_BORDER_COLOR, False, outer_points, 2)
    
    def _draw_gravel_range_preview(self, boundary_name, start, end):
        """Draw gravel strip for preview (with outline to show it's a preview)"""
        boundary = self.left_boundary if boundary_name == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        # Collect boundary points and extended points
        inner_points = []
        outer_points = []
        
        i = start
        while True:
            if i < len(boundary) and i < len(self.waypoints):
                bx, by = boundary[i]
                wx, wy = self.waypoints[i]
                
                # Direction from waypoint to boundary
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    inner_points.append(self._world_to_screen(bx, by))
                    
                    # Extend 25 pixels beyond boundary
                    extension = 25
                    gx = bx + (dx / length) * extension
                    gy = by + (dy / length) * extension
                    outer_points.append(self._world_to_screen(gx, gy))
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        if len(outer_points) >= 3 and len(inner_points) >= 3:
            # Create polygon: outer forward, inner backward
            polygon = outer_points + inner_points[::-1]
            pygame.draw.polygon(self.screen, GRAVEL_COLOR, polygon)
            # Yellow outline to show preview
            pygame.draw.lines(self.screen, CURSOR_COLOR, True, polygon, 2)
    
    def _draw_cursor(self):
        """Draw cursor indicator on the boundary"""
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_pos[0] >= TRACK_VIEW_WIDTH:
            return
        
        segment = self._get_segment_at_pos(mouse_pos)
        
        if segment is not None:
            # Get boundary point for this segment
            if self.current_boundary == 'left':
                if segment < len(self.left_boundary):
                    bx, by = self.left_boundary[segment]
                else:
                    return
            else:
                if segment < len(self.right_boundary):
                    bx, by = self.right_boundary[segment]
                else:
                    return
            
            sx, sy = self._world_to_screen(bx, by)
            
            # Draw cursor circle with tool color
            if self.current_tool == 'kerb':
                color = TOOL_KERB_COLOR
            elif self.current_tool == 'gravel':
                color = TOOL_GRAVEL_COLOR
            else:
                color = TOOL_ERASER_COLOR
            
            pygame.draw.circle(self.screen, color, (sx, sy), 10, 3)
            pygame.draw.circle(self.screen, CURSOR_COLOR, (sx, sy), 12, 2)
    
    def _draw_draw_mode_cursor(self):
        """Draw cursor for draw mode (waypoint placement)"""
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_pos[0] >= TRACK_VIEW_WIDTH:
            return
        
        mx, my = mouse_pos
        
        # Check if hovering over existing waypoint
        hovered_wp = self._get_waypoint_at_screen_pos(mouse_pos)
        
        if hovered_wp is not None:
            # Show selection cursor
            wx, wy = self.waypoints[hovered_wp]
            sx, sy = self._world_to_screen(wx, wy)
            pygame.draw.circle(self.screen, CURSOR_COLOR, (sx, sy), 12, 2)
        else:
            # Show placement cursor
            pygame.draw.circle(self.screen, (100, 255, 100), (mx, my), 8, 2)
            pygame.draw.line(self.screen, (100, 255, 100), (mx - 12, my), (mx + 12, my), 1)
            pygame.draw.line(self.screen, (100, 255, 100), (mx, my - 12), (mx, my + 12), 1)
    
    def _draw_ui_panel(self):
        """Draw UI panel"""
        # Background
        pygame.draw.rect(self.screen, PANEL_BG_COLOR, (PANEL_X, 0, PANEL_WIDTH, SCREEN_HEIGHT))
        
        y = 20
        
        # Title with mode indicator
        title = self.font_large.render("Track Decorator", True, TEXT_COLOR)
        self.screen.blit(title, (PANEL_X + 10, y))
        y += 35
        
        # Editor mode indicator (DRAW or DECORATE)
        if self.editor_mode == 'draw':
            editor_mode_text = "[DRAW MODE]"
            editor_mode_color = (100, 255, 100)  # Green
        else:
            editor_mode_text = "[DECORATE MODE]"
            editor_mode_color = ACCENT_COLOR
        editor_mode_surf = self.font_medium.render(editor_mode_text, True, editor_mode_color)
        self.screen.blit(editor_mode_surf, (PANEL_X + 10, y))
        y += 25
        
        # Tool indicator (only in decorate mode)
        if self.editor_mode == 'decorate':
            mode_text = f"Tool: {self.current_tool.upper()}"
            if self.current_tool == 'kerb':
                mode_color = TOOL_KERB_COLOR
            elif self.current_tool == 'gravel':
                mode_color = TOOL_GRAVEL_COLOR
            else:
                mode_color = TOOL_ERASER_COLOR
            mode_surf = self.font_small.render(mode_text, True, mode_color)
            self.screen.blit(mode_surf, (PANEL_X + 10, y))
            y += 20
        
        # Track info
        if self.track_path:
            name = os.path.basename(self.track_path)
            if len(name) > 20:
                name = name[:17] + "..."
            text = self.font_small.render(f"Track: {name}", True, TEXT_DIM_COLOR)
            self.screen.blit(text, (PANEL_X + 10, y))
            y += 20
        
        text = self.font_small.render(f"Waypoints: {len(self.waypoints)}", True, TEXT_DIM_COLOR)
        self.screen.blit(text, (PANEL_X + 10, y))
        y += 20
        
        text = self.font_small.render(f"Kerbs: {len(self.decorations['kerbs'])}", True, TEXT_DIM_COLOR)
        self.screen.blit(text, (PANEL_X + 10, y))
        y += 20
        
        text = self.font_small.render(f"Gravel: {len(self.decorations['gravel'])}", True, TEXT_DIM_COLOR)
        self.screen.blit(text, (PANEL_X + 10, y))
        y += 30
        
        # Tools section
        pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15
        
        tools_title = self.font_medium.render("TOOLS", True, TEXT_COLOR)
        self.screen.blit(tools_title, (PANEL_X + 10, y))
        y += 25
        
        # Tool buttons
        tools = [
            ('K', 'Kerb', 'kerb', TOOL_KERB_COLOR),
            ('G', 'Gravel', 'gravel', TOOL_GRAVEL_COLOR),
            ('E', 'Eraser', 'eraser', TOOL_ERASER_COLOR),
        ]
        
        for key, name, tool_id, color in tools:
            is_active = self.current_tool == tool_id
            
            # Draw indicator
            if is_active:
                pygame.draw.rect(self.screen, color, (PANEL_X + 10, y, 15, 15))
            else:
                pygame.draw.rect(self.screen, color, (PANEL_X + 10, y, 15, 15), 1)
            
            key_text = self.font_small.render(f"[{key}]", True, ACCENT_COLOR if is_active else TEXT_DIM_COLOR)
            name_text = self.font_small.render(name, True, TEXT_COLOR if is_active else TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 30, y))
            self.screen.blit(name_text, (PANEL_X + 60, y))
            y += 22
        
        y += 10
        
        # Boundary section
        pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15
        
        boundary_title = self.font_medium.render("BOUNDARY", True, TEXT_COLOR)
        self.screen.blit(boundary_title, (PANEL_X + 10, y))
        y += 25
        
        boundaries = [
            ('L', 'Left', 'left', LEFT_BOUNDARY_COLOR),
            ('R', 'Right', 'right', RIGHT_BOUNDARY_COLOR),
        ]
        
        for key, name, boundary_id, color in boundaries:
            is_active = self.current_boundary == boundary_id
            
            # Draw indicator
            if is_active:
                pygame.draw.rect(self.screen, color, (PANEL_X + 10, y, 15, 15))
            else:
                pygame.draw.rect(self.screen, color, (PANEL_X + 10, y, 15, 15), 1)
            
            key_text = self.font_small.render(f"[{key}]", True, ACCENT_COLOR if is_active else TEXT_DIM_COLOR)
            name_text = self.font_small.render(name, True, TEXT_COLOR if is_active else TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 30, y))
            self.screen.blit(name_text, (PANEL_X + 60, y))
            y += 22
        
        y += 10
        
        # Actions section
        pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15
        
        actions_title = self.font_medium.render("ACTIONS", True, TEXT_COLOR)
        self.screen.blit(actions_title, (PANEL_X + 10, y))
        y += 25
        
        actions = [
            ('D', 'Draw mode'),
            ('P', 'Decorate mode'),
            ('T', 'Set start line'),
            ('Z', 'Undo'),
            ('C', 'Clear all'),
            ('S', 'Save'),
            ('O', 'Open track'),
            ('A', 'Auto-suggest'),
            ('N', 'Toggle numbers'),
        ]
        
        for key, action in actions:
            key_text = self.font_small.render(f"[{key}]", True, ACCENT_COLOR)
            action_text = self.font_small.render(action, True, TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 10, y))
            self.screen.blit(action_text, (PANEL_X + 45, y))
            y += 18
        
        y += 10
        
        # Navigation section
        pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15
        
        nav_title = self.font_medium.render("NAVIGATION", True, TEXT_COLOR)
        self.screen.blit(nav_title, (PANEL_X + 10, y))
        y += 25
        
        nav_controls = [
            ('+/-', 'Zoom'),
            ('Scroll', 'Zoom'),
            ('Arrows', 'Pan'),
            ('Esc', 'Exit'),
        ]
        
        for key, action in nav_controls:
            key_text = self.font_small.render(key, True, ACCENT_COLOR)
            action_text = self.font_small.render(action, True, TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 10, y))
            self.screen.blit(action_text, (PANEL_X + 70, y))
            y += 18
        
        # Hover segment info
        if self.hover_segment is not None:
            y = SCREEN_HEIGHT - 120
            pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
            y += 10
            text = self.font_medium.render(f"Segment: {self.hover_segment}", True, CURSOR_COLOR)
            self.screen.blit(text, (PANEL_X + 10, y))
        
        # Message at bottom
        if self.message_timer > 0:
            msg_y = SCREEN_HEIGHT - 60
            pygame.draw.rect(self.screen, (40, 40, 40), (PANEL_X, msg_y, PANEL_WIDTH, 50))
            
            # Word wrap
            words = self.message.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_text = ' '.join(current_line)
                if self.font_small.size(test_text)[0] > PANEL_WIDTH - 20:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            for i, line in enumerate(lines[:2]):
                text = self.font_small.render(line, True, TEXT_COLOR)
                self.screen.blit(text, (PANEL_X + 10, msg_y + 10 + i * 18))
        
        # Instructions at very bottom
        inst_y = SCREEN_HEIGHT - 25
        inst_text = self.font_small.render("Left-drag: Paint | Right-drag: Erase", True, TEXT_DIM_COLOR)
        self.screen.blit(inst_text, (PANEL_X + 10, inst_y))


def main():
    """Entry point for visual mode"""
    import sys
    
    # Check for track file argument
    track_path = None
    if len(sys.argv) > 1:
        track_path = sys.argv[1]
    
    # Create decorator and run visual mode
    decorator = TrackDecorator(track_path)
    decorator.run_visual()


if __name__ == "__main__":
    main()
