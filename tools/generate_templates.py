"""
AI Template Generator - Creates quality F1-style track templates

Usage:
    python tools/generate_templates.py [count]
    
    count: Number of templates to generate (default: 10)

Templates are saved to tools/templates/ and can be loaded in Track Studio.

Uses proven track layout patterns with controlled variations to ensure
every generated track is race-worthy.
"""

import os
import sys
import json
import math
import random
from datetime import datetime

# Output directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

# Screen dimensions for scaling
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 800
MARGIN = 60


# =============================================================================
# PROVEN TRACK LAYOUT PATTERNS
# =============================================================================
# These are normalized (0-1) control points that create good racing circuits.
# Each pattern has been designed to create interesting, balanced tracks.

LAYOUT_PATTERNS = {
    'classic_gp': {
        'name': 'Classic Grand Prix',
        'description': 'Traditional GP layout with long straight and technical section',
        'points': [
            (0.15, 0.15), (0.50, 0.10), (0.85, 0.15),  # Top section
            (0.92, 0.30), (0.88, 0.50),                 # Right hairpin
            (0.75, 0.55), (0.60, 0.45), (0.50, 0.55),  # Esses
            (0.40, 0.50), (0.30, 0.60),                 # Technical
            (0.35, 0.75), (0.55, 0.85), (0.75, 0.80),  # Bottom sweep
            (0.85, 0.70), (0.80, 0.55),                 # Chicane entry
            (0.20, 0.85), (0.10, 0.70),                 # Back section
            (0.08, 0.45), (0.10, 0.25),                 # Return
        ],
    },
    'power_circuit': {
        'name': 'Power Circuit',
        'description': 'Long straights with heavy braking zones',
        'points': [
            (0.10, 0.20), (0.45, 0.12), (0.80, 0.15),  # Main straight
            (0.92, 0.25), (0.90, 0.40),                 # Turn 1 hairpin
            (0.75, 0.45), (0.55, 0.40), (0.40, 0.50),  # Short technical
            (0.45, 0.65), (0.70, 0.70),                 # Back straight
            (0.85, 0.80), (0.80, 0.90),                 # Turn complex
            (0.55, 0.88), (0.30, 0.85),                 # Straight
            (0.12, 0.75), (0.08, 0.55),                 # Hairpin
            (0.12, 0.38),                               # Return
        ],
    },
    'street_circuit': {
        'name': 'Street Circuit',
        'description': 'Tight and technical with many corners',
        'points': [
            (0.20, 0.15), (0.40, 0.12), (0.60, 0.15),  # Start
            (0.75, 0.22), (0.80, 0.35),                 # 90 degree
            (0.72, 0.45), (0.60, 0.42),                 # Chicane
            (0.50, 0.50), (0.55, 0.62),                 # Hairpin
            (0.70, 0.70), (0.80, 0.78),                 # Corner
            (0.75, 0.88), (0.55, 0.90),                 # Tight section
            (0.35, 0.85), (0.25, 0.75),                 # More corners
            (0.30, 0.60), (0.22, 0.48),                 # Chicane
            (0.15, 0.35), (0.12, 0.22),                 # Return
        ],
    },
    'flowing_circuit': {
        'name': 'Flowing Circuit',
        'description': 'Fast sweeping corners with rhythm',
        'points': [
            (0.15, 0.18), (0.40, 0.10), (0.70, 0.12),  # Fast straight
            (0.88, 0.22), (0.92, 0.42),                 # Sweeper
            (0.85, 0.58), (0.70, 0.52),                 # Esses entry
            (0.55, 0.58), (0.45, 0.50),                 # Esses
            (0.35, 0.58), (0.28, 0.70),                 # More flow
            (0.38, 0.82), (0.58, 0.88),                 # Bottom sweep
            (0.78, 0.82), (0.88, 0.70),                 # Fast corner
            (0.82, 0.55), (0.65, 0.65),                 # Link
            (0.25, 0.78), (0.10, 0.60),                 # Return sweep
            (0.08, 0.38),                               # Back
        ],
    },
    'modern_tilke': {
        'name': 'Modern Circuit',
        'description': 'Modern design with DRS zones and tight sections',
        'points': [
            (0.12, 0.15), (0.50, 0.08), (0.85, 0.12),  # DRS straight 1
            (0.94, 0.28), (0.88, 0.45),                 # Heavy braking
            (0.70, 0.48), (0.55, 0.42),                 # Technical
            (0.45, 0.52), (0.50, 0.68),                 # Hairpin
            (0.68, 0.75), (0.85, 0.72),                 # DRS straight 2
            (0.92, 0.85), (0.78, 0.92),                 # Corner complex
            (0.50, 0.88), (0.25, 0.85),                 # Straight
            (0.10, 0.72), (0.08, 0.50),                 # Hairpin 2
            (0.15, 0.32),                               # Return
        ],
    },
    'arena_circuit': {
        'name': 'Arena Circuit',
        'description': 'Compact layout with lots of action',
        'points': [
            (0.25, 0.18), (0.55, 0.15), (0.78, 0.22),  # Start
            (0.85, 0.38), (0.78, 0.52),                 # Turn 1-2
            (0.62, 0.48), (0.52, 0.58),                 # Chicane
            (0.60, 0.72), (0.78, 0.78),                 # Acceleration
            (0.82, 0.88), (0.65, 0.92),                 # Hairpin
            (0.42, 0.85), (0.28, 0.78),                 # Corners
            (0.22, 0.62), (0.30, 0.48),                 # Technical
            (0.22, 0.35), (0.18, 0.25),                 # Return
        ],
    },
    'figure_flow': {
        'name': 'Figure Flow',
        'description': 'Flowing layout with crossover feel',
        'points': [
            (0.20, 0.12), (0.50, 0.08), (0.80, 0.15),  # Top
            (0.90, 0.32), (0.82, 0.50),                 # Right side
            (0.65, 0.55), (0.48, 0.48),                 # Cross middle
            (0.32, 0.55), (0.20, 0.68),                 # Left dip
            (0.28, 0.82), (0.50, 0.90),                 # Bottom
            (0.75, 0.85), (0.88, 0.72),                 # Right bottom
            (0.85, 0.55), (0.70, 0.45),                 # Back up
            (0.35, 0.42), (0.15, 0.55),                 # Cross back
            (0.08, 0.38), (0.10, 0.22),                 # Return
        ],
    },
    'championship': {
        'name': 'Championship Circuit',
        'description': 'Balanced layout for close racing',
        'points': [
            (0.18, 0.15), (0.48, 0.10), (0.78, 0.18),  # Main straight
            (0.90, 0.35), (0.85, 0.52),                 # Turn 1
            (0.70, 0.55), (0.58, 0.48),                 # Chicane
            (0.48, 0.58), (0.55, 0.72),                 # Hairpin
            (0.72, 0.80), (0.85, 0.75),                 # Back straight
            (0.90, 0.88), (0.72, 0.92),                 # Final complex
            (0.45, 0.88), (0.25, 0.82),                 # Penultimate
            (0.12, 0.68), (0.10, 0.48),                 # Stadium section
            (0.15, 0.30),                               # Return
        ],
    },
}


