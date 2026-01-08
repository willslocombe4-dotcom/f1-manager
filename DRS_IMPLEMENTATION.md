# DRS (Drag Reduction System) Implementation

## Overview
DRS zones have been implemented to match real F1 racing dynamics. DRS provides a speed boost to cars that are within 1 second of the car ahead, but only when in designated DRS zones on the track.

## Implementation Details

### Configuration (config.py)
- `DRS_DETECTION_TIME = 1.0` - Gap required to car ahead (in seconds)
- `DRS_SPEED_BOOST = 0.08` - Speed boost when DRS is active (+8%)

### Car State (race/car.py)
Two new attributes track DRS status:
- `is_drs_available` - True if car is within 1 second of car ahead
- `is_drs_active` - True if DRS is available AND car is in a DRS zone

### DRS Eligibility Rules
A car can activate DRS when ALL of these conditions are met:
1. **Not the race leader** (position > 1)
2. **After lap 1** (lap > 1) - DRS is enabled from lap 2 onwards
3. **Within 1 second of car ahead** (gap_to_ahead_time <= DRS_DETECTION_TIME)
4. **Currently in a DRS zone** on the track

### Speed Boost Application
When DRS is active, the car receives an 8% speed boost:
```python
if self.is_drs_active:
    pace *= (1.0 + config.DRS_SPEED_BOOST)  # +8% boost
```

This boost is applied in the `_calculate_current_pace()` method, after all other modifiers (tier, skill, fuel, tires, variance).

### DRS Zones per Circuit
Each F1 circuit has DRS zones defined as progress ranges (0.0 to 1.0):

- **Monaco**: 1 DRS zone (0.00 → 0.08)
- **Silverstone**: 2 DRS zones (Hangar Straight, Wellington Straight)
- **Spa-Francorchamps**: 2 DRS zones (Kemmel Straight, main straight)
- **Monza**: 2 DRS zones (long straights)
- **Suzuka**: 1 DRS zone
- **Circuit of the Americas**: 2 DRS zones (main straight, back straight)

DRS zones are defined in `data/circuits.py` for each circuit.

### Track Methods (race/track.py)
The Track class provides two methods for DRS:
- `get_drs_zones()` - Returns list of DRS zone definitions
- `is_in_drs_zone(progress)` - Checks if a position is in any DRS zone
  - Handles zones that cross the start/finish line correctly

### Update Flow
Each frame:
1. `RaceEngine.update()` updates all cars
2. For each car, `Car.update(track)` is called:
   - Checks if DRS is available (based on previous frame's gap)
   - Checks if car is in a DRS zone
   - Sets `is_drs_available` and `is_drs_active`
3. `Car._calculate_current_pace()` applies DRS boost if active
4. Car moves forward with boosted pace
5. After all cars updated, gaps are recalculated for next frame

### Testing
A comprehensive test suite is provided in `test_drs_zones.py`:
- Test 1: DRS zone detection for all circuits
- Test 2: DRS availability based on gap to car ahead
- Test 3: DRS activation (available + in zone)
- Test 4: DRS speed boost verification
- Test 5: All circuits have DRS zones

## Strategic Impact
- Creates overtaking opportunities on straights
- Adds authentic F1 racing dynamics
- Cars can close gaps more effectively in DRS zones
- Leader has no DRS, following cars have advantage
- Balances racing between different circuit types

## Notes
- DRS detection uses gap from previous frame (60 FPS = negligible lag)
- DRS zones match real F1 configurations for each circuit
- The 8% boost is balanced to be noticeable but not overpowered
- Monaco (street circuit) has only 1 DRS zone, while fast circuits like Monza have 2
