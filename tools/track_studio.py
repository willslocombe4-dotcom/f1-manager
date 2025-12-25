"""
F1 Track Studio - Visual track creation tool

Create F1 circuits by generating from templates or drawing from scratch,
then paint decorations manually.

Usage:
    python tools/track_studio.py

Modes:
    [1] Generate mode - Browse and apply templates (Monaco, Silverstone, etc.)
    [2] Draw mode - Place waypoints manually  
    [3] Decorate mode - Paint kerbs, gravel, and grass on boundaries

Controls:
    1/2/3       Switch modes
    B           Browse templates (Generate mode)
    Enter       Apply template (Generate mode)
    V           Generate variation (Generate mode)
    K           Kerb tool (Decorate mode)
    G           Gravel tool (Decorate mode)
    F           Grass tool (Decorate mode)
    E           Eraser tool (Decorate mode)
    L           Left boundary
    R           Right boundary
    T           Set start line at hover segment
    S           Save track
    O           Open/load track
    Z           Undo
    C           Clear (waypoints in Draw, decorations in Decorate)
    N           Toggle segment numbers
    Esc         Exit
"""

import sys
import os
import math
import json
import copy
import random
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame


# =============================================================================
# CONSTANTS
# =============================================================================

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
GRASS_COLOR = (34, 139, 34)  # Forest green
GRASS_LIGHT_COLOR = (50, 160, 50)  # Lighter green for variety

# Tool colors
TOOL_KERB_COLOR = (200, 0, 0)
TOOL_GRAVEL_COLOR = (194, 178, 128)
TOOL_GRASS_COLOR = (34, 139, 34)
TOOL_ERASER_COLOR = (255, 100, 100)

# Selection colors
CURSOR_COLOR = (255, 255, 0)  # Yellow for cursor
PREVIEW_ALPHA = 180

# Sizes
WAYPOINT_RADIUS = 4
BOUNDARY_RADIUS = 3
TRACK_WIDTH = 35
MAX_SNAP_DISTANCE = 30


# =============================================================================
# TRACK TEMPLATES (from track_generator.py)
# =============================================================================

TEMPLATES = {
    'monaco': {
        'name': 'Monaco',
        'description': 'Tight and twisty street circuit',
        'points': [
            (0.3, 0.1), (0.6, 0.1), (0.8, 0.2),
            (0.9, 0.35), (0.75, 0.4), (0.85, 0.55),
            (0.7, 0.6), (0.55, 0.5), (0.5, 0.65),
            (0.6, 0.8), (0.45, 0.9), (0.25, 0.85),
            (0.15, 0.7), (0.25, 0.55), (0.1, 0.4),
            (0.15, 0.25), (0.25, 0.15),
        ],
    },
    'silverstone': {
        'name': 'Silverstone',
        'description': 'Fast and flowing British circuit',
        'points': [
            (0.4, 0.1), (0.65, 0.12), (0.85, 0.2),
            (0.92, 0.35), (0.85, 0.5), (0.7, 0.45),
            (0.6, 0.55), (0.7, 0.7), (0.6, 0.85),
            (0.4, 0.9), (0.2, 0.8), (0.12, 0.6),
            (0.2, 0.45), (0.15, 0.3), (0.25, 0.18),
        ],
    },
    'monza': {
        'name': 'Monza',
        'description': 'Long straights with chicanes',
        'points': [
            (0.5, 0.1), (0.75, 0.1), (0.9, 0.15),
            (0.95, 0.3), (0.85, 0.4), (0.9, 0.5),
            (0.85, 0.6), (0.7, 0.55), (0.6, 0.65),
            (0.7, 0.8), (0.6, 0.9), (0.4, 0.9),
            (0.2, 0.85), (0.1, 0.7), (0.1, 0.5),
            (0.15, 0.3), (0.3, 0.15),
        ],
    },
    'spa': {
        'name': 'Spa-Francorchamps',
        'description': 'Flowing with elevation changes',
        'points': [
            (0.2, 0.15), (0.45, 0.1), (0.7, 0.15),
            (0.85, 0.25), (0.9, 0.45), (0.8, 0.6),
            (0.65, 0.5), (0.55, 0.6), (0.6, 0.75),
            (0.5, 0.9), (0.3, 0.85), (0.15, 0.7),
            (0.1, 0.5), (0.15, 0.35), (0.1, 0.2),
        ],
    },
    'suzuka': {
        'name': 'Suzuka',
        'description': 'Figure-8 inspired layout',
        'points': [
            (0.5, 0.1), (0.7, 0.15), (0.85, 0.3),
            (0.75, 0.45), (0.6, 0.4), (0.5, 0.5),
            (0.65, 0.6), (0.8, 0.7), (0.75, 0.85),
            (0.55, 0.9), (0.35, 0.8), (0.25, 0.65),
            (0.35, 0.5), (0.25, 0.35), (0.15, 0.25),
            (0.25, 0.12), (0.4, 0.08),
        ],
    },
    'bahrain': {
        'name': 'Bahrain',
        'description': 'Classic F1 layout with technical sections',
        'points': [
            (0.8, 0.15), (0.95, 0.25), (0.95, 0.45),
            (0.85, 0.55), (0.7, 0.5), (0.6, 0.55),
            (0.5, 0.7), (0.55, 0.85), (0.7, 0.9),
            (0.5, 0.95), (0.3, 0.85), (0.2, 0.7),
            (0.1, 0.5), (0.15, 0.3), (0.3, 0.2),
            (0.5, 0.15), (0.65, 0.1),
        ],
    },
}


# =============================================================================
# PAINT STATE
# =============================================================================

class PaintState:
    """Paint state machine states"""
    IDLE = "idle"
    PAINTING = "painting"
    ERASING = "erasing"


class EditorMode:
    """Editor mode constants"""
    GENERATE = "generate"
    DRAW = "draw"
    DECORATE = "decorate"


# =============================================================================
# TRACK STUDIO CLASS
# =============================================================================

