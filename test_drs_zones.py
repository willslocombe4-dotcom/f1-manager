"""
Test script for DRS zones functionality
Verifies DRS detection, activation, and speed boost
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from race.track import Track
from race.car import Car
from data.teams import TEAMS_DATA
import config

def test_drs_zone_detection():
    """Test that tracks have DRS zones and detection works"""
    print("=" * 60)
    print("TEST 1: DRS Zone Detection")
    print("=" * 60)

    circuits = ["monaco", "silverstone", "spa", "monza", "suzuka", "cota"]

    for circuit_id in circuits:
        track = Track(circuit_id=circuit_id)
        drs_zones = track.get_drs_zones()

        print(f"\n{track.get_circuit_name()}:")
        print(f"  DRS Zones: {len(drs_zones)}")

        for i, zone in enumerate(drs_zones):
            print(f"    Zone {i+1}: {zone['start']:.2f} → {zone['end']:.2f}")

            # Test detection at start, middle, and end of zone
            start_pos = zone['start']
            middle_pos = (zone['start'] + zone['end']) / 2
            end_pos = zone['end']

            # Handle wrap-around zones
            if zone['start'] > zone['end']:
                middle_pos = (zone['start'] + 1.0 + zone['end']) / 2
                if middle_pos >= 1.0:
                    middle_pos -= 1.0

            # Test positions
            in_start = track.is_in_drs_zone(start_pos)
            in_middle = track.is_in_drs_zone(middle_pos)
            in_end = track.is_in_drs_zone(end_pos)

            print(f"      Start ({start_pos:.2f}): {'✓' if in_start else '✗'}")
            print(f"      Middle ({middle_pos:.2f}): {'✓' if in_middle else '✗'}")
            print(f"      End ({end_pos:.2f}): {'✓' if in_end else '✗'}")

            # Test outside zone
            outside_pos = (zone['end'] + 0.1) % 1.0
            if track.is_in_drs_zone(outside_pos):
                # If it's still in a zone, we're probably in another zone
                print(f"      Outside ({outside_pos:.2f}): In another zone")
            else:
                print(f"      Outside ({outside_pos:.2f}): ✓ (correctly outside)")

def test_drs_availability():
    """Test DRS availability based on gap to car ahead"""
    print("\n" + "=" * 60)
    print("TEST 2: DRS Availability (Gap Detection)")
    print("=" * 60)

    # Create a track (Monaco for testing)
    track = Track(circuit_id="monaco")

    # Create two test cars
    team_data = TEAMS_DATA[0]
    car1 = Car(team_data["drivers"][0], team_data, position=1)
    car2 = Car(team_data["drivers"][1], team_data, position=2)

    # Set up initial state
    car1.lap = 2  # DRS active from lap 2
    car2.lap = 2
    car1.progress = 0.5
    car2.progress = 0.48

    print(f"\nCar 1 (Leader): Lap {car1.lap}, Progress {car1.progress:.2f}")
    print(f"Car 2 (Following): Lap {car2.lap}, Progress {car2.progress:.2f}")

    # Test different gap scenarios
    test_gaps = [0.5, 0.9, 1.0, 1.1, 2.0]

    for gap in test_gaps:
        car2.gap_to_ahead_time = gap
        car2.update(track, total_race_laps=20)

        status = "AVAILABLE" if car2.is_drs_available else "NOT AVAILABLE"
        symbol = "✓" if car2.is_drs_available else "✗"
        print(f"  Gap {gap:.1f}s: DRS {status} {symbol}")

    # Test lap 1 (DRS should not be available)
    print("\nLap 1 Test (DRS should be disabled):")
    car2.lap = 1
    car2.gap_to_ahead_time = 0.5  # Within gap
    car2.update(track, total_race_laps=20)
    status = "NOT AVAILABLE" if not car2.is_drs_available else "AVAILABLE (ERROR!)"
    symbol = "✓" if not car2.is_drs_available else "✗"
    print(f"  Lap 1, Gap 0.5s: DRS {status} {symbol}")

def test_drs_activation():
    """Test DRS activation (available + in zone)"""
    print("\n" + "=" * 60)
    print("TEST 3: DRS Activation (Available + In Zone)")
    print("=" * 60)

    # Create a track with DRS zones (Silverstone has 2 zones)
    track = Track(circuit_id="silverstone")
    drs_zones = track.get_drs_zones()

    print(f"\nTrack: {track.get_circuit_name()}")
    print(f"DRS Zones: {len(drs_zones)}")

    # Create test car
    team_data = TEAMS_DATA[0]
    car = Car(team_data["drivers"][0], team_data, position=2)
    car.lap = 2
    car.gap_to_ahead_time = 0.8  # Within DRS detection window

    # Test at various progress points
    test_positions = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9]

    print(f"\nCar: P{car.position}, Lap {car.lap}, Gap {car.gap_to_ahead_time:.1f}s")
    print("\nDRS Status at different track positions:")

    for progress in test_positions:
        car.progress = progress
        car.update(track, total_race_laps=20)

        in_zone = track.is_in_drs_zone(progress)
        zone_str = "IN ZONE" if in_zone else "Outside zone"
        avail_str = "Available" if car.is_drs_available else "Not available"
        active_str = "ACTIVE ✓" if car.is_drs_active else "Inactive"

        print(f"  Progress {progress:.2f}: {zone_str:12} | {avail_str:14} | {active_str}")

def test_drs_speed_boost():
    """Test that DRS provides speed boost"""
    print("\n" + "=" * 60)
    print("TEST 4: DRS Speed Boost")
    print("=" * 60)

    track = Track(circuit_id="monza")  # Monza has long straights with DRS

    team_data = TEAMS_DATA[0]
    car = Car(team_data["drivers"][0], team_data, position=2)
    car.lap = 2
    car.gap_to_ahead_time = 0.5  # Within DRS window

    # Get a DRS zone
    drs_zones = track.get_drs_zones()
    if drs_zones:
        drs_zone = drs_zones[0]
        in_zone_progress = (drs_zone['start'] + drs_zone['end']) / 2
        outside_zone_progress = (drs_zone['end'] + 0.2) % 1.0

        print(f"\nTrack: {track.get_circuit_name()}")
        print(f"Testing with DRS Zone: {drs_zone['start']:.2f} → {drs_zone['end']:.2f}")
        print(f"DRS Speed Boost: +{config.DRS_SPEED_BOOST * 100:.1f}%")

        # Test pace WITHOUT DRS (outside zone)
        car.progress = outside_zone_progress
        car.update(track, total_race_laps=20)
        pace_without_drs = car.current_pace

        print(f"\nOutside DRS Zone (Progress {outside_zone_progress:.2f}):")
        print(f"  DRS Active: {car.is_drs_active}")
        print(f"  Pace: {pace_without_drs:.6f}")

        # Test pace WITH DRS (inside zone)
        car.progress = in_zone_progress
        car.update(track, total_race_laps=20)
        pace_with_drs = car.current_pace

        print(f"\nInside DRS Zone (Progress {in_zone_progress:.2f}):")
        print(f"  DRS Active: {car.is_drs_active}")
        print(f"  Pace: {pace_with_drs:.6f}")

        # Calculate actual boost
        if pace_without_drs > 0:
            boost_pct = ((pace_with_drs / pace_without_drs) - 1.0) * 100
            expected_boost = config.DRS_SPEED_BOOST * 100

            print(f"\nSpeed Comparison:")
            print(f"  Expected boost: +{expected_boost:.1f}%")
            print(f"  Actual boost: +{boost_pct:.1f}%")

            if abs(boost_pct - expected_boost) < 0.1:
                print(f"  Result: ✓ PASS (boost matches expected)")
            else:
                print(f"  Result: ✗ FAIL (boost doesn't match)")

def test_all_circuits_have_drs():
    """Verify all circuits have DRS zones defined"""
    print("\n" + "=" * 60)
    print("TEST 5: All Circuits Have DRS Zones")
    print("=" * 60)

    circuits = ["monaco", "silverstone", "spa", "monza", "suzuka", "cota"]

    all_pass = True
    for circuit_id in circuits:
        track = Track(circuit_id=circuit_id)
        drs_zones = track.get_drs_zones()

        has_drs = len(drs_zones) > 0
        status = "✓" if has_drs else "✗ MISSING"

        print(f"  {track.get_circuit_name():30} {len(drs_zones)} zone(s) {status}")

        if not has_drs:
            all_pass = False

    print(f"\n{'All circuits have DRS zones! ✓' if all_pass else 'Some circuits missing DRS zones! ✗'}")

def main():
    """Run all DRS tests"""
    print("\n" + "=" * 60)
    print("DRS ZONES FUNCTIONALITY TEST SUITE")
    print("=" * 60)

    try:
        test_all_circuits_have_drs()
        test_drs_zone_detection()
        test_drs_availability()
        test_drs_activation()
        test_drs_speed_boost()

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
