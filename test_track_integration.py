"""
Test Track Characteristics Integration with Race Engine

Verifies that:
1. RaceEngine can create tracks with circuit_id
2. Track characteristics are properly applied to cars
3. Tire degradation multipliers work correctly
4. DRS zones are detected properly
5. Backward compatibility maintained (custom tracks still work)
"""

from race.race_engine import RaceEngine
from race.track import Track
import config


def test_circuit_integration():
    """Test RaceEngine integration with real F1 circuits"""
    print("=" * 70)
    print("TEST: Track Characteristics Integration with Race Engine")
    print("=" * 70)

    # Test 1: Create race engine with Monaco circuit
    print("\n1. Testing Monaco circuit creation...")
    race_monaco = RaceEngine(circuit_id="monaco")
    assert race_monaco.track.circuit_id == "monaco"
    assert race_monaco.track.is_real_f1_circuit() == True
    assert race_monaco.track.get_circuit_name() == "Circuit de Monaco"
    print("   ✓ Monaco circuit loaded successfully")
    print(f"   ✓ Circuit name: {race_monaco.track.get_circuit_name()}")
    print(f"   ✓ Location: {race_monaco.track.get_circuit_location()}")
    print(f"   ✓ Length: {race_monaco.track.get_circuit_length_km()} km")

    # Test 2: Verify tire degradation multiplier
    print("\n2. Testing tire degradation multipliers...")
    monaco_deg = race_monaco.track.get_tire_degradation_multiplier()
    print(f"   Monaco tire degradation: {monaco_deg}x (expected: 0.7x - low wear)")
    assert monaco_deg == 0.7, f"Expected 0.7, got {monaco_deg}"

    race_suzuka = RaceEngine(circuit_id="suzuka")
    suzuka_deg = race_suzuka.track.get_tire_degradation_multiplier()
    print(f"   Suzuka tire degradation: {suzuka_deg}x (expected: 1.4x - high wear)")
    assert suzuka_deg == 1.4, f"Expected 1.4, got {suzuka_deg}"

    print("   ✓ Tire degradation multipliers correct")

    # Test 3: Verify DRS zones
    print("\n3. Testing DRS zones...")
    monaco_drs = race_monaco.track.get_drs_zones()
    print(f"   Monaco DRS zones: {len(monaco_drs)} zone(s)")
    assert len(monaco_drs) == 1, f"Expected 1 DRS zone, got {len(monaco_drs)}"

    silverstone = RaceEngine(circuit_id="silverstone")
    silverstone_drs = silverstone.track.get_drs_zones()
    print(f"   Silverstone DRS zones: {len(silverstone_drs)} zone(s)")
    assert len(silverstone_drs) == 2, f"Expected 2 DRS zones, got {len(silverstone_drs)}"

    print("   ✓ DRS zones configured correctly")

    # Test 4: Verify cars receive track characteristics
    print("\n4. Testing car integration with track characteristics...")
    # Update race to populate car attributes
    race_monaco.start_race()
    race_monaco.update()

    # Check that cars have received track tire degradation multiplier
    test_car = race_monaco.cars[0]
    print(f"   Car tire degradation multiplier: {test_car.track_tire_deg_multiplier}x")
    assert test_car.track_tire_deg_multiplier == 0.7, \
        f"Expected car to receive 0.7x multiplier, got {test_car.track_tire_deg_multiplier}"
    print("   ✓ Cars receiving track tire degradation multiplier")

    # Test 5: Test DRS detection (simulate car close to another)
    print("\n5. Testing DRS detection integration...")
    # Set up scenario: car in position 2, within 1 second of car ahead, in DRS zone
    car1 = race_monaco.cars[0]  # Leader
    car2 = race_monaco.cars[1]  # P2

    # Move car2 into a DRS zone
    drs_zone = monaco_drs[0]
    car2.progress = (drs_zone["start"] + drs_zone["end"]) / 2  # Middle of DRS zone
    car2.position = 2
    car2.lap = 2  # DRS enabled from lap 2
    car2.gap_to_ahead_time = 0.5  # Within 1 second

    # Update to trigger DRS check
    race_monaco.update()

    # Verify DRS states
    assert car2.is_drs_available == True, "Car should have DRS available (within 1s)"
    assert car2.is_drs_active == True, "Car should have DRS active (in DRS zone)"
    print("   ✓ DRS detection working correctly")
    print(f"   ✓ Car 2 - DRS Available: {car2.is_drs_available}, DRS Active: {car2.is_drs_active}")

    # Test 6: Test backward compatibility with custom tracks
    print("\n6. Testing backward compatibility with custom tracks...")
    custom_waypoints = [(100, 100), (200, 200), (300, 100), (200, 50)]
    race_custom = RaceEngine(waypoints=custom_waypoints)

    assert race_custom.track.is_real_f1_circuit() == False
    assert race_custom.track.get_tire_degradation_multiplier() == 1.0  # Default
    assert len(race_custom.track.get_drs_zones()) == 0  # No DRS zones
    print("   ✓ Custom tracks still work with default characteristics")
    print("   ✓ Tire degradation: 1.0x (baseline)")
    print("   ✓ DRS zones: 0 (none)")

    # Test 7: Test all circuits
    print("\n7. Testing all F1 circuits...")
    circuits = ["monaco", "silverstone", "spa", "monza", "suzuka", "cota"]
    for circuit_id in circuits:
        race = RaceEngine(circuit_id=circuit_id)
        assert race.track.is_real_f1_circuit() == True
        assert race.track.get_circuit_name() is not None
        deg = race.track.get_tire_degradation_multiplier()
        drs = race.track.get_drs_zones()
        print(f"   ✓ {circuit_id.upper()}: {race.track.get_circuit_name()} - " +
              f"Deg: {deg}x, DRS zones: {len(drs)}")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED! ✓")
    print("=" * 70)
    print("\nIntegration Summary:")
    print("• RaceEngine accepts circuit_id parameter")
    print("• Track characteristics properly loaded from circuits.py")
    print("• Cars receive and apply tire degradation multipliers")
    print("• DRS zone detection working correctly")
    print("• Backward compatibility maintained for custom tracks")
    print("• All 6 F1 circuits functional")
    print("=" * 70)


if __name__ == "__main__":
    test_circuit_integration()
