"""
Track Loader - Loads track waypoints from JSON files
"""
import os
import json
import config


def get_available_tracks():
    """
    Get list of available tracks from the tracks directory.
    
    Returns:
        list: List of dicts with 'name', 'filepath', and 'num_waypoints' keys.
              Returns empty list if directory doesn't exist.
    """
    tracks = []
    tracks_dir = config.TRACKS_DIRECTORY
    
    if not os.path.exists(tracks_dir):
        return tracks
    
    for filename in os.listdir(tracks_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(tracks_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    
                # Extract track info
                track_info = {
                    'name': filename.replace('.json', '').replace('_', ' ').title(),
                    'filepath': filepath,
                    'num_waypoints': data.get('num_waypoints', len(data.get('waypoints', []))),
                }
                tracks.append(track_info)
            except (json.JSONDecodeError, IOError):
                # Skip invalid files
                continue
    
    # Sort by name
    tracks.sort(key=lambda t: t['name'])
    return tracks


def load_track_waypoints(filepath):
    """
    Load waypoints from a JSON track file.
    
    Args:
        filepath: Path to the JSON track file
        
    Returns:
        list: List of (x, y) tuples representing waypoints.
              Returns None if file cannot be loaded.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert waypoints to tuples
        waypoints = []
        for point in data.get('waypoints', []):
            if isinstance(point, (list, tuple)) and len(point) >= 2:
                waypoints.append((int(point[0]), int(point[1])))
        
        if len(waypoints) < 3:
            return None
            
        return waypoints
        
    except (json.JSONDecodeError, IOError, KeyError):
        return None


def get_default_waypoints():
    """
    Get the default track waypoints (hardcoded).
    This is the same track used in race/track.py.
    
    Returns:
        list: List of (x, y) tuples representing the default circuit.
    """
    return [
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