class TrackStudio:
    """Visual track creation studio with generation, drawing, and decoration."""
    
    def __init__(self, track_path=None):
        """
        Initialize the studio.
        
        Args:
            track_path: Path to JSON track file to load (optional)
        """
        self.track_path = track_path
        self.track_name = "Untitled Track"
        self.waypoints = []
        self.decorations = {
            'kerbs': [],
            'gravel': [],
            'grass': [],
            'start_line': None,
            'racing_line': False,
        }
        self.undo_stack = []
        
        # Canvas dimensions
        self.canvas_width = 1000
        self.canvas_height = 900
        self.margin = 80
        
        # Load track if path provided
        if track_path:
            self.load(track_path)
        
        # Calculate boundaries if we have waypoints
        self.left_boundary = []
        self.right_boundary = []
        if self.waypoints:
            self._calculate_boundaries()
    
    # =========================================================================
    # TEMPLATE METHODS
    # =========================================================================
    
    def _scan_templates_folder(self):
        """
        Scan the templates folder for JSON files.
        
        Returns:
            list: List of template file paths
        """
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(templates_dir, exist_ok=True)
        
        templates = []
        if os.path.exists(templates_dir):
            for filename in sorted(os.listdir(templates_dir)):
                if filename.endswith('.json'):
                    filepath = os.path.join(templates_dir, filename)
                    templates.append(filepath)
        
        return templates
    
    def _load_template_info(self, filepath):
        """
        Load basic info from a template file without loading full waypoints.
        
        Returns:
            dict: {'name': str, 'style': str, 'num_waypoints': int, 'filepath': str}
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return {
                'name': data.get('name', os.path.basename(filepath)),
                'style': data.get('style', 'unknown'),
                'num_waypoints': data.get('num_waypoints', len(data.get('waypoints', []))),
                'filepath': filepath
            }
        except:
            return None
    
    def list_templates(self):
        """
        List available track templates from templates folder.
        
        Returns:
            list: Template file paths
        """
        return self._scan_templates_folder()
    
    def get_template_info(self, filepath):
        """
        Get information about a template.
        
        Args:
            filepath: Path to template file
            
        Returns:
            dict: {'name': str, 'style': str, 'num_waypoints': int} or None
        """
        return self._load_template_info(filepath)
    
    def load_template_file(self, filepath):
        """
        Load a template from the templates folder.
        
        Args:
            filepath: Path to template JSON file
        """
        self._save_undo_state()
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load waypoints
        self.waypoints = [tuple(wp) for wp in data.get('waypoints', [])]
        
        # Load decorations if present
        if 'decorations' in data:
            self.decorations = data['decorations']
        else:
            self.decorations = {
                'kerbs': [],
                'gravel': [],
                'grass': [],
                'start_line': None,
                'racing_line': False,
            }
        
        # Set name
        self.track_name = data.get('name', os.path.basename(filepath).replace('.json', ''))
        
        # Recalculate boundaries
        self._calculate_boundaries()
    
    def generate_from_template(self, template_name, variation=False, 
                                scale=1.0, rotation=0, mirror=False, smoothing=0.5):
        """
        Generate track from a hardcoded template (legacy method).
        
        Args:
            template_name: Template identifier ('monaco', 'silverstone', etc.)
            variation: Apply random variations to template
            scale: Size multiplier (default 1.0)
            rotation: Rotate degrees (default 0)
            mirror: Mirror horizontally (default False)
            smoothing: Curve smoothing 0-1 (default 0.5)
        
        Returns:
            list: Generated waypoints
        """
        template_name = template_name.lower()
        
        if template_name not in TEMPLATES:
            available = ", ".join(TEMPLATES.keys())
            raise ValueError(f"Unknown template: {template_name}. Available: {available}")
        
        self._save_undo_state()
        
        template = TEMPLATES[template_name]
        points = list(template['points'])
        
        # Apply variation
        if variation:
            points = self._apply_variation(points)
        
        # Apply mirror
        if mirror:
            points = [(1.0 - x, y) for x, y in points]
        
        # Apply rotation
        if rotation != 0:
            points = self._rotate_points(points, rotation)
        
        # Convert to canvas coordinates
        control_points = []
        for tx, ty in points:
            # Scale to canvas
            x = self.margin + tx * (self.canvas_width - 2 * self.margin)
            y = self.margin + ty * (self.canvas_height - 2 * self.margin)
            control_points.append((x, y))
        
        # Apply scale
        if scale != 1.0:
            control_points = self._scale_points(control_points, scale)
        
        # Generate smooth curve
        samples = max(3, int(4 + smoothing * 4))  # 3-8 samples per segment
        self.waypoints = self._catmull_rom_spline(control_points, samples)
        
        # Scale to fit canvas
        self.waypoints = self._scale_to_canvas(self.waypoints)
        
        # Update track name
        self.track_name = f"{template['name']} {datetime.now().strftime('%H%M%S')}"
        
        # Recalculate boundaries
        self._calculate_boundaries()
        
        return self.waypoints
    
    def _apply_variation(self, points, amount=0.08):
        """Apply random variation to template points"""
        varied = []
        for tx, ty in points:
            x = tx + random.uniform(-amount, amount)
            y = ty + random.uniform(-amount, amount)
            x = max(0.1, min(0.9, x))
            y = max(0.1, min(0.9, y))
            varied.append((x, y))
        return varied
    
    def _rotate_points(self, points, degrees):
        """Rotate points around center"""
        radians = math.radians(degrees)
        cos_a = math.cos(radians)
        sin_a = math.sin(radians)
        
        # Find center
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
        
        rotated = []
        for x, y in points:
            # Translate to origin
            dx = x - cx
            dy = y - cy
            # Rotate
            rx = dx * cos_a - dy * sin_a
            ry = dx * sin_a + dy * cos_a
            # Translate back
            rotated.append((rx + cx, ry + cy))
        
        return rotated
    
    def _scale_points(self, points, scale):
        """Scale points around center"""
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
        
        scaled = []
        for x, y in points:
            dx = (x - cx) * scale
            dy = (y - cy) * scale
            scaled.append((cx + dx, cy + dy))
        
        return scaled
    
    def _catmull_rom_spline(self, points, samples_per_segment=4):
        """Generate smooth curve through points using Catmull-Rom spline"""
        if len(points) < 4:
            return points
        
        result = []
        n = len(points)
        
        for i in range(n):
            p0 = points[(i - 1) % n]
            p1 = points[i]
            p2 = points[(i + 1) % n]
            p3 = points[(i + 2) % n]
            
            for t_idx in range(samples_per_segment):
                t = t_idx / samples_per_segment
                t2 = t * t
                t3 = t2 * t
                
                x = 0.5 * (
                    (2 * p1[0]) +
                    (-p0[0] + p2[0]) * t +
                    (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
                    (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3
                )
                
                y = 0.5 * (
                    (2 * p1[1]) +
                    (-p0[1] + p2[1]) * t +
                    (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
                    (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3
                )
                
                result.append((x, y))
        
        return result
    
    def _scale_to_canvas(self, waypoints):
        """Scale waypoints to fit within canvas with margin"""
        if not waypoints:
            return waypoints
        
        xs = [p[0] for p in waypoints]
        ys = [p[1] for p in waypoints]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        width = max_x - min_x
        height = max_y - min_y
        
        if width == 0 or height == 0:
            return waypoints
        
        available_width = self.canvas_width - 2 * self.margin
        available_height = self.canvas_height - 2 * self.margin
        
        scale = min(available_width / width, available_height / height)
        
        scaled_width = width * scale
        scaled_height = height * scale
        
        offset_x = (self.canvas_width - scaled_width) / 2
        offset_y = (self.canvas_height - scaled_height) / 2
        
        result = []
        for x, y in waypoints:
            new_x = (x - min_x) * scale + offset_x
            new_y = (y - min_y) * scale + offset_y
            result.append((int(new_x), int(new_y)))
        
        return result
    
    # =========================================================================
    # DRAWING METHODS
    # =========================================================================
    
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
    
    # =========================================================================
    # DECORATION METHODS
    # =========================================================================
    
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
    
    def add_grass(self, boundary, start, end):
        """
        Add a grass area decoration.
        
        Args:
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
        """
        self._save_undo_state()
        self.decorations['grass'].append({
            'boundary': boundary,
            'start': start,
            'end': end
        })
    
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
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def validate(self):
        """
        Validate track for errors.
        
        Returns:
            list: List of error strings (empty if valid)
        """
        errors = []
        num_waypoints = len(self.waypoints)
        
        if num_waypoints < 3:
            errors.append("Track needs at least 3 waypoints")
            return errors
        
        for dtype in ['kerbs', 'gravel']:
            for i, dec in enumerate(self.decorations[dtype]):
                if dec['boundary'] not in ['left', 'right']:
                    errors.append(f"{dtype}[{i}]: Invalid boundary '{dec['boundary']}'")
                
                if dec['start'] < 0 or dec['start'] >= num_waypoints:
                    errors.append(f"{dtype}[{i}]: Invalid start index {dec['start']}")
                if dec['end'] < 0 or dec['end'] >= num_waypoints:
                    errors.append(f"{dtype}[{i}]: Invalid end index {dec['end']}")
        
        return errors
    
    def undo(self):
        """Undo last change"""
        if self.undo_stack:
            state = self.undo_stack.pop()
            self.decorations = state['decorations']
            self.waypoints = state['waypoints']
            self._calculate_boundaries()
            return True
        return False
    
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
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        
        data = {
            'name': self.track_name,
            'waypoints': self.waypoints,
            'decorations': self.decorations,
            'created': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'num_waypoints': len(self.waypoints),
            'generated_by': 'track_studio'
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.track_path = filepath
        print(f"Saved: {filepath}")
    
    def load(self, filepath):
        """
        Load track from JSON file.
        
        Args:
            filepath: Path to JSON file
        """
        # Handle relative paths
        if not os.path.isabs(filepath):
            tracks_dir = os.path.join(os.path.dirname(__file__), 'tracks')
            full_path = os.path.join(tracks_dir, filepath)
            if not os.path.exists(full_path):
                full_path = filepath
        else:
            full_path = filepath
        
        with open(full_path, 'r') as f:
            data = json.load(f)
        
        self.waypoints = [tuple(wp) for wp in data.get('waypoints', [])]
        
        if 'decorations' in data:
            self.decorations = data['decorations']
        else:
            self.decorations = {
                'kerbs': [],
                'gravel': [],
                'grass': [],
                'start_line': None,
                'racing_line': False,
            }
        
        if 'name' in data:
            self.track_name = data['name']
        else:
            self.track_name = os.path.basename(filepath).replace('.json', '')
        
        self.track_path = full_path
        self._calculate_boundaries()
    
    def get_track_data(self):
        """
        Get current track data as dictionary.
        
        Returns:
            dict: Track data
        """
        return {
            'name': self.track_name,
            'waypoints': list(self.waypoints),
            'decorations': copy.deepcopy(self.decorations),
            'num_waypoints': len(self.waypoints)
        }
    
    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================
    
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
            
            dx1 = p_curr[0] - p_prev[0]
            dy1 = p_curr[1] - p_prev[1]
            dx2 = p_next[0] - p_curr[0]
            dy2 = p_next[1] - p_curr[1]
            
            len1 = math.sqrt(dx1*dx1 + dy1*dy1)
            len2 = math.sqrt(dx2*dx2 + dy2*dy2)
            if len1 > 0:
                dx1, dy1 = dx1/len1, dy1/len1
            if len2 > 0:
                dx2, dy2 = dx2/len2, dy2/len2
            
            perp1_x, perp1_y = -dy1, dx1
            perp2_x, perp2_y = -dy2, dx2
            
            avg_x = perp1_x + perp2_x
            avg_y = perp1_y + perp2_y
            avg_len = math.sqrt(avg_x*avg_x + avg_y*avg_y)
            
            if avg_len > 0.001:
                avg_x, avg_y = avg_x/avg_len, avg_y/avg_len
            else:
                avg_x, avg_y = perp1_x, perp1_y
            
            self.left_boundary.append((
                p_curr[0] + avg_x * TRACK_WIDTH,
                p_curr[1] + avg_y * TRACK_WIDTH
            ))
            self.right_boundary.append((
                p_curr[0] - avg_x * TRACK_WIDTH,
                p_curr[1] - avg_y * TRACK_WIDTH
            ))
    
    def _get_angle_between_segments(self, p1, p2, p3):
        """Calculate signed angle change at p2"""
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
    
    def _save_undo_state(self):
        """Save current state for undo"""
        state = {
            'decorations': copy.deepcopy(self.decorations),
            'waypoints': copy.deepcopy(self.waypoints),
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)
    
    # =========================================================================
    # VISUAL MODE (pygame)
    # =========================================================================
    
    def run_visual(self):
        """Run the visual editor (pygame window)"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("F1 Track Studio")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Editor mode
        self.editor_mode = EditorMode.GENERATE
        
        # Generate mode state - load from templates folder
        self.template_files = self._scan_templates_folder()
        self.template_index = 0
        self.template_info = None  # Info about current template
        self.template_preview = None
        
        # Draw mode state
        self.selected_waypoint = None
        self.dragging_waypoint = False
        
        # Decorate mode state
        self.paint_state = PaintState.IDLE
        self.current_tool = 'kerb'
        self.current_boundary = 'left'
        self.stroke_start_segment = None
        self.stroke_end_segment = None
        
        # Visual state
        self.running = True
        self.show_segment_numbers = False
        self.hover_segment = None
        self.message = "Press [1] Generate, [2] Draw, [3] Decorate"
        self.message_timer = 0
        
        # View transform
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        
        # Generate initial preview
        self._update_template_preview()
        
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
        
        if key == pygame.K_ESCAPE:
            self.running = False
        
        # Mode switching
        elif key == pygame.K_1:
            self.editor_mode = EditorMode.GENERATE
            self._update_template_preview()
            self._show_message("GENERATE MODE: Press B to browse templates, Enter to apply")
        
        elif key == pygame.K_2:
            self.editor_mode = EditorMode.DRAW
            self._show_message("DRAW MODE: Click to place waypoints, drag to move")
        
        elif key == pygame.K_3:
            self.editor_mode = EditorMode.DECORATE
            self._show_message("DECORATE MODE: Paint kerbs/gravel on boundaries")
        
        # Generate mode controls
        elif self.editor_mode == EditorMode.GENERATE:
            if key == pygame.K_b:
                # B to browse to next template from templates folder
                if self.template_files:
                    self.template_index = (self.template_index + 1) % len(self.template_files)
                    self._update_template_preview()
                    if self.template_info:
                        self._show_message(f"Template: {self.template_info['name']}")
                else:
                    self._show_message("No templates found! Run generate_templates.py first")
            
            elif key == pygame.K_RETURN:
                # Apply current template
                if self.template_files:
                    filepath = self.template_files[self.template_index]
                    self.load_template_file(filepath)
                    self._show_message(f"Applied: {self.template_info['name'] if self.template_info else 'template'}")
                else:
                    self._show_message("No templates to apply")
            
            elif key == pygame.K_v:
                # V still works for variation on hardcoded templates (legacy)
                self._show_message("Variations only work with legacy templates")
        
        # Decorate mode controls
        elif self.editor_mode == EditorMode.DECORATE:
            if key == pygame.K_k:
                self.current_tool = 'kerb'
                self._show_message("Tool: KERB (red/white stripes)")
            
            elif key == pygame.K_g:
                self.current_tool = 'gravel'
                self._show_message("Tool: GRAVEL (tan runoff)")
            
            elif key == pygame.K_f:
                self.current_tool = 'grass'
                self._show_message("Tool: GRASS (green field)")
            
            elif key == pygame.K_e:
                self.current_tool = 'eraser'
                self._show_message("Tool: ERASER")
            
            elif key == pygame.K_t:
                if self.hover_segment is not None:
                    self._save_undo_state()
                    self.decorations['start_line'] = {'segment': self.hover_segment}
                    self._show_message(f"Start line set at segment {self.hover_segment}")
                else:
                    self._show_message("Hover over a segment first")
        
        # Boundary selection (all modes) - use 'if' not 'elif' so it works in any mode
        if key == pygame.K_l:
            self.current_boundary = 'left'
            self._show_message("Boundary: LEFT (blue)")
        
        elif key == pygame.K_r:
            self.current_boundary = 'right'
            self._show_message("Boundary: RIGHT (red)")
        
        # Common actions
        if key == pygame.K_z:
            if self.undo():
                self._show_message("Undo")
            else:
                self._show_message("Nothing to undo")
        
        elif key == pygame.K_c:
            if self.editor_mode == EditorMode.DRAW:
                self.clear_waypoints()
                self._show_message("All waypoints cleared")
            elif self.editor_mode == EditorMode.DECORATE:
                self.clear_decorations()
                self._show_message("All decorations cleared")
        
        elif key == pygame.K_s:
            if len(self.waypoints) >= 3:
                self._save_track_dialog()
            else:
                self._show_message("Need at least 3 waypoints to save")
        
        elif key == pygame.K_o:
            self._load_track_dialog()
        
        elif key == pygame.K_n:
            self.show_segment_numbers = not self.show_segment_numbers
            self._show_message(f"Segment numbers: {'ON' if self.show_segment_numbers else 'OFF'}")
        
        # Zoom controls
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.zoom = min(3.0, self.zoom * 1.2)
        elif key == pygame.K_MINUS:
            self.zoom = max(0.3, self.zoom / 1.2)
        
        # Pan controls
        elif key == pygame.K_LEFT and self.editor_mode != EditorMode.GENERATE:
            self.offset_x += 50
        elif key == pygame.K_RIGHT and self.editor_mode != EditorMode.GENERATE:
            self.offset_x -= 50
        elif key == pygame.K_UP:
            self.offset_y += 50
        elif key == pygame.K_DOWN:
            self.offset_y -= 50
    
    def _handle_mouse_down(self, event):
        """Handle mouse button press"""
        if event.pos[0] >= TRACK_VIEW_WIDTH:
            return
        
        if self.editor_mode == EditorMode.DRAW:
            self._handle_draw_mouse_down(event)
        elif self.editor_mode == EditorMode.DECORATE:
            self._handle_decorate_mouse_down(event)
    
    def _handle_draw_mouse_down(self, event):
        """Handle mouse down in draw mode"""
        mx, my = event.pos
        world_x, world_y = self._screen_to_world(mx, my)
        
        if event.button == 1:
            clicked_idx = self._get_waypoint_at_screen_pos(event.pos)
            
            if clicked_idx is not None:
                self.selected_waypoint = clicked_idx
                self.dragging_waypoint = True
            else:
                self._save_undo_state()
                self.waypoints.append((int(world_x), int(world_y)))
                self._calculate_boundaries()
                self.selected_waypoint = len(self.waypoints) - 1
                self._show_message(f"Waypoint {len(self.waypoints)} placed")
        
        elif event.button == 3:
            clicked_idx = self._get_waypoint_at_screen_pos(event.pos)
            if clicked_idx is not None:
                self._save_undo_state()
                self.waypoints.pop(clicked_idx)
                self._calculate_boundaries()
                self.selected_waypoint = None
                self._show_message(f"Waypoint deleted ({len(self.waypoints)} remaining)")
    
    def _handle_decorate_mouse_down(self, event):
        """Handle mouse down in decorate mode"""
        segment = self._get_segment_at_pos(event.pos)
        
        if event.button == 1:
            if segment is not None:
                self.paint_state = PaintState.PAINTING
                self.stroke_start_segment = segment
                self.stroke_end_segment = segment
        
        elif event.button == 3:
            self.paint_state = PaintState.ERASING
            if segment is not None:
                self._erase_at_segment(segment)
    
    def _handle_mouse_up(self, event):
        """Handle mouse button release"""
        if self.editor_mode == EditorMode.DRAW:
            if event.button == 1:
                self.dragging_waypoint = False
        elif self.editor_mode == EditorMode.DECORATE:
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
        
        if self.editor_mode == EditorMode.DRAW:
            if self.dragging_waypoint and self.selected_waypoint is not None:
                mx, my = event.pos
                world_x, world_y = self._screen_to_world(mx, my)
                self.waypoints[self.selected_waypoint] = (int(world_x), int(world_y))
                self._calculate_boundaries()
        
        elif self.editor_mode == EditorMode.DECORATE:
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
    
    def _update_template_preview(self):
        """Update the template preview waypoints from templates folder"""
        if not self.template_files:
            self.template_preview = None
            self.template_info = None
            return
        
        filepath = self.template_files[self.template_index]
        self.template_info = self._load_template_info(filepath)
        
        # Load waypoints for preview
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.template_preview = [tuple(wp) for wp in data.get('waypoints', [])]
        except:
            self.template_preview = None
    
    def _get_segment_at_pos(self, pos):
        """Find the closest segment on the current boundary"""
        mx, my = pos
        
        if self.current_boundary == 'left':
            boundary_points = self.left_boundary
        else:
            boundary_points = self.right_boundary
        
        if not boundary_points:
            return None
        
        closest_segment = None
        closest_dist = float('inf')
        
        for i, (bx, by) in enumerate(boundary_points):
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
            return
        
        start = min(self.stroke_start_segment, self.stroke_end_segment)
        end = max(self.stroke_start_segment, self.stroke_end_segment)
        
        if self.current_tool == 'kerb':
            self.add_kerb(self.current_boundary, start, end)
            self._show_message(f"Added kerb: {self.current_boundary} {start}-{end}")
        elif self.current_tool == 'gravel':
            self.add_gravel(self.current_boundary, start, end)
            self._show_message(f"Added gravel: {self.current_boundary} {start}-{end}")
        elif self.current_tool == 'grass':
            self.add_grass(self.current_boundary, start, end)
            self._show_message(f"Added grass: {self.current_boundary} {start}-{end}")
        
        self.stroke_start_segment = None
        self.stroke_end_segment = None
    
    def _erase_at_segment(self, segment):
        """Erase any decoration at the given segment"""
        for dtype in ['kerbs', 'gravel', 'grass']:
            for dec in self.decorations[dtype][:]:
                if dec['boundary'] == self.current_boundary:
                    if self._segment_in_range(segment, dec['start'], dec['end']):
                        self._save_undo_state()
                        self.decorations[dtype].remove(dec)
                        return
    
    def _segment_in_range(self, segment, start, end):
        """Check if segment is in range"""
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
        """Get index of waypoint at screen position"""
        mx, my = pos
        
        for i, (wx, wy) in enumerate(self.waypoints):
            sx, sy = self._world_to_screen(wx, wy)
            dist = math.sqrt((mx - sx) ** 2 + (my - sy) ** 2)
            if dist <= 15:
                return i
        
        return None
    
    def _load_track_dialog(self):
        """Open file dialog to load track from templates folder"""
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            
            # Load from templates folder (where AI-generated tracks go)
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
            os.makedirs(templates_dir, exist_ok=True)
            
            filepath = filedialog.askopenfilename(
                title="Select Template",
                initialdir=templates_dir,
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            root.destroy()
            
            if filepath:
                self.load(filepath)
                self._show_message(f"Loaded: {os.path.basename(filepath)}")
        except Exception as e:
            self._show_message(f"Load failed: {e}")
    
    def _save_track_dialog(self):
        """Open file dialog to save track"""
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            
            tracks_dir = os.path.join(os.path.dirname(__file__), 'tracks')
            os.makedirs(tracks_dir, exist_ok=True)
            
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
                self.save(filepath)
                self._show_message(f"Saved: {os.path.basename(filepath)}")
        except Exception as e:
            self._show_message(f"Save failed: {e}")
    
    def _show_message(self, text):
        """Display a temporary message"""
        self.message = text
        self.message_timer = 180
    
    def _update(self):
        """Update visual state"""
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def _draw(self):
        """Draw everything"""
        self.screen.fill(BG_COLOR)
        
        # Draw track view background
        pygame.draw.rect(self.screen, TRACK_BG_COLOR, (0, 0, TRACK_VIEW_WIDTH, TRACK_VIEW_HEIGHT))
        
        # Draw template preview in generate mode
        if self.editor_mode == EditorMode.GENERATE and self.template_preview:
            self._draw_template_preview()
        
        # Draw track
        if len(self.waypoints) >= 3:
            self._draw_track()
            self._draw_decorations()
            self._draw_boundaries()
        
        # Draw waypoints
        self._draw_waypoints()
        
        # Draw stroke preview
        if self.editor_mode == EditorMode.DECORATE and self.paint_state == PaintState.PAINTING:
            self._draw_stroke_preview()
        
        # Draw cursor
        if self.editor_mode == EditorMode.DECORATE:
            self._draw_cursor()
        elif self.editor_mode == EditorMode.DRAW:
            self._draw_draw_mode_cursor()
        
        # Draw UI panel
        self._draw_ui_panel()
        
        pygame.display.flip()
    
    def _draw_template_preview(self):
        """Draw template preview in generate mode"""
        if not self.template_preview or len(self.template_preview) < 2:
            return
        
        # Draw as dashed line
        screen_points = [self._world_to_screen(*p) for p in self.template_preview]
        
        for i in range(0, len(screen_points), 2):
            next_i = (i + 1) % len(screen_points)
            pygame.draw.line(self.screen, (100, 100, 100), 
                           screen_points[i], screen_points[next_i], 2)
    
    def _draw_track(self):
        """Draw track surface"""
        if len(self.left_boundary) < 3 or len(self.right_boundary) < 3:
            return
        
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
        """Draw left and right boundaries"""
        if len(self.left_boundary) < 2:
            return
        
        left_screen = [self._world_to_screen(*p) for p in self.left_boundary]
        left_width = 4 if self.current_boundary == 'left' else 2
        pygame.draw.lines(self.screen, LEFT_BOUNDARY_COLOR, True, left_screen, left_width)
        
        right_screen = [self._world_to_screen(*p) for p in self.right_boundary]
        right_width = 4 if self.current_boundary == 'right' else 2
        pygame.draw.lines(self.screen, RIGHT_BOUNDARY_COLOR, True, right_screen, right_width)
    
    def _draw_waypoints(self):
        """Draw waypoints"""
        for i, (wx, wy) in enumerate(self.waypoints):
            sx, sy = self._world_to_screen(wx, wy)
            
            if self.editor_mode == EditorMode.DRAW and i == self.selected_waypoint:
                color = (100, 255, 100)
                radius = WAYPOINT_RADIUS + 3
            elif i == self.hover_segment:
                color = CURSOR_COLOR
                radius = WAYPOINT_RADIUS + 2
            else:
                color = TEXT_DIM_COLOR
                radius = WAYPOINT_RADIUS
            
            pygame.draw.circle(self.screen, color, (sx, sy), radius)
            
            if self.show_segment_numbers or i == self.hover_segment or (self.editor_mode == EditorMode.DRAW and i == self.selected_waypoint):
                if i % 5 == 0 or i == self.hover_segment or i == self.selected_waypoint:
                    text = self.font_small.render(str(i), True, TEXT_COLOR)
                    self.screen.blit(text, (sx + 8, sy - 5))
    
    def _draw_decorations(self):
        """Draw all decorations"""
        # Draw grass first (behind gravel and kerbs)
        for grass in self.decorations.get('grass', []):
            self._draw_grass_decoration(grass)
        
        # Then gravel
        for gravel in self.decorations['gravel']:
            self._draw_gravel_decoration(gravel)
        
        # Then kerbs
        for kerb in self.decorations['kerbs']:
            self._draw_kerb_decoration(kerb)
        
        # Then start line
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
        
        dx = wx2 - wx1
        dy = wy2 - wy1
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return
        
        perp_x = -dy / length
        perp_y = dx / length
        
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
        """Draw the decoration being painted"""
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
        elif self.current_tool == 'grass':
            self._draw_grass_range_preview(self.current_boundary, start, end)
    
    def _draw_kerb_decoration(self, kerb):
        """Draw a kerb decoration"""
        boundary = self.left_boundary if kerb['boundary'] == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        start = kerb['start']
        end = kerb['end']
        
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
        """Draw kerb stripes for preview"""
        boundary = self.left_boundary if boundary_name == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        stripe_count = 0
        i = start
        while True:
            next_i = (i + 1) % len(self.waypoints)
            
            if i < len(boundary) and next_i < len(boundary):
                p1 = self._world_to_screen(*boundary[i])
                p2 = self._world_to_screen(*boundary[next_i])
                
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
        
        inner_points = []
        outer_points = []
        
        i = start
        while True:
            if i < len(boundary) and i < len(self.waypoints):
                bx, by = boundary[i]
                wx, wy = self.waypoints[i]
                
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    inner_points.append(self._world_to_screen(bx, by))
                    
                    extension = 25
                    gx = bx + (dx / length) * extension
                    gy = by + (dy / length) * extension
                    outer_points.append(self._world_to_screen(gx, gy))
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        if len(outer_points) >= 3 and len(inner_points) >= 3:
            polygon = outer_points + inner_points[::-1]
            pygame.draw.polygon(self.screen, GRAVEL_COLOR, polygon)
            pygame.draw.lines(self.screen, GRAVEL_BORDER_COLOR, False, outer_points, 2)
    
    def _draw_gravel_range_preview(self, boundary_name, start, end):
        """Draw gravel strip for preview"""
        boundary = self.left_boundary if boundary_name == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        inner_points = []
        outer_points = []
        
        i = start
        while True:
            if i < len(boundary) and i < len(self.waypoints):
                bx, by = boundary[i]
                wx, wy = self.waypoints[i]
                
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    inner_points.append(self._world_to_screen(bx, by))
                    
                    extension = 25
                    gx = bx + (dx / length) * extension
                    gy = by + (dy / length) * extension
                    outer_points.append(self._world_to_screen(gx, gy))
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        if len(outer_points) >= 3 and len(inner_points) >= 3:
            polygon = outer_points + inner_points[::-1]
            pygame.draw.polygon(self.screen, GRAVEL_COLOR, polygon)
            pygame.draw.lines(self.screen, CURSOR_COLOR, True, polygon, 2)
    
    def _draw_grass_decoration(self, grass):
        """Draw a grass area decoration"""
        boundary = self.left_boundary if grass['boundary'] == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        start = grass['start']
        end = grass['end']
        
        inner_points = []
        outer_points = []
        
        i = start
        while True:
            if i < len(boundary) and i < len(self.waypoints):
                bx, by = boundary[i]
                wx, wy = self.waypoints[i]
                
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    inner_points.append(self._world_to_screen(bx, by))
                    
                    # Grass extends further than gravel (50px vs 25px)
                    extension = 50
                    gx = bx + (dx / length) * extension
                    gy = by + (dy / length) * extension
                    outer_points.append(self._world_to_screen(gx, gy))
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        if len(outer_points) >= 3 and len(inner_points) >= 3:
            polygon = outer_points + inner_points[::-1]
            pygame.draw.polygon(self.screen, GRASS_COLOR, polygon)
    
    def _draw_grass_range_preview(self, boundary_name, start, end):
        """Draw grass strip for preview"""
        boundary = self.left_boundary if boundary_name == 'left' else self.right_boundary
        if len(boundary) < 2:
            return
        
        inner_points = []
        outer_points = []
        
        i = start
        while True:
            if i < len(boundary) and i < len(self.waypoints):
                bx, by = boundary[i]
                wx, wy = self.waypoints[i]
                
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    inner_points.append(self._world_to_screen(bx, by))
                    
                    # Grass extends further than gravel (50px vs 25px)
                    extension = 50
                    gx = bx + (dx / length) * extension
                    gy = by + (dy / length) * extension
                    outer_points.append(self._world_to_screen(gx, gy))
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        if len(outer_points) >= 3 and len(inner_points) >= 3:
            polygon = outer_points + inner_points[::-1]
            pygame.draw.polygon(self.screen, GRASS_COLOR, polygon)
            pygame.draw.lines(self.screen, CURSOR_COLOR, True, polygon, 2)
    
    def _draw_cursor(self):
        """Draw cursor indicator on the boundary"""
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_pos[0] >= TRACK_VIEW_WIDTH:
            return
        
        segment = self._get_segment_at_pos(mouse_pos)
        
        if segment is not None:
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
            
            if self.current_tool == 'kerb':
                color = TOOL_KERB_COLOR
            elif self.current_tool == 'gravel':
                color = TOOL_GRAVEL_COLOR
            elif self.current_tool == 'grass':
                color = TOOL_GRASS_COLOR
            else:
                color = TOOL_ERASER_COLOR
            
            pygame.draw.circle(self.screen, color, (sx, sy), 10, 3)
            pygame.draw.circle(self.screen, CURSOR_COLOR, (sx, sy), 12, 2)
    
    def _draw_draw_mode_cursor(self):
        """Draw cursor for draw mode"""
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_pos[0] >= TRACK_VIEW_WIDTH:
            return
        
        mx, my = mouse_pos
        
        hovered_wp = self._get_waypoint_at_screen_pos(mouse_pos)
        
        if hovered_wp is not None:
            wx, wy = self.waypoints[hovered_wp]
            sx, sy = self._world_to_screen(wx, wy)
            pygame.draw.circle(self.screen, CURSOR_COLOR, (sx, sy), 12, 2)
        else:
            pygame.draw.circle(self.screen, (100, 255, 100), (mx, my), 8, 2)
            pygame.draw.line(self.screen, (100, 255, 100), (mx - 12, my), (mx + 12, my), 1)
            pygame.draw.line(self.screen, (100, 255, 100), (mx, my - 12), (mx, my + 12), 1)
    
    def _draw_ui_panel(self):
        """Draw UI panel"""
        pygame.draw.rect(self.screen, PANEL_BG_COLOR, (PANEL_X, 0, PANEL_WIDTH, SCREEN_HEIGHT))
        
        y = 20
        
        # Title
        title = self.font_large.render("Track Studio", True, TEXT_COLOR)
        self.screen.blit(title, (PANEL_X + 10, y))
        y += 35
        
        # Mode indicator
        mode_names = {
            EditorMode.GENERATE: "[GENERATE MODE]",
            EditorMode.DRAW: "[DRAW MODE]",
            EditorMode.DECORATE: "[DECORATE MODE]"
        }
        mode_colors = {
            EditorMode.GENERATE: (255, 200, 100),
            EditorMode.DRAW: (100, 255, 100),
            EditorMode.DECORATE: ACCENT_COLOR
        }
        mode_text = mode_names.get(self.editor_mode, "[UNKNOWN]")
        mode_color = mode_colors.get(self.editor_mode, TEXT_COLOR)
        mode_surf = self.font_medium.render(mode_text, True, mode_color)
        self.screen.blit(mode_surf, (PANEL_X + 10, y))
        y += 25
        
        # Mode-specific info
        if self.editor_mode == EditorMode.GENERATE:
            if self.template_files and self.template_info:
                # Show template count
                count_text = f"[{self.template_index + 1}/{len(self.template_files)}]"
                text = self.font_small.render(count_text, True, ACCENT_COLOR)
                self.screen.blit(text, (PANEL_X + 10, y))
                y += 18
                # Show template name
                text = self.font_small.render(f"{self.template_info['name']}", True, TEXT_DIM_COLOR)
                self.screen.blit(text, (PANEL_X + 10, y))
                y += 18
                # Show style
                style_text = f"Style: {self.template_info.get('style', 'unknown')}"
                text = self.font_small.render(style_text, True, TEXT_DIM_COLOR)
                self.screen.blit(text, (PANEL_X + 10, y))
                y += 18
            else:
                text = self.font_small.render("No templates found", True, TEXT_DIM_COLOR)
                self.screen.blit(text, (PANEL_X + 10, y))
                y += 18
                text = self.font_small.render("Run generate_templates.py", True, TEXT_DIM_COLOR)
                self.screen.blit(text, (PANEL_X + 10, y))
                y += 18
        
        elif self.editor_mode == EditorMode.DECORATE:
            tool_text = f"Tool: {self.current_tool.upper()}"
            if self.current_tool == 'kerb':
                tool_color = TOOL_KERB_COLOR
            elif self.current_tool == 'gravel':
                tool_color = TOOL_GRAVEL_COLOR
            elif self.current_tool == 'grass':
                tool_color = TOOL_GRASS_COLOR
            else:
                tool_color = TOOL_ERASER_COLOR
            text = self.font_small.render(tool_text, True, tool_color)
            self.screen.blit(text, (PANEL_X + 10, y))
            y += 18
        
        # Track info
        y += 10
        text = self.font_small.render(f"Waypoints: {len(self.waypoints)}", True, TEXT_DIM_COLOR)
        self.screen.blit(text, (PANEL_X + 10, y))
        y += 18
        
        text = self.font_small.render(f"Kerbs: {len(self.decorations['kerbs'])}", True, TEXT_DIM_COLOR)
        self.screen.blit(text, (PANEL_X + 10, y))
        y += 18
        
        text = self.font_small.render(f"Gravel: {len(self.decorations['gravel'])}", True, TEXT_DIM_COLOR)
        self.screen.blit(text, (PANEL_X + 10, y))
        y += 18
        
        text = self.font_small.render(f"Grass: {len(self.decorations.get('grass', []))}", True, TEXT_DIM_COLOR)
        self.screen.blit(text, (PANEL_X + 10, y))
        y += 25
        
        # Mode section
        pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15
        
        mode_title = self.font_medium.render("MODE", True, TEXT_COLOR)
        self.screen.blit(mode_title, (PANEL_X + 10, y))
        y += 22
        
        modes = [
            ('1', 'Generate', EditorMode.GENERATE),
            ('2', 'Draw', EditorMode.DRAW),
            ('3', 'Decorate', EditorMode.DECORATE),
        ]
        
        for key, name, mode in modes:
            is_active = self.editor_mode == mode
            key_text = self.font_small.render(f"[{key}]", True, ACCENT_COLOR if is_active else TEXT_DIM_COLOR)
            name_text = self.font_small.render(name, True, TEXT_COLOR if is_active else TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 10, y))
            self.screen.blit(name_text, (PANEL_X + 45, y))
            y += 18
        
        y += 10
        
        # Mode-specific controls
        pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15
        
        if self.editor_mode == EditorMode.GENERATE:
            controls_title = self.font_medium.render("TEMPLATES", True, TEXT_COLOR)
            self.screen.blit(controls_title, (PANEL_X + 10, y))
            y += 22
            
            controls = [
                ('B', 'Browse'),
                ('Enter', 'Apply'),
                ('V', 'Variation'),
            ]
        
        elif self.editor_mode == EditorMode.DRAW:
            controls_title = self.font_medium.render("DRAWING", True, TEXT_COLOR)
            self.screen.blit(controls_title, (PANEL_X + 10, y))
            y += 22
            
            controls = [
                ('Click', 'Place point'),
                ('Drag', 'Move point'),
                ('Right', 'Delete point'),
            ]
        
        else:  # DECORATE
            controls_title = self.font_medium.render("TOOLS", True, TEXT_COLOR)
            self.screen.blit(controls_title, (PANEL_X + 10, y))
            y += 22
            
            controls = [
                ('K', 'Kerb'),
                ('G', 'Gravel'),
                ('F', 'Grass'),
                ('E', 'Eraser'),
                ('L', 'Left boundary'),
                ('R', 'Right boundary'),
                ('T', 'Start line'),
            ]
        
        for key, action in controls:
            key_text = self.font_small.render(key, True, ACCENT_COLOR)
            action_text = self.font_small.render(action, True, TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 10, y))
            self.screen.blit(action_text, (PANEL_X + 70, y))
            y += 18
        
        y += 10
        
        # Common actions
        pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15
        
        actions_title = self.font_medium.render("ACTIONS", True, TEXT_COLOR)
        self.screen.blit(actions_title, (PANEL_X + 10, y))
        y += 22
        
        actions = [
            ('S', 'Save'),
            ('O', 'Open'),
            ('Z', 'Undo'),
            ('C', 'Clear'),
            ('N', 'Numbers'),
            ('Esc', 'Exit'),
        ]
        
        for key, action in actions:
            key_text = self.font_small.render(f"[{key}]", True, ACCENT_COLOR)
            action_text = self.font_small.render(action, True, TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 10, y))
            self.screen.blit(action_text, (PANEL_X + 55, y))
            y += 18
        
        # Hover segment info
        if self.hover_segment is not None:
            y = SCREEN_HEIGHT - 100
            pygame.draw.line(self.screen, (60, 60, 60), (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
            y += 10
            text = self.font_medium.render(f"Segment: {self.hover_segment}", True, CURSOR_COLOR)
            self.screen.blit(text, (PANEL_X + 10, y))
        
        # Message at bottom
        if self.message_timer > 0:
            msg_y = SCREEN_HEIGHT - 50
            pygame.draw.rect(self.screen, (40, 40, 40), (PANEL_X, msg_y, PANEL_WIDTH, 50))
            
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
                self.screen.blit(text, (PANEL_X + 10, msg_y + 8 + i * 18))


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Entry point for visual mode"""
    import sys
    
    track_path = None
    if len(sys.argv) > 1:
        track_path = sys.argv[1]
    
    studio = TrackStudio(track_path)
    studio.run_visual()


if __name__ == "__main__":
    main()
