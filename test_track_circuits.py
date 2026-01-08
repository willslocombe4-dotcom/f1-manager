"""
Test script for Track class circuit metadata support
Run this with: python test_track_circuits.py
"""
from race.track import Track
from data.circuits import get_all_circuits


def test_default_track():
    """Test default track (no circuit_id)"""
    print("Test 1: Default track")
    default_track = Track()
    assert default_track.is_real_f1_circuit() == False
    assert default_track.get_tire_degradation_multiplier() == 1.0
    assert default_track.get_drs_zones() == []
    assert default_track.get_circuit_name() is None
    print("  ✓ Default track works correctly")


def test_monaco_circuit():
    """Test Monaco circuit"""
    print("\nTest 2: Monaco circuit")
    monaco = Track(circuit_id='monaco')
    assert monaco.is_real_f1_circuit() == True
    assert monaco.get_circuit_name() == "Circuit de Monaco"
    assert monaco.get_circuit_location() == "Monte Carlo, Monaco"
    assert monaco.get_circuit_length_km() == 3.337
    assert monaco.get_circuit_type() == "street"
    assert monaco.get_tire_degradation_multiplier() == 0.7
    assert len(monaco.get_drs_zones()) == 1
    assert monaco.is_in_drs_zone(0.04) == True
    assert monaco.is_in_drs_zone(0.5) == False
    assert len(monaco.get_famous_corners()) == 5
    print(f"  ✓ Monaco: {monaco.get_circuit_name()}")
    print(f"    - {len(monaco.waypoints)} waypoints")
    print(f"    - Tire degradation: {monaco.get_tire_degradation_multiplier()}")
    print(f"    - {len(monaco.get_drs_zones())} DRS zone(s)")


def test_silverstone_circuit():
    """Test Silverstone circuit"""
    print("\nTest 3: Silverstone circuit")
    silverstone = Track(circuit_id='silverstone')
    assert silverstone.get_circuit_name() == "Silverstone Circuit"
    assert silverstone.get_tire_degradation_multiplier() == 1.3
    assert len(silverstone.get_drs_zones()) == 2
    print(f"  ✓ Silverstone: {silverstone.get_circuit_name()}")
    print(f"    - Tire degradation: {silverstone.get_tire_degradation_multiplier()}")
    print(f"    - {len(silverstone.get_drs_zones())} DRS zones")


def test_all_circuits():
    """Test that all circuits can be loaded"""
    print("\nTest 4: All circuits")
    for circuit_id in get_all_circuits():
        track = Track(circuit_id=circuit_id)
        assert track.is_real_f1_circuit() == True
        assert track.get_circuit_name() is not None
        assert len(track.waypoints) > 0
        print(f"  ✓ {circuit_id}: {track.get_circuit_name()} ({len(track.waypoints)} waypoints)")


def test_custom_waypoints_override():
    """Test that custom waypoints can still override circuit waypoints"""
    print("\nTest 5: Custom waypoints override")
    custom_waypoints = [(100, 100), (200, 200), (300, 100)]
    track = Track(waypoints=custom_waypoints, circuit_id='monaco')
    assert track.waypoints == custom_waypoints
    assert track.get_circuit_name() == "Circuit de Monaco"  # Metadata still available
    print("  ✓ Custom waypoints override circuit waypoints while keeping metadata")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Track class circuit metadata support")
    print("=" * 60)

    test_default_track()
    test_monaco_circuit()
    test_silverstone_circuit()
    test_all_circuits()
    test_custom_waypoints_override()

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
