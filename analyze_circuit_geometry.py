"""
Circuit Geometry Analysis

Analyzes waypoint geometry to predict visual quality without running the game.
Checks for smoothness, density, and potential visual issues.
"""

import math
from data.circuits import CIRCUITS, get_all_circuits


def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def calculate_angle_change(p1, p2, p3):
    """Calculate angle change between three consecutive points (in degrees)"""
    # Vector 1: p1 to p2
    v1x, v1y = p2[0] - p1[0], p2[1] - p1[1]
    # Vector 2: p2 to p3
    v2x, v2y = p3[0] - p2[0], p3[1] - p2[1]

    # Calculate angle using dot product and cross product
    dot = v1x * v2x + v1y * v2y
    cross = v1x * v2y - v1y * v2x

    angle = math.atan2(cross, dot)
    return abs(math.degrees(angle))


def analyze_waypoint_smoothness(waypoints):
    """Analyze how smooth the waypoint transitions are"""
    if len(waypoints) < 3:
        return {"smooth": False, "issues": ["Too few waypoints"]}

    issues = []
    max_angle_change = 0
    sharp_corners = 0
    total_angle_change = 0

    # Analyze angle changes between consecutive waypoints
    for i in range(len(waypoints)):
        p1 = waypoints[i]
        p2 = waypoints[(i + 1) % len(waypoints)]
        p3 = waypoints[(i + 2) % len(waypoints)]

        angle_change = calculate_angle_change(p1, p2, p3)
        total_angle_change += angle_change

        if angle_change > max_angle_change:
            max_angle_change = angle_change

        # Sharp corner detection (>45 degrees)
        if angle_change > 45:
            sharp_corners += 1

    avg_angle_change = total_angle_change / len(waypoints)

    # Identify issues
    if max_angle_change > 90:
        issues.append(f"Very sharp corner detected ({max_angle_change:.1f}° - may look jagged)")
    if sharp_corners > len(waypoints) * 0.3:
        issues.append(f"Many sharp corners ({sharp_corners}) - track may look angular")
    if avg_angle_change < 5:
        issues.append(f"Very gentle curves ({avg_angle_change:.1f}° avg) - may need fewer waypoints")

    return {
        "smooth": len(issues) == 0,
        "max_angle": max_angle_change,
        "avg_angle": avg_angle_change,
        "sharp_corners": sharp_corners,
        "issues": issues
    }


def analyze_waypoint_spacing(waypoints):
    """Analyze consistency of waypoint spacing"""
    if len(waypoints) < 2:
        return {"consistent": False, "issues": ["Too few waypoints"]}

    distances = []
    for i in range(len(waypoints)):
        p1 = waypoints[i]
        p2 = waypoints[(i + 1) % len(waypoints)]
        dist = calculate_distance(p1, p2)
        distances.append(dist)

    avg_distance = sum(distances) / len(distances)
    min_distance = min(distances)
    max_distance = max(distances)

    # Calculate variance
    variance = sum((d - avg_distance)**2 for d in distances) / len(distances)
    std_dev = math.sqrt(variance)

    issues = []

    # Check for very inconsistent spacing
    if max_distance > avg_distance * 3:
        issues.append(f"Very inconsistent spacing (max {max_distance:.1f}px vs avg {avg_distance:.1f}px)")

    # Check for too-close waypoints
    if min_distance < 5:
        issues.append(f"Waypoints too close together ({min_distance:.1f}px) - redundant")

    # Check for too-far waypoints
    if max_distance > 100:
        issues.append(f"Waypoints too far apart ({max_distance:.1f}px) - may cause jagged appearance")

    # Check for high variance
    if std_dev > avg_distance * 0.5:
        issues.append(f"High spacing variance (σ={std_dev:.1f}) - inconsistent visual quality")

    return {
        "consistent": len(issues) == 0,
        "avg_distance": avg_distance,
        "min_distance": min_distance,
        "max_distance": max_distance,
        "std_dev": std_dev,
        "issues": issues
    }


def analyze_track_shape(waypoints):
    """Analyze overall track shape characteristics"""
    x_coords = [w[0] for w in waypoints]
    y_coords = [w[1] for w in waypoints]

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    width = max_x - min_x
    height = max_y - min_y

    # Calculate track perimeter (approximate)
    perimeter = sum(
        calculate_distance(waypoints[i], waypoints[(i+1) % len(waypoints)])
        for i in range(len(waypoints))
    )

    # Calculate compactness (area vs perimeter)
    area = width * height
    compactness = (4 * math.pi * area) / (perimeter ** 2) if perimeter > 0 else 0

    return {
        "center": (center_x, center_y),
        "bounds": {"x": (min_x, max_x), "y": (min_y, max_y)},
        "size": {"width": width, "height": height},
        "perimeter": perimeter,
        "compactness": compactness,  # 1.0 = perfect circle, <1.0 = elongated
    }


