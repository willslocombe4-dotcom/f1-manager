
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from race.race_engine import RaceEngine
from race.car import Car
import config

def test_gap_calculation():
    print("Initializing Race Engine...")
    engine = RaceEngine()
    
    # Mock cars to specific positions
    # Leader: Lap 1, Progress 0.5
    leader = engine.cars[0]
    leader.lap = 1
    leader.progress = 0.5
    
    # Car 2: Lap 1, Progress 0.4 (0.1 laps behind)
    car2 = engine.cars[1]
    car2.lap = 1
    car2.progress = 0.4
    
    # Car 3: Lap 1, Progress 0.27 (0.23 laps behind)
    car3 = engine.cars[2]
    car3.lap = 1
    car3.progress = 0.27
    
    # Force update to calculate gaps
    # We need to bypass the normal update which moves cars
    # So we'll just call the sorting and gap calculation part manually
    # or just call update() with dt=0? 
    # update() calls car.update() which moves car.
    # Let's just manually run the gap logic from RaceEngine.update
    
    print("\n--- Manual Gap Calculation Check ---")
    
    # Sort
    engine.cars.sort(key=lambda c: c.get_total_progress(), reverse=True)
    
    leader = engine.cars[0]
    leader_progress = leader.get_total_progress()
    print(f"Leader Progress: {leader_progress}")
    
    # Calculate expected time gap
    # Track length = 65 waypoints
    # Base speed = 0.25 pixels/frame
    # FPS = 60
    # Speed = 0.25 * 60 = 15 pixels/sec
    # Track length in pixels? No, track length is waypoints.
    # Speed in progress/sec = (0.25 / 65) * 60 = 0.230769...
    # Seconds per lap = 1 / 0.230769 = 4.333...
    
    seconds_per_lap = 65 / (0.25 * 60)
    print(f"Estimated Seconds Per Lap: {seconds_per_lap:.4f}")
    
    for i, car in enumerate(engine.cars[:3]):
        car.position = i + 1
        car.gap_to_leader = leader_progress - car.get_total_progress()
        
        if i > 0:
            ahead = engine.cars[i - 1]
            car.gap_to_ahead = ahead.get_total_progress() - car.get_total_progress()
        else:
            car.gap_to_ahead = 0.0
            
        print(f"\nCar {i+1} ({car.driver_short}):")
        print(f"  Progress: {car.progress:.4f}")
        print(f"  Gap to Leader (Progress): {car.gap_to_leader:.4f}")
        print(f"  Gap to Ahead (Progress): {car.gap_to_ahead:.4f}")
        
        # What the user sees (current bug)
        print(f"  DISPLAYED Gap: +{car.gap_to_ahead:.3f}")
        
        # What it should be (Time)
        expected_time_gap = car.gap_to_ahead * seconds_per_lap
        print(f"  EXPECTED Time Gap: +{expected_time_gap:.3f}s")

if __name__ == "__main__":
    test_gap_calculation()
