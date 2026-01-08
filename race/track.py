"""
F1 Track - Circuit layout and waypoint generation
"""
import math
import config
from data import circuits


def normalize_angle(angle):
    """Normalize angle to [-pi, pi] range"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def get_angle_between_segments(p1, p2, p3):
    """
    Calculate the signed angle change at p2 between segments p1->p2 and p2->p3.
    Positive = left turn (CCW), Negative = right turn (CW)
    Returns angle in radians.
    """
    dx1 = p2[0] - p1[0]
    dy1 = p2[1] - p1[1]
    dx2 = p3[0] - p2[0]
    dy2 = p3[1] - p2[1]
    
    angle1 = math.atan2(dy1, dx1)
    angle2 = math.atan2(dy2, dx2)
    
    return normalize_angle(angle2 - angle1)


class Track:
    """Represents an F1 circuit with waypoints for car movement"""

    def __init__(self, waypoints=None, decorations=None, circuit_id=None):
        self.center_x = config.TRACK_CENTER_X
        self.center_y = config.TRACK_CENTER_Y
        self.outer_radius = config.TRACK_OUTER_RADIUS
        self.inner_radius = config.TRACK_INNER_RADIUS
        self.racing_line_radius = (self.outer_radius + self.inner_radius) // 2

        # Circuit metadata
        self.circuit_id = circuit_id
        self.circuit_data = None
        if circuit_id:
            self.circuit_data = circuits.get_circuit_by_id(circuit_id)

        # Use provided waypoints, circuit waypoints, or generate default
        if waypoints is not None:
            self.waypoints = waypoints
        elif self.circuit_data:
            self.waypoints = self.circuit_data["waypoints"]
        else:
            self.waypoints = self._generate_waypoints()
        self.track_length = len(self.waypoints)

        # Decorations (kerbs and gravel traps)
        # Format: {'kerbs': [{'boundary': 'left'|'right', 'start': int, 'end': int}, ...],
        #          'gravel': [{'boundary': 'left'|'right', 'start': int, 'end': int}, ...]}
        self.decorations = decorations or {'kerbs': [], 'gravel': []}

    def _generate_waypoints(self):
        """
        Generate waypoints for an F1-style circuit
        Imported from track_20251221_032901_export.py
        Total waypoints: 65
        """
        waypoints = [
            (292, 133), (211, 162), (127, 204), (75, 231), (74, 280),
            (95, 329), (110, 375), (97, 418), (85, 454), (83, 479),
            (83, 510), (89, 547), (93, 567), (111, 614), (151, 656),
            (211, 681), (300, 721), (403, 762), (489, 799), (576, 844),
            (621, 846), (664, 704), (637, 584), (550, 481), (411, 313),
            (419, 203), (465, 143), (519, 133), (554, 142), (561, 173),
            (554, 202), (545, 229), (542, 263), (550, 283), (564, 292),
            (602, 282), (613, 246), (645, 208), (684, 177), (731, 172),
            (727, 214), (709, 247), (691, 264), (669, 296), (654, 329),
            (653, 366), (657, 404), (667, 438), (688, 471), (706, 498),
            (723, 520), (749, 534), (775, 563), (797, 588), (817, 594),
            (835, 547), (850, 480), (849, 434), (839, 338), (825, 279),
            (802, 190), (755, 132), (685, 102), (531, 55), (353, 103),
        ]

        return waypoints

    def get_position(self, progress):
        """
        Get x, y coordinates for a given progress (0.0 to 1.0) around the track.
        Uses linear interpolation between waypoints for smooth movement.
        
        Note: Handles negative progress values (used for grid formation) correctly
        by using math.floor() instead of int() for proper floor division.
        """
        # Calculate exact position with interpolation
        exact_index = progress * self.track_length
        
        # Use math.floor() for correct handling of negative values
        # int() rounds toward zero: int(-0.975) = 0
        # math.floor() always rounds down: math.floor(-0.975) = -1
        floored_index = math.floor(exact_index)
        index = floored_index % self.track_length
        next_index = (index + 1) % self.track_length
        
        # Interpolation factor (0.0 to 1.0 between waypoints)
        # With math.floor(), t is always positive: -0.975 - (-1) = 0.025
        t = exact_index - floored_index
        
        x1, y1 = self.waypoints[index]
        x2, y2 = self.waypoints[next_index]
        
        # Linear interpolation
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        
        return x, y

    def get_angle(self, progress):
        """
        Get the angle (in radians) of the track at a given progress.
        Uses interpolation between segment angles for smooth rotation.
        
        Note: Handles negative progress values (used for grid formation) correctly
        by using math.floor() instead of int() for proper floor division.
        """
        # Calculate exact position
        exact_index = progress * self.track_length
        
        # Use math.floor() for correct handling of negative values
        floored_index = math.floor(exact_index)
        index = floored_index % self.track_length
        next_index = (index + 1) % self.track_length
        next_next_index = (index + 2) % self.track_length
        
        # Interpolation factor (always 0.0 to 1.0 with math.floor())
        t = exact_index - floored_index

        # Get current segment angle
        x1, y1 = self.waypoints[index]
        x2, y2 = self.waypoints[next_index]
        angle1 = math.atan2(y2 - y1, x2 - x1)
        
        # Get next segment angle
        x3, y3 = self.waypoints[next_next_index]
        angle2 = math.atan2(y3 - y2, x3 - x2)
        
        # Handle angle wrapping (e.g., from 179° to -179°)
        angle_diff = angle2 - angle1
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        elif angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # Interpolate angle
        return angle1 + angle_diff * t

    def get_offset_position(self, progress, offset):
        """
        Get position offset from racing line (for multiple cars side by side)
        offset: perpendicular distance from racing line (positive = right, negative = left)
        """
        x, y = self.get_position(progress)
        angle = self.get_angle(progress)

        # Perpendicular angle (90 degrees offset)
        perp_angle = angle + math.pi / 2

        offset_x = x + offset * math.cos(perp_angle)
        offset_y = y + offset * math.sin(perp_angle)

        return offset_x, offset_y

    def get_corner_indices(self, curvature_threshold=15):
        """
        Identify corner waypoints based on angle change
        Returns list of waypoint indices that represent corners
        """
        corners = []
        threshold_rad = math.radians(curvature_threshold)

        for i in range(len(self.waypoints)):
            prev_i = (i - 1) % len(self.waypoints)
            next_i = (i + 1) % len(self.waypoints)

            # Get angles
            x1, y1 = self.waypoints[prev_i]
            x2, y2 = self.waypoints[i]
            x3, y3 = self.waypoints[next_i]

            # Calculate angles
            angle1 = math.atan2(y2 - y1, x2 - x1)
            angle2 = math.atan2(y3 - y2, x3 - x2)

            # Calculate angle change
            angle_diff = abs(angle2 - angle1)
            # Normalize to 0-pi range
            if angle_diff > math.pi:
                angle_diff = 2 * math.pi - angle_diff

            if angle_diff > threshold_rad:
                corners.append(i)

        return corners

    def get_track_boundaries(self, track_width=35):
        """
        Calculate left and right track boundaries using averaged perpendicular offsets.
        
        The track is defined by waypoints that form the racing line (center).
        - left_boundary: boundary on the LEFT side of the racing line direction
        - right_boundary: boundary on the RIGHT side of the racing line direction
        
        Uses a simple bevel-style join (averaged perpendiculars) which avoids
        the complexity and edge cases of miter joins at sharp corners.
        
        Returns tuple of (left_boundary, right_boundary)
        """
        if len(self.waypoints) < 3:
            return [], []
        
        left_boundary = []
        right_boundary = []
        
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
            left_boundary.append((p_curr[0] + avg_x * track_width, p_curr[1] + avg_y * track_width))
            right_boundary.append((p_curr[0] - avg_x * track_width, p_curr[1] - avg_y * track_width))
        
        return left_boundary, right_boundary

    def get_boundary_points_for_range(self, boundary, start, end, track_width=35):
        """
        Get boundary points for a segment range.
        
        Args:
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
            track_width: Width of track from center to boundary
            
        Returns:
            list: List of (x, y) points from the specified boundary
        """
        left_boundary, right_boundary = self.get_track_boundaries(track_width)
        boundary_points = left_boundary if boundary == 'left' else right_boundary
        
        if not boundary_points:
            return []
        
        points = []
        i = start
        while True:
            if i < len(boundary_points):
                points.append(boundary_points[i])
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        return points

    def get_gravel_strip_points(self, boundary, start, end, track_width=35, extension=25):
        """
        Get inner and outer points for a gravel strip polygon.
        
        Args:
            boundary: 'left' or 'right'
            start: Starting segment index
            end: Ending segment index
            track_width: Width of track from center to boundary
            extension: How far gravel extends beyond track boundary
            
        Returns:
            tuple: (inner_points, outer_points) where each is a list of (x, y) tuples
        """
        left_boundary, right_boundary = self.get_track_boundaries(track_width)
        boundary_points = left_boundary if boundary == 'left' else right_boundary
        
        if not boundary_points:
            return [], []
        
        inner_points = []
        outer_points = []
        
        i = start
        while True:
            if i < len(boundary_points) and i < len(self.waypoints):
                bx, by = boundary_points[i]
                wx, wy = self.waypoints[i]
                
                # Direction from waypoint to boundary
                dx = bx - wx
                dy = by - wy
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    inner_points.append((bx, by))
                    
                    # Extend beyond boundary
                    gx = bx + (dx / length) * extension
                    gy = by + (dy / length) * extension
                    outer_points.append((gx, gy))
            
            if i == end:
                break
            i = (i + 1) % len(self.waypoints)
        
        return inner_points, outer_points

    def has_explicit_decorations(self):
        """
        Check if track has explicit decorations defined.

        Returns:
            bool: True if decorations are defined, False otherwise
        """
        return bool(self.decorations.get('kerbs') or self.decorations.get('gravel'))

    # =============================================================================
    # CIRCUIT METADATA ACCESS METHODS
    # =============================================================================

    def get_circuit_name(self):
        """
        Get the full name of the circuit.

        Returns:
            str: Circuit name or None if not a real F1 circuit
        """
        if self.circuit_data:
            return self.circuit_data.get("name")
        return None

    def get_circuit_location(self):
        """
        Get the location of the circuit.

        Returns:
            str: Circuit location or None if not a real F1 circuit
        """
        if self.circuit_data:
            return self.circuit_data.get("location")
        return None

    def get_circuit_length_km(self):
        """
        Get the length of the circuit in kilometers.

        Returns:
            float: Circuit length in km or None if not a real F1 circuit
        """
        if self.circuit_data:
            return self.circuit_data.get("length_km")
        return None

    def get_circuit_type(self):
        """
        Get the type of circuit (street or permanent).

        Returns:
            str: 'street' or 'permanent', or None if not a real F1 circuit
        """
        if self.circuit_data:
            return self.circuit_data.get("type")
        return None

    def get_tire_degradation_multiplier(self):
        """
        Get the tire degradation multiplier for this circuit.
        Different circuits wear tires at different rates.

        Returns:
            float: Tire degradation multiplier (0.7 to 1.4), defaults to config.DEFAULT_TIRE_DEG_MULTIPLIER
        """
        if self.circuit_data and "characteristics" in self.circuit_data:
            return self.circuit_data["characteristics"].get("tire_degradation", config.DEFAULT_TIRE_DEG_MULTIPLIER)
        return config.DEFAULT_TIRE_DEG_MULTIPLIER

    def get_drs_zones(self):
        """
        Get DRS zones for this circuit.
        DRS zones are defined as progress ranges (0.0 to 1.0).

        Returns:
            list: List of dicts with 'start' and 'end' keys, or empty list if none
        """
        if self.circuit_data:
            return self.circuit_data.get("drs_zones", [])
        return []

    def is_in_drs_zone(self, progress):
        """
        Check if a given progress value is within a DRS zone.

        Args:
            progress: Current progress around track (0.0 to 1.0)

        Returns:
            bool: True if in a DRS zone, False otherwise
        """
        drs_zones = self.get_drs_zones()
        for zone in drs_zones:
            # Handle progress wrapping (DRS zone may cross start/finish)
            start = zone["start"]
            end = zone["end"]

            if start <= end:
                # Normal case: zone doesn't cross start/finish
                if start <= progress <= end:
                    return True
            else:
                # Zone crosses start/finish line
                if progress >= start or progress <= end:
                    return True
        return False

    def get_track_characteristics(self):
        """
        Get track characteristics (tire degradation, overtaking difficulty, etc.).

        Returns:
            dict: Track characteristics or empty dict if not a real F1 circuit
        """
        if self.circuit_data:
            return self.circuit_data.get("characteristics", {})
        return {}

    def get_famous_corners(self):
        """
        Get list of famous corners on this circuit.

        Returns:
            list: List of dicts with 'name' and 'description', or empty list
        """
        if self.circuit_data:
            return self.circuit_data.get("famous_corners", [])
        return []

    def is_real_f1_circuit(self):
        """
        Check if this is a real F1 circuit or a custom track.

        Returns:
            bool: True if real F1 circuit, False if custom/default track
        """
        return self.circuit_data is not None
