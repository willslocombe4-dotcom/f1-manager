"""
Visual Circuit Testing Script

This script validates circuit waypoints for visual accuracy and racing line quality.
Run this with: python main.py (then select each circuit and observe)

This automated script checks:
- Waypoint count and density
- Track bounds (fits in 1000x900 area)
- Closed loop verification
- DRS zone validity
- Track characteristics consistency
"""

import sys
from data.circuits import CIRCUITS, get_all_circuits


def validate_waypoints(circuit_id, waypoints):
    """Validate waypoint technical requirements"""
    issues = []

    # Check waypoint count (should be 65-150 for good visual quality)
    waypoint_count = len(waypoints)
    if waypoint_count < 50:
        issues.append(f"  ⚠️  Low waypoint count ({waypoint_count}) - may look jagged")
    elif waypoint_count > 200:
        issues.append(f"  ⚠️  High waypoint count ({waypoint_count}) - may impact performance")
    else:
        print(f"  ✓ Waypoint count: {waypoint_count} (good)")

    # Check bounds (should fit in 1000x900 track view area)
    x_coords = [w[0] for w in waypoints]
    y_coords = [w[1] for w in waypoints]

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Check if track fits in bounds (leave margins)
    if min_x < 50 or max_x > 950:
        issues.append(f"  ⚠️  X coordinates out of safe bounds: {min_x} to {max_x}")
    if min_y < 50 or max_y > 850:
        issues.append(f"  ⚠️  Y coordinates out of safe bounds: {min_y} to {max_y}")

    if not issues:
        print(f"  ✓ Bounds: X[{min_x}, {max_x}] Y[{min_y}, {max_y}] (fits well)")

    # Check track size (should use reasonable portion of screen)
    width = max_x - min_x
    height = max_y - min_y

    if width < 300 or height < 300:
        issues.append(f"  ⚠️  Track too small ({width}x{height}) - won't be visually impressive")
    else:
        print(f"  ✓ Track size: {width}x{height} pixels (good)")

    # Check for closed loop (first and last waypoints should be close)
    first = waypoints[0]
    last = waypoints[-1]
    distance = ((last[0] - first[0])**2 + (last[1] - first[1])**2)**0.5

    if distance > 100:
        issues.append(f"  ⚠️  Track not properly closed (gap: {distance:.1f}px)")
    else:
        print(f"  ✓ Closed loop: gap {distance:.1f}px (good)")

    return issues


def validate_drs_zones(circuit_id, drs_zones):
    """Validate DRS zone configuration"""
    issues = []

    for i, zone in enumerate(drs_zones):
        start = zone.get('start', 0)
        end = zone.get('end', 0)

        # Check valid range (0.0 to 1.0)
        if not (0.0 <= start <= 1.0 and 0.0 <= end <= 1.0):
            issues.append(f"  ⚠️  DRS zone {i+1} out of range: {start} to {end}")

        # Check that end > start (unless wrapping around)
        if start >= end:
            # Could be wrapping around start/finish
            if not (start > 0.9 and end < 0.1):
                issues.append(f"  ⚠️  DRS zone {i+1} invalid: start ({start}) >= end ({end})")

        # Check reasonable length (should be 0.05 to 0.3 of track)
        length = end - start if end > start else (1.0 - start + end)
        if length < 0.03:
            issues.append(f"  ⚠️  DRS zone {i+1} too short ({length*100:.1f}% of lap)")
        elif length > 0.4:
            issues.append(f"  ⚠️  DRS zone {i+1} too long ({length*100:.1f}% of lap)")

    if not issues:
        print(f"  ✓ DRS zones: {len(drs_zones)} configured correctly")

    return issues


def check_circuit_characteristics(circuit_id, circuit):
    """Verify circuit characteristics are realistic"""
    issues = []

    characteristics = circuit.get('characteristics', {})

    # Tire degradation should be 0.7 to 1.4
    tire_deg = characteristics.get('tire_degradation', 1.0)
    if not (0.6 <= tire_deg <= 1.5):
        issues.append(f"  ⚠️  Tire degradation unrealistic: {tire_deg}")
    else:
        deg_label = "low" if tire_deg < 0.9 else "medium" if tire_deg < 1.1 else "high"
        print(f"  ✓ Tire degradation: {tire_deg} ({deg_label})")

    # Overtaking difficulty
    overtaking = characteristics.get('overtaking_difficulty', 'medium')
    valid_difficulties = ['very_high', 'high', 'medium', 'low', 'very_low']
    if overtaking not in valid_difficulties:
        issues.append(f"  ⚠️  Invalid overtaking difficulty: {overtaking}")
    else:
        print(f"  ✓ Overtaking: {overtaking}")

    return issues


