import json
import math
import glob
import os
import sys

def load_track(filepath):
    """Loads a track JSON file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        points_data = None
        if isinstance(data, list):
            points_data = data
        elif isinstance(data, dict):
            if 'points' in data:
                points_data = data['points']
            elif 'waypoints' in data:
                points_data = data['waypoints']
        
        if points_data is None:
            print(f"Error: Unknown JSON structure in {filepath}")
            return None

        # Convert to standard format [{'x': x, 'y': y}, ...]
        standardized_points = []
        for p in points_data:
            if isinstance(p, dict) and 'x' in p and 'y' in p:
                standardized_points.append(p)
            elif isinstance(p, (list, tuple)) and len(p) >= 2:
                standardized_points.append({'x': p[0], 'y': p[1]})
            else:
                print(f"Warning: Invalid point format in {filepath}: {p}")
        
        return standardized_points
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def dist_sq(p1, p2):
    return (p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2

def dist(p1, p2):
    return math.sqrt(dist_sq(p1, p2))

def get_segments(points):
    """Returns a list of segments (p1, p2) from the points."""
    segments = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)] # Loop back to start
        segments.append((p1, p2))
    return segments

def on_segment(p, a, b):
    """Checks if point p lies on segment ab."""
    return (p['x'] <= max(a['x'], b['x']) and p['x'] >= min(a['x'], b['x']) and
            p['y'] <= max(a['y'], b['y']) and p['y'] >= min(a['y'], b['y']))

def orientation(p, q, r):
    """
    0 -> Collinear
    1 -> Clockwise
    2 -> Counterclockwise
    """
    val = (q['y'] - p['y']) * (r['x'] - q['x']) - (q['x'] - p['x']) * (r['y'] - q['y'])
    if val == 0: return 0
    return 1 if val > 0 else 2

def do_intersect(p1, q1, p2, q2):
    """Checks if segment p1q1 intersects with p2q2."""
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases (collinear) - usually not needed for simple crossing check but good for robustness
    if o1 == 0 and on_segment(p2, p1, q1): return True
    if o2 == 0 and on_segment(q2, p1, q1): return True
    if o3 == 0 and on_segment(p1, p2, q2): return True
    if o4 == 0 and on_segment(q1, p2, q2): return True

    return False

def check_intersections(points):
    """A. Self-Intersection (The 'Figure-8' Check)"""
    segments = get_segments(points)
    n = len(segments)
    errors = []
    
    # Naive O(N^2) check is fine for track sizes (< 1000 points)
    for i in range(n):
        for j in range(i + 2, n): # Skip adjacent segments
            # If it's the last segment and first segment, they share a point (closed loop), so skip
            if i == 0 and j == n - 1:
                continue
                
            p1, q1 = segments[i]
            p2, q2 = segments[j]
            
            if do_intersect(p1, q1, p2, q2):
                errors.append(f"Track intersects itself at indices {i} and {j}.")
                # Return early or collect all? Spec implies reporting, let's collect.
                
    return errors

def get_angle(p1, p2, p3):
    """Calculates the interior angle at p2."""
    # Vector p2->p1
    v1x = p1['x'] - p2['x']
    v1y = p1['y'] - p2['y']
    # Vector p2->p3
    v2x = p3['x'] - p2['x']
    v2y = p3['y'] - p2['y']
    
    dot = v1x * v2x + v1y * v2y
    mag1 = math.sqrt(v1x**2 + v1y**2)
    mag2 = math.sqrt(v2x**2 + v2y**2)
    
    if mag1 == 0 or mag2 == 0:
        return 0
        
    # Clamp for floating point errors
    cos_angle = max(-1.0, min(1.0, dot / (mag1 * mag2)))
    angle = math.degrees(math.acos(cos_angle))
    return angle

def check_angles(points):
    """B. Minimum Angle (The 'Spike' Check)"""
    errors = []
    n = len(points)
    for i in range(n):
        p1 = points[(i - 1 + n) % n]
        p2 = points[i]
        p3 = points[(i + 1) % n]
        
        angle = get_angle(p1, p2, p3)
        # Spec says: Threshold: Angle must be > 45°.
        # Note: A straight line is 180. A sharp spike back is near 0.
        if angle < 45:
            errors.append(f"Sharp spike detected at index {i} (Angle: {angle:.1f} deg).")
            
    return errors

def check_spacing(points):
    """C. Segment Length Consistency (The 'Bunching' Check)"""
    errors = []
    lengths = []
    n = len(points)
    
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        lengths.append(dist(p1, p2))
        
    if not lengths:
        return ["No segments found."]
        
    sorted_lengths = sorted(lengths)
    median_len = sorted_lengths[len(lengths) // 2]
    
    if median_len == 0:
        return ["Median segment length is 0."]

    l_min_threshold = 0.2 * median_len
    l_max_threshold = 3.0 * median_len
    
    for i, length in enumerate(lengths):
        if length < l_min_threshold:
            errors.append(f"Segment {i} length ({length:.1f}) is too short (Median: {median_len:.1f}).")
        elif length > l_max_threshold:
            errors.append(f"Segment {i} length ({length:.1f}) is too long (Median: {median_len:.1f}).")
            
    return errors

def check_curvature(points):
    """D. Curvature Continuity (The 'Kink' Check)"""
    # Spec: Measure the *change* in direction between consecutive segments.
    # Threshold: Direction change < 90° per step.
    # This is effectively 180 - interior angle.
    # If interior angle is < 90, then turn is > 90.
    
    errors = []
    n = len(points)
    for i in range(n):
        p1 = points[(i - 1 + n) % n]
        p2 = points[i]
        p3 = points[(i + 1) % n]
        
        angle = get_angle(p1, p2, p3)
        turn_angle = 180 - angle
        
        if turn_angle > 90:
             errors.append(f"Abrupt turn at index {i} (Turn angle: {turn_angle:.1f} deg).")
             
    return errors

def validate_track(filepath):
    print(f"Validating {filepath}...")
    points = load_track(filepath)
    if not points or len(points) < 3:
        print("  [FAIL] Invalid track data or too few points.")
        return False
        
    all_errors = []
    
    # Run checks
    all_errors.extend(check_intersections(points))
    all_errors.extend(check_angles(points))
    all_errors.extend(check_spacing(points))
    all_errors.extend(check_curvature(points))
    
    if all_errors:
        print("  [FAIL] Issues found:")
        for err in all_errors[:10]: # Limit output
            print(f"    - {err}")
        if len(all_errors) > 10:
            print(f"    - ... and {len(all_errors) - 10} more.")
        return False
    else:
        print("  [PASS] Track is valid.")
        return True

def main():
    track_dir = os.path.join("tools", "tracks")
    pattern = os.path.join(track_dir, "*.json")
    files = glob.glob(pattern)
    
    if not files:
        print(f"No track files found in {track_dir}")
        return
        
    print(f"Found {len(files)} tracks to validate.")
    print("-" * 40)
    
    failed_count = 0
    for f in files:
        if not validate_track(f):
            failed_count += 1
            
    print("-" * 40)
    print(f"Validation complete. {len(files) - failed_count} passed, {failed_count} failed.")
    
    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
