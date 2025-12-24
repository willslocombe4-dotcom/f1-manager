"""
F1 Track - Circuit layout and waypoint generation
"""
import math
import config

class Track:
    """Represents an F1 circuit with waypoints for car movement"""

    def __init__(self, waypoints=None):
        self.center_x = config.TRACK_CENTER_X
        self.center_y = config.TRACK_CENTER_Y
        self.outer_radius = config.TRACK_OUTER_RADIUS
        self.inner_radius = config.TRACK_INNER_RADIUS
        self.racing_line_radius = (self.outer_radius + self.inner_radius) // 2

        # Use provided waypoints or generate default
        if waypoints is not None:
            self.waypoints = waypoints
        else:
            self.waypoints = self._generate_waypoints()
        self.track_length = len(self.waypoints)

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
        Calculate outer and inner track boundaries
        Returns tuple of (outer_points, inner_points)
        """
        outer_points = []
        inner_points = []

        for i, (x, y) in enumerate(self.waypoints):
            # Get direction to next point
            next_i = (i + 1) % len(self.waypoints)
            next_x, next_y = self.waypoints[next_i]

            dx = next_x - x
            dy = next_y - y
            length = math.sqrt(dx * dx + dy * dy)

            if length > 0:
                # Perpendicular direction
                perp_x = -dy / length
                perp_y = dx / length

                # Outer and inner points
                outer_points.append((x + perp_x * track_width, y + perp_y * track_width))
                inner_points.append((x - perp_x * track_width, y - perp_y * track_width))

        return outer_points, inner_points