def generate_track_from_pattern(pattern_name, variation_amount=0.03):
    """
    Generate a track from a proven pattern with slight variations.
    
    Args:
        pattern_name: Key from LAYOUT_PATTERNS
        variation_amount: How much to vary points (0.0 = exact, 0.05 = moderate)
    
    Returns:
        tuple: (waypoints, style_name)
    """
    pattern = LAYOUT_PATTERNS[pattern_name]
    points = list(pattern['points'])
    
    # Apply small variations to make each track unique
    if variation_amount > 0:
        varied_points = []
        for x, y in points:
            # Add controlled randomness
            nx = x + random.uniform(-variation_amount, variation_amount)
            ny = y + random.uniform(-variation_amount, variation_amount)
            # Clamp to valid range
            nx = max(0.05, min(0.95, nx))
            ny = max(0.05, min(0.95, ny))
            varied_points.append((nx, ny))
        points = varied_points
    
    # Convert to canvas coordinates
    canvas_points = []
    for x, y in points:
        px = MARGIN + x * (CANVAS_WIDTH - 2 * MARGIN)
        py = MARGIN + y * (CANVAS_HEIGHT - 2 * MARGIN)
        canvas_points.append((px, py))
    
    # Generate smooth spline through points
    waypoints = catmull_rom_closed(canvas_points, points_per_segment=8)
    
    # Apply random rotation for variety
    angle = random.uniform(0, 2 * math.pi)
    waypoints = rotate_track(waypoints, angle)
    
    # Random mirror
    if random.choice([True, False]):
        waypoints = mirror_track(waypoints)
    
    # Center on canvas
    waypoints = center_track(waypoints)
    
    return waypoints, pattern_name