def predict_visual_quality(circuit_id):
    """Predict visual quality based on waypoint geometry"""
    print(f"\n{'='*70}")
    print(f"🔬 Geometric Analysis: {circuit_id.upper()}")
    print(f"{'='*70}")

    circuit = CIRCUITS.get(circuit_id)
    if not circuit:
        print(f"❌ Circuit not found")
        return

    waypoints = circuit.get('waypoints', [])

    # Overall info
    print(f"\n📊 Basic Statistics:")
    print(f"   Waypoint count: {len(waypoints)}")

    # Analyze shape
    shape = analyze_track_shape(waypoints)
    print(f"   Track size: {shape['size']['width']:.0f} x {shape['size']['height']:.0f} pixels")
    print(f"   Track perimeter: {shape['perimeter']:.0f} pixels")
    print(f"   Compactness: {shape['compactness']:.2f} (1.0 = circular, 0.0 = very elongated)")

    # Determine track character from compactness
    if shape['compactness'] > 0.6:
        track_char = "Compact/circular layout (e.g., Monaco-style)"
    elif shape['compactness'] > 0.3:
        track_char = "Balanced layout (e.g., Silverstone-style)"
    else:
        track_char = "Elongated layout (e.g., Spa-style)"
    print(f"   → {track_char}")

    all_issues = []

    # Analyze smoothness
    print(f"\n🌊 Smoothness Analysis:")
    smoothness = analyze_waypoint_smoothness(waypoints)
    print(f"   Max angle change: {smoothness['max_angle']:.1f}°")
    print(f"   Avg angle change: {smoothness['avg_angle']:.1f}°")
    print(f"   Sharp corners (>45°): {smoothness['sharp_corners']}")

    if smoothness['smooth']:
        print(f"   ✅ Track appears smooth")
    else:
        print(f"   ⚠️  Potential smoothness issues:")
        for issue in smoothness['issues']:
            print(f"      • {issue}")
        all_issues.extend(smoothness['issues'])

    # Analyze spacing
    print(f"\n📏 Waypoint Spacing Analysis:")
    spacing = analyze_waypoint_spacing(waypoints)
    print(f"   Average spacing: {spacing['avg_distance']:.1f} pixels")
    print(f"   Min spacing: {spacing['min_distance']:.1f} pixels")
    print(f"   Max spacing: {spacing['max_distance']:.1f} pixels")
    print(f"   Std deviation: {spacing['std_dev']:.1f} pixels")

    if spacing['consistent']:
        print(f"   ✅ Spacing is consistent")
    else:
        print(f"   ⚠️  Potential spacing issues:")
        for issue in spacing['issues']:
            print(f"      • {issue}")
        all_issues.extend(spacing['issues'])

    # Visual quality prediction
    print(f"\n🎨 Visual Quality Prediction:")

    quality_score = 0

    # Waypoint count (optimal: 70-120)
    wp_count = len(waypoints)
    if 70 <= wp_count <= 120:
        quality_score += 3
        print(f"   ✓ Good waypoint count ({wp_count})")
    elif 50 <= wp_count < 70 or 120 < wp_count <= 150:
        quality_score += 2
        print(f"   ○ Acceptable waypoint count ({wp_count})")
    else:
        quality_score += 1
        print(f"   ⚠ Suboptimal waypoint count ({wp_count})")

    # Smoothness
    if smoothness['max_angle'] < 60:
        quality_score += 3
        print(f"   ✓ Smooth curves (max {smoothness['max_angle']:.1f}°)")
    elif smoothness['max_angle'] < 90:
        quality_score += 2
        print(f"   ○ Moderately smooth (max {smoothness['max_angle']:.1f}°)")
    else:
        quality_score += 1
        print(f"   ⚠ Some sharp angles (max {smoothness['max_angle']:.1f}°)")

    # Spacing consistency
    if spacing['std_dev'] < spacing['avg_distance'] * 0.3:
        quality_score += 3
        print(f"   ✓ Very consistent spacing")
    elif spacing['std_dev'] < spacing['avg_distance'] * 0.5:
        quality_score += 2
        print(f"   ○ Reasonably consistent spacing")
    else:
        quality_score += 1
        print(f"   ⚠ Inconsistent spacing")

    # Final score (out of 9)
    print(f"\n   Overall Quality Score: {quality_score}/9")

    if quality_score >= 8:
        quality_rating = "EXCELLENT ⭐⭐⭐"
        prediction = "Should look very smooth and professional"
    elif quality_score >= 6:
        quality_rating = "GOOD ⭐⭐"
        prediction = "Should look good, minor imperfections possible"
    elif quality_score >= 4:
        quality_rating = "ACCEPTABLE ⭐"
        prediction = "Will work but may have visual roughness"
    else:
        quality_rating = "NEEDS IMPROVEMENT"
        prediction = "Likely to have visual issues - consider revising waypoints"

    print(f"   Rating: {quality_rating}")
    print(f"   Prediction: {prediction}")

    return len(all_issues) == 0


def main():
    """Analyze all circuits"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              CIRCUIT GEOMETRY ANALYSIS                           ║
║                                                                  ║
║  Analyzing waypoint geometry to predict visual quality          ║
╚══════════════════════════════════════════════════════════════════╝
""")

    all_circuits = get_all_circuits()
    results = {}

    for circuit_id in all_circuits:
        passed = predict_visual_quality(circuit_id)
        results[circuit_id] = passed

    # Summary
    print(f"\n\n{'='*70}")
    print(f"📊 GEOMETRIC ANALYSIS SUMMARY")
    print(f"{'='*70}\n")

    for circuit_id, passed in results.items():
        status = "✅ NO ISSUES" if passed else "⚠️  HAS ISSUES"
        print(f"{status} - {circuit_id.upper()}")

    issues_count = sum(1 for v in results.values() if not v)

    if issues_count == 0:
        print(f"\n✅ All circuits have good geometry!")
        print(f"\n📝 Ready for visual testing - run the game and verify each circuit")
    else:
        print(f"\n⚠️  {issues_count} circuit(s) have geometric issues")
        print(f"   Review issues above and consider adjusting waypoints")


if __name__ == '__main__':
    main()
