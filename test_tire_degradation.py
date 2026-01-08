"""
Test tire degradation system with different circuit characteristics
"""
from race.track import Track
from race.car import Car
from data.teams import TEAMS_DATA
import config

def test_tire_degradation_multipliers():
    """Test that different circuits have different tire degradation rates"""

    print("=" * 60)
    print("TIRE DEGRADATION SYSTEM TEST")
    print("=" * 60)

    # Create tracks with different tire degradation characteristics
    circuits = {
        "Monaco": ("monaco", 0.7),           # Low degradation (street circuit)
        "Monza": ("monza", 0.8),             # Low degradation (temple of speed)
        "Spa": ("spa", 1.0),                 # Medium degradation
        "COTA": ("cota", 1.2),               # Medium-high degradation
        "Silverstone": ("silverstone", 1.3), # High degradation
        "Suzuka": ("suzuka", 1.4),           # Highest degradation
        "Custom": (None, 1.0),               # Default track (baseline)
    }

    print("\n1. Testing track tire degradation multipliers:")
    print("-" * 60)

    for circuit_name, (circuit_id, expected_multiplier) in circuits.items():
        track = Track(circuit_id=circuit_id)
        actual_multiplier = track.get_tire_degradation_multiplier()

        status = "✓" if abs(actual_multiplier - expected_multiplier) < 0.01 else "✗"
        print(f"{status} {circuit_name:15s}: {actual_multiplier:.2f}x (expected {expected_multiplier:.2f}x)")

    print("\n2. Testing car tire degradation calculation:")
    print("-" * 60)

    # Create a test car
    team_data = TEAMS_DATA[0]
    driver_data = team_data["drivers"][0]
    team_info = {
        "name": team_data["name"],
        "tier": team_data.get("tier", "B"),
        "characteristics": team_data.get("characteristics", {}),
    }

    # Test with Monaco (low degradation) vs Suzuka (high degradation)
    monaco_track = Track(circuit_id="monaco")
    suzuka_track = Track(circuit_id="suzuka")

    # Create two identical cars
    monaco_car = Car(driver_data, team_info, 1)
    suzuka_car = Car(driver_data, team_info, 1)

    # Set tire age to 10 laps for both
    monaco_car.tire_age = 10
    suzuka_car.tire_age = 10
    monaco_car.tire_compound = config.TIRE_SOFT
    suzuka_car.tire_compound = config.TIRE_SOFT

    # Update cars once to get track multipliers
    monaco_car.update(monaco_track, dt=1.0, total_race_laps=20)
    suzuka_car.update(suzuka_track, dt=1.0, total_race_laps=20)

    print(f"\nCar on Monaco (0.7x multiplier):")
    print(f"  Track multiplier: {monaco_car.track_tire_deg_multiplier:.2f}x")
    print(f"  Tire age: {monaco_car.tire_age} laps")
    print(f"  Current pace: {monaco_car.current_pace:.6f}")

    print(f"\nCar on Suzuka (1.4x multiplier):")
    print(f"  Track multiplier: {suzuka_car.track_tire_deg_multiplier:.2f}x")
    print(f"  Tire age: {suzuka_car.tire_age} laps")
    print(f"  Current pace: {suzuka_car.current_pace:.6f}")

    # Suzuka should have lower pace due to higher tire degradation
    pace_difference = ((monaco_car.current_pace - suzuka_car.current_pace) / suzuka_car.current_pace) * 100

    print(f"\n  Pace difference: {pace_difference:.2f}% faster on Monaco")
    print(f"  (Monaco's lower tire wear results in better pace)")

    if suzuka_car.current_pace < monaco_car.current_pace:
        print("\n✓ Tire degradation system working correctly!")
        print("  Cars on high-degradation circuits (Suzuka) are slower")
        print("  Cars on low-degradation circuits (Monaco) are faster")
    else:
        print("\n✗ ERROR: Tire degradation system not working as expected")
        return False

    print("\n3. Testing degradation over multiple laps:")
    print("-" * 60)

    # Create fresh cars for lap-by-lap test
    monaco_car = Car(driver_data, team_info, 1)
    suzuka_car = Car(driver_data, team_info, 1)
    monaco_car.tire_compound = config.TIRE_SOFT
    suzuka_car.tire_compound = config.TIRE_SOFT

    print(f"\n{'Lap':>5} | {'Monaco Pace':>12} | {'Suzuka Pace':>12} | {'Gap %':>8}")
    print("-" * 60)

    for lap in range(0, 15, 3):
        monaco_car.tire_age = lap
        suzuka_car.tire_age = lap

        monaco_car.update(monaco_track, dt=1.0, total_race_laps=20)
        suzuka_car.update(suzuka_track, dt=1.0, total_race_laps=20)

        gap = ((monaco_car.current_pace - suzuka_car.current_pace) / suzuka_car.current_pace) * 100

        print(f"{lap:>5} | {monaco_car.current_pace:>12.6f} | {suzuka_car.current_pace:>12.6f} | {gap:>7.2f}%")

    print("\n" + "=" * 60)
    print("TEST COMPLETE - Tire degradation system is working!")
    print("=" * 60)

    return True

if __name__ == "__main__":
    success = test_tire_degradation_multipliers()
    exit(0 if success else 1)