def catmull_rom_closed(points, points_per_segment=10):
    """Generate smooth closed curve through control points."""
    if len(points) < 3:
        return points
    
    result = []
    n = len(points)
    
    for i in range(n):
        p0 = points[(i - 1) % n]
        p1 = points[i]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n]
        
        for t_idx in range(points_per_segment):
            t = t_idx / points_per_segment
            t2 = t * t
            t3 = t2 * t
            
            x = 0.5 * ((2 * p1[0]) +
                      (-p0[0] + p2[0]) * t +
                      (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                      (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            
            y = 0.5 * ((2 * p1[1]) +
                      (-p0[1] + p2[1]) * t +
                      (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                      (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            
            result.append((int(x), int(y)))
    
    return result


def rotate_track(waypoints, angle):
    """Rotate track around its center."""
    if not waypoints:
        return waypoints
    
    # Find center
    cx = sum(p[0] for p in waypoints) / len(waypoints)
    cy = sum(p[1] for p in waypoints) / len(waypoints)
    
    result = []
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    for x, y in waypoints:
        # Translate to origin
        dx = x - cx
        dy = y - cy
        
        # Rotate
        nx = dx * cos_a - dy * sin_a
        ny = dx * sin_a + dy * cos_a
        
        # Translate back
        result.append((int(cx + nx), int(cy + ny)))
    
    return result


def mirror_track(waypoints):
    """Mirror track horizontally."""
    if not waypoints:
        return waypoints
    
    cx = sum(p[0] for p in waypoints) / len(waypoints)
    
    result = []
    for x, y in waypoints:
        nx = cx - (x - cx)
        result.append((int(nx), int(y)))
    
    return result


def center_track(waypoints):
    """Center track on canvas."""
    if not waypoints:
        return waypoints
    
    # Find bounds
    min_x = min(p[0] for p in waypoints)
    max_x = max(p[0] for p in waypoints)
    min_y = min(p[1] for p in waypoints)
    max_y = max(p[1] for p in waypoints)
    
    # Calculate offset to center
    track_cx = (min_x + max_x) / 2
    track_cy = (min_y + max_y) / 2
    
    canvas_cx = CANVAS_WIDTH / 2
    canvas_cy = CANVAS_HEIGHT / 2
    
    offset_x = canvas_cx - track_cx
    offset_y = canvas_cy - track_cy
    
    result = []
    for x, y in waypoints:
        result.append((int(x + offset_x), int(y + offset_y)))
    
    return result


def generate_name():
    """Generate a random F1-style track name."""
    locations = [
        'Valencia', 'Portimao', 'Kyoto', 'Dubai', 'Mumbai', 'Lagos',
        'Santiago', 'Vancouver', 'Stockholm', 'Prague', 'Vienna', 'Seoul',
        'Cairo', 'Lisbon', 'Warsaw', 'Helsinki', 'Oslo', 'Copenhagen',
        'Auckland', 'Perth', 'Taipei', 'Manila', 'Jakarta', 'Hanoi',
        'Marrakech', 'Doha', 'Riyadh', 'Baku', 'Sochi', 'Istanbul',
        'Zandvoort', 'Imola', 'Mugello', 'Portimao', 'Jerez', 'Estoril',
        'Sepang', 'Fuji', 'Suzuka', 'Yeongam', 'Buddh', 'Losail'
    ]
    
    suffixes = [
        'Grand Prix Circuit',
        'International Circuit', 
        'Street Circuit',
        'Autodrome',
        'Racing Circuit',
        'Motorsport Park',
        'Ring',
        'Raceway'
    ]
    
    return f"{random.choice(locations)} {random.choice(suffixes)}"


def save_template(waypoints, style, index):
    """Save template to JSON file."""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"template_{index:03d}_{timestamp}.json"
    filepath = os.path.join(TEMPLATES_DIR, filename)
    
    # Get style info
    pattern_info = LAYOUT_PATTERNS.get(style, {})
    
    data = {
        'name': generate_name(),
        'waypoints': waypoints,
        'style': pattern_info.get('name', style),
        'description': pattern_info.get('description', ''),
        'generated': timestamp,
        'num_waypoints': len(waypoints),
        'decorations': {
            'kerbs': [],
            'gravel': [],
            'grass': [],
            'start_line': None,
            'racing_line': False
        }
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filename, pattern_info.get('name', style)


def main():
    """Main entry point."""
    count = 10
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print(f"Invalid count: {sys.argv[1]}")
            print("Usage: python tools/generate_templates.py [count]")
            return
    
    print(f"Generating {count} track templates...")
    print(f"Output directory: {TEMPLATES_DIR}")
    print()
    
    pattern_names = list(LAYOUT_PATTERNS.keys())
    
    for i in range(count):
        # Cycle through patterns, with variations
        pattern = pattern_names[i % len(pattern_names)]
        
        # More variation for repeated patterns
        variation = 0.02 + (i // len(pattern_names)) * 0.01
        variation = min(variation, 0.05)  # Cap at 5%
        
        waypoints, style = generate_track_from_pattern(pattern, variation)
        filename, style_name = save_template(waypoints, style, i + 1)
        print(f"  [{i+1}/{count}] {filename} ({style_name}, {len(waypoints)} pts)")
    
    print()
    print(f"Done! Templates saved to {TEMPLATES_DIR}/")
    print("Load them in Track Studio: Press [1] then [B] to browse")


if __name__ == "__main__":
    main()
