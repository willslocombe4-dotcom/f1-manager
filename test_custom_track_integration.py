"""
Test script to verify custom track editor integration works with F1 circuits

This test ensures:
1. Custom tracks can be loaded from the tracks directory
2. Track selection screen shows both F1 circuits and custom tracks
3. Custom tracks can be selected and loaded with waypoints/decorations
4. Track class can be instantiated with custom waypoints
5. All track types (F1, default, custom) work together
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from race.track_loader import get_available_tracks, load_track_with_decorations, get_default_waypoints
from race.track import Track
from data.circuits import get_all_circuits, get_circuit_by_id
from ui.track_selection import TrackSelectionScreen


def test_custom_track_loading():
    """Test 1: Verify custom tracks can be loaded from directory"""
    print("=" * 70)
    print("TEST 1: Custom Track Loading")
    print("=" * 70)

    custom_tracks = get_available_tracks()

    print(f"\nFound {len(custom_tracks)} custom track(s) in tools/tracks/")

    for i, track in enumerate(custom_tracks, 1):
        print(f"\n{i}. {track['name']}")
        print(f"   File: {track['filepath']}")
        print(f"   Waypoints: {track['num_waypoints']}")

        # Try loading waypoints and decorations
        waypoints, decorations = load_track_with_decorations(track['filepath'])

        if waypoints:
            print(f"   ✓ Successfully loaded {len(waypoints)} waypoints")
            print(f"   ✓ Decorations: {len(decorations.get('kerbs', []))} kerbs, {len(decorations.get('gravel', []))} gravel")
        else:
            print(f"   ✗ Failed to load waypoints")
            return False

    if len(custom_tracks) == 0:
        print("\n⚠️  No custom tracks found (this is OK, but creating one would help test)")
        return True

    print("\n✓ Custom track loading: PASSED")
    return True


def test_track_selection_integration():
    """Test 2: Verify track selection screen integrates F1 circuits and custom tracks"""
    print("\n" + "=" * 70)
    print("TEST 2: Track Selection Screen Integration")
    print("=" * 70)

    # Initialize pygame for TrackSelectionScreen
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))

    # Create track selection screen
    track_selection = TrackSelectionScreen(screen)

    print(f"\nTotal tracks available: {len(track_selection.tracks)}")

    # Count track types
    f1_circuits = sum(1 for t in track_selection.tracks if t.get('is_f1_circuit'))
    default_track = sum(1 for t in track_selection.tracks if t.get('is_default'))
    custom_tracks = sum(1 for t in track_selection.tracks if not t.get('is_f1_circuit') and not t.get('is_default'))

    print(f"\nTrack breakdown:")
    print(f"  - F1 Circuits: {f1_circuits}")
    print(f"  - Default Track: {default_track}")
    print(f"  - Custom Tracks: {custom_tracks}")

    # Verify F1 circuits
    print("\nF1 Circuits:")
    for track in track_selection.tracks:
        if track.get('is_f1_circuit'):
            print(f"  • {track['name']} ({track.get('location', 'Unknown')})")

    # Verify custom tracks
    if custom_tracks > 0:
        print("\nCustom Tracks:")
        for track in track_selection.tracks:
            if not track.get('is_f1_circuit') and not track.get('is_default'):
                print(f"  • {track['name']} ({track['num_waypoints']} waypoints)")

    # Test that custom tracks have correct attributes
    for track in track_selection.tracks:
        if not track.get('is_f1_circuit') and not track.get('is_default'):
            assert track.get('circuit_id') is None, "Custom tracks should not have circuit_id"
            assert track.get('filepath') is not None, "Custom tracks should have filepath"

    pygame.quit()

    print("\n✓ Track selection integration: PASSED")
    return True


def test_custom_track_instantiation():
    """Test 3: Verify Track class can be instantiated with custom waypoints"""
    print("\n" + "=" * 70)
    print("TEST 3: Custom Track Instantiation")
    print("=" * 70)

    # Test with default waypoints
    print("\n1. Testing with default waypoints...")
    default_waypoints = get_default_waypoints()
    track_default = Track(waypoints=default_waypoints)
    print(f"   ✓ Created track with {len(track_default.waypoints)} default waypoints")
    assert track_default.circuit_id is None
    assert track_default.circuit_data is None
    print("   ✓ No circuit_id (as expected)")

    # Test with custom track waypoints (if any exist)
    custom_tracks = get_available_tracks()
    if custom_tracks:
        print(f"\n2. Testing with custom track waypoints...")
        track_info = custom_tracks[0]
        waypoints, decorations = load_track_with_decorations(track_info['filepath'])

        if waypoints:
            track_custom = Track(waypoints=waypoints, decorations=decorations)
            print(f"   ✓ Created track with {len(track_custom.waypoints)} custom waypoints")
            print(f"   ✓ Decorations loaded: {len(track_custom.decorations.get('kerbs', []))} kerbs, {len(track_custom.decorations.get('gravel', []))} gravel")
            assert track_custom.circuit_id is None
            assert track_custom.circuit_data is None
            print("   ✓ No circuit_id (as expected)")

            # Test getting position on custom track
            test_progress = 0.5
            pos = track_custom.get_position(test_progress)
            print(f"   ✓ get_position({test_progress}) = {pos}")
    else:
        print(f"\n2. No custom tracks to test (skipped)")

    # Test with F1 circuit
    print(f"\n3. Testing with F1 circuit...")
    track_f1 = Track(circuit_id='monaco')
    print(f"   ✓ Created Monaco circuit with {len(track_f1.waypoints)} waypoints")
    assert track_f1.circuit_id == 'monaco'
    assert track_f1.circuit_data is not None
    print(f"   ✓ Circuit metadata loaded: {track_f1.get_circuit_name()}")

    print("\n✓ Custom track instantiation: PASSED")
    return True


def test_track_selection_workflow():
    """Test 4: Simulate full track selection workflow"""
    print("\n" + "=" * 70)
    print("TEST 4: Track Selection Workflow Simulation")
    print("=" * 70)

    custom_tracks = get_available_tracks()

    if not custom_tracks:
        print("\n⚠️  No custom tracks found - skipping workflow test")
        print("   (To fully test, create a track with tools/track_editor.py)")
        return True

    # Simulate selecting a custom track
    track_info = custom_tracks[0]
    print(f"\nSimulating selection of custom track: '{track_info['name']}'")

    # Load waypoints and decorations (as track selection screen would)
    waypoints, decorations = load_track_with_decorations(track_info['filepath'])

    if waypoints is None:
        print("   ✗ Failed to load track")
        return False

    print(f"   ✓ Loaded {len(waypoints)} waypoints")
    print(f"   ✓ Loaded decorations: {decorations}")

    # Create Track instance (as race engine would)
    track = Track(waypoints=waypoints, decorations=decorations)

    print(f"   ✓ Track instance created")
    print(f"   ✓ Track length: {track.track_length}")
    print(f"   ✓ Is real F1 circuit: {track.is_real_f1_circuit()}")

    # Verify track methods work
    test_pos = track.get_position(0.0)
    print(f"   ✓ get_position(0.0) = {test_pos}")

    test_pos = track.get_position(0.5)
    print(f"   ✓ get_position(0.5) = {test_pos}")

    print("\n✓ Track selection workflow: PASSED")
    return True


def test_backward_compatibility():
    """Test 5: Verify backward compatibility with existing features"""
    print("\n" + "=" * 70)
    print("TEST 5: Backward Compatibility")
    print("=" * 70)

    print("\nTesting various track initialization methods:")

    # Method 1: No parameters (default track)
    print("\n1. Track() - default circuit")
    track1 = Track()
    print(f"   ✓ Created with {len(track1.waypoints)} waypoints")

    # Method 2: circuit_id only (F1 circuit)
    print("\n2. Track(circuit_id='silverstone') - F1 circuit")
    track2 = Track(circuit_id='silverstone')
    print(f"   ✓ Created Silverstone with {len(track2.waypoints)} waypoints")
    print(f"   ✓ {track2.get_circuit_name()}")

    # Method 3: Custom waypoints only
    print("\n3. Track(waypoints=custom) - custom track")
    custom_wp = [(100, 100), (200, 100), (200, 200), (100, 200)]
    track3 = Track(waypoints=custom_wp)
    print(f"   ✓ Created with {len(track3.waypoints)} waypoints")

    # Method 4: Custom waypoints + decorations
    print("\n4. Track(waypoints=custom, decorations=deco) - custom with decorations")
    decorations = {'kerbs': [{'boundary': 'left', 'start': 0, 'end': 2}], 'gravel': []}
    track4 = Track(waypoints=custom_wp, decorations=decorations)
    print(f"   ✓ Created with {len(track4.waypoints)} waypoints and decorations")
    print(f"   ✓ Decorations: {track4.decorations}")

    print("\n✓ Backward compatibility: PASSED")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("CUSTOM TRACK EDITOR INTEGRATION TEST")
    print("Testing backward compatibility with F1 circuits")
    print("=" * 70)

    tests = [
        test_custom_track_loading,
        test_track_selection_integration,
        test_custom_track_instantiation,
        test_track_selection_workflow,
        test_backward_compatibility,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ TEST FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(results)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✓ ALL TESTS PASSED")
        print("\nCustom track editor integration is working correctly!")
        print("F1 circuits and custom tracks coexist seamlessly.")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
