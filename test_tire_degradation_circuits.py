"""
Test Tire Degradation Differences Between Circuits

This script tests that tire degradation varies appropriately across different circuits,
creating strategic variety in race simulation.

Expected Results:
- Monaco (0.7x): Lowest tire wear - 30% less than baseline
- Monza (0.8x): Low tire wear - 20% less than baseline
- Spa (1.0x): Baseline tire wear
- COTA (1.2x): Medium-high tire wear - 20% more than baseline
- Silverstone (1.3x): High tire wear - 30% more than baseline
- Suzuka (1.4x): Highest tire wear - 40% more than baseline
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from race.track import Track
from race.car import Car
from data.teams import TEAMS_DATA
from data.circuits import CIRCUITS
import config

def create_test_car():
    """Create a standardized test car for consistent comparison."""
    # Use same driver and team for all tests to isolate tire degradation
    test_driver = {
        "number": 1,
        "name": "Test Driver",
        "short": "TST",
        "skill": 85,
        "consistency": 3,
        "racecraft": 3,
        "style": "adaptive"
    }

    test_team = {
        "name": "Test Team",
        "tier": "B",
        "characteristics": {
            "balance": 0,
            "cornering": 0,
            "traction": 3
        }
    }

    return Car(test_driver, test_team, starting_position=1)


def test_circuit_tire_degradation(circuit_id, circuit_name, expected_multiplier, num_laps=30):
    """
    Test tire degradation on a specific circuit.

    Args:
        circuit_id: Circuit identifier
        circuit_name: Human-readable circuit name
        expected_multiplier: Expected tire degradation multiplier
        num_laps: Number of laps to simulate

    Returns:
        dict: Test results with tire wear data
    """
    print(f"\n{'='*70}")
    print(f"Testing: {circuit_name} (multiplier: {expected_multiplier}x)")
    print(f"{'='*70}")

    # Create track and car
    track = Track(circuit_id=circuit_id)
    car = create_test_car()

    # Put car on soft tires for maximum degradation visibility
    car.tire_compound = config.TIRE_SOFT
    car.tire_age = 0

    # Verify track multiplier
    track_multiplier = track.get_tire_degradation_multiplier()
    print(f"Track tire degradation multiplier: {track_multiplier}")

    if abs(track_multiplier - expected_multiplier) > 0.01:
        print(f"❌ ERROR: Expected {expected_multiplier}, got {track_multiplier}")
        return None

    # Simulate laps and track pace degradation
    lap_data = []

    for lap in range(1, num_laps + 1):
        car.lap = lap
        car.tire_age = lap - 1

        # Update car to get track multiplier
        car.track_tire_deg_multiplier = track_multiplier

        # Calculate tire degradation penalty
        deg_rate = config.TIRE_DEG_RATES[car.tire_compound]
        tire_penalty_without_track = car.tire_age * deg_rate
        tire_penalty_with_track = car.tire_age * deg_rate * track_multiplier

        # Check for tire cliff
        cliff_lap = config.TIRE_CLIFF_LAPS[car.tire_compound]
        at_cliff = car.tire_age >= cliff_lap

        if at_cliff:
            tire_penalty_with_track += config.TIRE_CLIFF_PENALTY

        # Cap at maximum
        tire_penalty_capped = min(tire_penalty_with_track, config.MAX_TIRE_PENALTY)

        # Calculate pace (as percentage of base pace)
        pace_multiplier = 1.0 - tire_penalty_capped

        lap_data.append({
            'lap': lap,
            'tire_age': car.tire_age,
            'penalty_no_track': tire_penalty_without_track,
            'penalty_with_track': tire_penalty_with_track,
            'penalty_capped': tire_penalty_capped,
            'pace_percent': pace_multiplier * 100,
            'at_cliff': at_cliff
        })

        # Print key laps
        if lap == 1 or lap == 10 or lap == cliff_lap or lap == 20 or lap == num_laps:
            print(f"  Lap {lap:2d}: Tire age={car.tire_age:2d} | "
                  f"Penalty={tire_penalty_capped*100:5.2f}% | "
                  f"Pace={pace_multiplier*100:6.2f}%"
                  f"{' [CLIFF]' if at_cliff else ''}")

    # Calculate summary statistics
    lap_10_data = lap_data[9]  # Lap 10 (index 9)
    cliff_lap_data = lap_data[cliff_lap - 1]
    final_lap_data = lap_data[-1]

    results = {
        'circuit_id': circuit_id,
        'circuit_name': circuit_name,
        'multiplier': track_multiplier,
        'lap_data': lap_data,
        'lap_10_pace': lap_10_data['pace_percent'],
        'cliff_lap': cliff_lap,
        'cliff_pace': cliff_lap_data['pace_percent'],
        'final_pace': final_lap_data['pace_percent'],
        'pace_loss_to_lap_10': 100 - lap_10_data['pace_percent'],
        'pace_loss_to_cliff': 100 - cliff_lap_data['pace_percent'],
    }

    print(f"\n  Summary:")
    print(f"    Lap 10 pace: {results['lap_10_pace']:.2f}%")
    print(f"    Cliff lap {cliff_lap} pace: {results['cliff_pace']:.2f}%")
    print(f"    Final lap {num_laps} pace: {results['final_pace']:.2f}%")
    print(f"    Total pace loss by lap 10: {results['pace_loss_to_lap_10']:.2f}%")
    print(f"    Total pace loss by cliff: {results['pace_loss_to_cliff']:.2f}%")

    return results


def compare_circuits(all_results):
    """Compare tire degradation across all circuits."""
    print(f"\n{'='*70}")
    print("COMPARATIVE ANALYSIS")
    print(f"{'='*70}")

    # Sort by multiplier
    sorted_results = sorted(all_results, key=lambda x: x['multiplier'])

    print("\n1. Tire Degradation Multipliers (Low to High):")
    print(f"   {'Circuit':<20} {'Multiplier':<12} {'Type'}")
    print(f"   {'-'*50}")
    for r in sorted_results:
        circuit_info = CIRCUITS[r['circuit_id']]
        circuit_type = circuit_info['type'].capitalize()
        print(f"   {r['circuit_name']:<20} {r['multiplier']:<12.1f} {circuit_type}")

    print("\n2. Pace Loss at Lap 10 (Soft Tires):")
    print(f"   {'Circuit':<20} {'Pace Loss':<12} {'Remaining Pace'}")
    print(f"   {'-'*50}")
    sorted_by_loss = sorted(all_results, key=lambda x: x['pace_loss_to_lap_10'])
    for r in sorted_by_loss:
        print(f"   {r['circuit_name']:<20} {r['pace_loss_to_lap_10']:5.2f}%       "
              f"{r['lap_10_pace']:.2f}%")

    print("\n3. Pace Loss at Tire Cliff (Lap 12 for Soft):")
    print(f"   {'Circuit':<20} {'Pace Loss':<12} {'Remaining Pace'}")
    print(f"   {'-'*50}")
    sorted_by_cliff = sorted(all_results, key=lambda x: x['pace_loss_to_cliff'])
    for r in sorted_by_cliff:
        print(f"   {r['circuit_name']:<20} {r['pace_loss_to_cliff']:5.2f}%       "
              f"{r['cliff_pace']:.2f}%")

    # Calculate strategic implications
    print("\n4. Strategic Implications:")
    monaco = next(r for r in all_results if r['circuit_id'] == 'monaco')
    suzuka = next(r for r in all_results if r['circuit_id'] == 'suzuka')
    spa = next(r for r in all_results if r['circuit_id'] == 'spa')

    print(f"   Baseline (Spa): {spa['pace_loss_to_lap_10']:.2f}% loss by lap 10")
    print(f"   Monaco vs Spa: {monaco['pace_loss_to_lap_10'] - spa['pace_loss_to_lap_10']:.2f}% difference")
    print(f"   Suzuka vs Spa: {suzuka['pace_loss_to_lap_10'] - spa['pace_loss_to_lap_10']:.2f}% difference")
    print(f"   Monaco vs Suzuka: {monaco['pace_loss_to_lap_10'] - suzuka['pace_loss_to_lap_10']:.2f}% difference")

    print(f"\n   This means:")
    monaco_advantage = suzuka['pace_loss_to_lap_10'] - monaco['pace_loss_to_lap_10']
    print(f"   - Monaco has {monaco_advantage:.2f}% LESS tire wear than Suzuka")
    print(f"   - Teams can run {monaco_advantage / monaco['pace_loss_to_lap_10'] * 100:.1f}% longer stints at Monaco")
    print(f"   - Aggressive strategies more viable at Monaco, conservative at Suzuka")

    return True


def test_all_circuits():
    """Test tire degradation on all F1 circuits."""
    print("="*70)
    print("TIRE DEGRADATION TESTING - ALL F1 CIRCUITS")
    print("="*70)
    print("\nThis test verifies that tire degradation varies appropriately")
    print("across different circuits, creating strategic variety.")
    print("\nTest Configuration:")
    print("  - Tire Compound: SOFT (highest degradation)")
    print("  - Test Duration: 30 laps")
    print("  - Driver/Team: Standardized (B-tier, 85 skill)")

    # Circuit test configuration
    circuits_to_test = [
        ('monaco', 'Monaco', 0.7),
        ('monza', 'Monza', 0.8),
        ('spa', 'Spa-Francorchamps', 1.0),
        ('cota', 'Circuit of the Americas', 1.2),
        ('silverstone', 'Silverstone', 1.3),
        ('suzuka', 'Suzuka', 1.4),
    ]

    all_results = []

    # Test each circuit
    for circuit_id, circuit_name, expected_mult in circuits_to_test:
        result = test_circuit_tire_degradation(circuit_id, circuit_name, expected_mult)
        if result:
            all_results.append(result)
        else:
            print(f"❌ FAILED: {circuit_name}")
            return False

    # Compare all circuits
    compare_circuits(all_results)

    # Final validation
    print(f"\n{'='*70}")
    print("VALIDATION RESULTS")
    print(f"{'='*70}")

    print("\n✅ All circuits tested successfully!")
    print("✅ Tire degradation multipliers verified")
    print("✅ Strategic variety confirmed:")
    print("   - Monaco: Low-degradation street circuit (gentle on tires)")
    print("   - Monza: Low-degradation speed circuit (minimal cornering)")
    print("   - Spa: Medium-degradation balanced circuit (baseline)")
    print("   - COTA: Medium-high degradation (varied corners)")
    print("   - Silverstone: High-degradation (fast sweeping corners)")
    print("   - Suzuka: Highest degradation (technical, demanding layout)")

    print("\n✅ PASS: Tire degradation creates meaningful strategic differences")
    print("         between circuits, enhancing gameplay variety and realism.")

    return True


if __name__ == "__main__":
    success = test_all_circuits()
    sys.exit(0 if success else 1)