def print_visual_testing_guide(circuit_id, circuit):
    """Print what to look for when visually testing this circuit"""
    print(f"\n  📋 VISUAL TESTING CHECKLIST:")

    # Famous corners to verify
    famous = circuit.get('famous_corners', [])
    if famous:
        print(f"  - Look for these iconic corners:")
        for corner in famous:
            print(f"    • {corner['name']}: {corner['description']}")

    # Circuit type specific checks
    circuit_type = circuit.get('type', 'unknown')
    if circuit_type == 'street':
        print(f"  - Should look like a street circuit (tight, technical)")
    else:
        print(f"  - Should look like a permanent circuit (flowing, wider)")

    # Track characteristics
    characteristics = circuit.get('characteristics', {})
    overtaking = characteristics.get('overtaking_difficulty', 'medium')
    if overtaking in ['very_high', 'high']:
        print(f"  - Few long straights (difficult overtaking)")
    else:
        print(f"  - Should have long straights for overtaking")

    # DRS zones
    drs_zones = circuit.get('drs_zones', [])
    print(f"  - Verify {len(drs_zones)} DRS zone(s) on straights")


def test_circuit(circuit_id):
    """Comprehensive test for a single circuit"""
    print(f"\n{'='*70}")
    print(f"🏁 Testing: {circuit_id.upper()}")
    print(f"{'='*70}")

    circuit = CIRCUITS.get(circuit_id)
    if not circuit:
        print(f"❌ Circuit '{circuit_id}' not found!")
        return False

    print(f"\n📍 {circuit['name']} - {circuit['location']}")
    print(f"📏 Length: {circuit['length_km']} km")
    print(f"🏎️  Type: {circuit['type'].title()} Circuit")

    all_issues = []

    # Test waypoints
    print(f"\n🔍 WAYPOINT VALIDATION:")
    waypoints = circuit.get('waypoints', [])
    issues = validate_waypoints(circuit_id, waypoints)
    all_issues.extend(issues)

    # Test DRS zones
    print(f"\n🚀 DRS ZONE VALIDATION:")
    drs_zones = circuit.get('drs_zones', [])
    issues = validate_drs_zones(circuit_id, drs_zones)
    all_issues.extend(issues)

    # Test characteristics
    print(f"\n⚙️  CHARACTERISTICS VALIDATION:")
    issues = check_circuit_characteristics(circuit_id, circuit)
    all_issues.extend(issues)

    # Visual testing guide
    print_visual_testing_guide(circuit_id, circuit)

    # Summary
    print(f"\n{'─'*70}")
    if all_issues:
        print(f"❌ VALIDATION FAILED - {len(all_issues)} issues found:")
        for issue in all_issues:
            print(issue)
        return False
    else:
        print(f"✅ VALIDATION PASSED - Circuit data is technically correct")
        print(f"👀 Manual visual testing still required (run game and select this circuit)")
        return True


def main():
    """Test all circuits"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                   F1 CIRCUIT VISUAL TESTING                      ║
║                                                                  ║
║  This script validates circuit waypoints for technical          ║
║  correctness. For full visual accuracy testing, you must        ║
║  run the game and observe each circuit.                         ║
╚══════════════════════════════════════════════════════════════════╝
""")

    all_circuits = get_all_circuits()
    print(f"Testing {len(all_circuits)} circuits...\n")

    results = {}
    for circuit_id in all_circuits:
        passed = test_circuit(circuit_id)
        results[circuit_id] = passed

    # Final summary
    print(f"\n\n{'='*70}")
    print(f"📊 FINAL SUMMARY")
    print(f"{'='*70}\n")

    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    for circuit_id, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {circuit_id.upper()}")

    print(f"\n{'─'*70}")
    print(f"Results: {passed_count}/{total_count} circuits passed technical validation")

    if passed_count == total_count:
        print(f"\n✅ All circuits technically validated!")
        print(f"\n📝 NEXT STEPS FOR VISUAL TESTING:")
        print(f"   1. Run: python main.py")
        print(f"   2. Select each circuit from the track selection screen")
        print(f"   3. Verify the track shape looks accurate and recognizable")
        print(f"   4. Check that famous corners are visually identifiable")
        print(f"   5. Ensure the racing line flows naturally")
        print(f"   6. Observe cars racing for 2-3 laps to verify smoothness")
        return 0
    else:
        print(f"\n❌ Some circuits failed validation - fix issues before visual testing")
        return 1


if __name__ == '__main__':
    sys.exit(main())
