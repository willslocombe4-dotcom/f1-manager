# Track Characteristics Integration

## Overview

This document describes how track characteristics (tire degradation, DRS zones, etc.) are integrated with the race engine.

## Integration Flow

### 1. Race Engine Initialization

The `RaceEngine` now accepts a `circuit_id` parameter:

```python
# Create race with Monaco circuit
race_engine = RaceEngine(circuit_id="monaco")

# Create race with custom waypoints (backward compatible)
race_engine = RaceEngine(waypoints=custom_waypoints)

# Create race with default track
race_engine = RaceEngine()
```

### 2. Track Creation

When `RaceEngine` creates a `Track`, it passes the `circuit_id`:

```python
self.track = Track(waypoints=waypoints, decorations=decorations, circuit_id=circuit_id)
```

The `Track` class loads circuit data from `data/circuits.py` when `circuit_id` is provided.

### 3. Car Updates

During each frame, cars fetch track characteristics:

```python
# In Car.update():
# 1. Get tire degradation multiplier from track
self.track_tire_deg_multiplier = track.get_tire_degradation_multiplier()

# 2. Check DRS availability and activation
self.is_drs_available = (
    self.position > 1 and
    self.lap > 1 and
    self.gap_to_ahead_time <= config.DRS_DETECTION_TIME
)
self.is_drs_active = (
    self.is_drs_available and
    track.is_in_drs_zone(self.progress)
)
```

### 4. Pace Calculation

Track characteristics affect car pace:

```python
# Tire degradation with track multiplier
tire_penalty = self.tire_age * deg_rate * self.track_tire_deg_multiplier

# DRS speed boost
if self.is_drs_active:
    pace *= (1.0 + config.DRS_SPEED_BOOST)  # +8% speed
```

## Track Characteristics by Circuit

| Circuit | Tire Degradation | DRS Zones | Type |
|---------|------------------|-----------|------|
| Monaco | 0.7x (low) | 1 | Street |
| Monza | 0.8x (low) | 2 | Permanent |
| Spa | 1.0x (medium) | 2 | Permanent |
| COTA | 1.2x (medium-high) | 2 | Permanent |
| Silverstone | 1.3x (high) | 2 | Permanent |
| Suzuka | 1.4x (high) | 1 | Permanent |

## Strategic Impact

### Tire Degradation

- **Monaco (0.7x)**: 30% less tire wear → longer stints, fewer pit stops
- **Suzuka (1.4x)**: 40% more tire wear → more aggressive pit strategies
- Different circuits require different tire compound choices

### DRS Zones

- **Detection**: Car must be within 1 second of car ahead
- **Activation**: Only when in designated DRS zones
- **Effect**: +8% speed boost for overtaking
- **Street circuits** (Monaco): Minimal DRS zones
- **Fast circuits** (Silverstone, Monza): Multiple long DRS zones

## Backward Compatibility

Custom tracks (created via track editor) continue to work:

```python
# Custom track with waypoints
race_engine = RaceEngine(waypoints=my_waypoints, decorations=my_decorations)

# Track characteristics:
# - tire_degradation: 1.0 (baseline)
# - DRS zones: none
# - All features work normally
```

## Usage Examples

### Example 1: Quick Race on Monaco

```python
from race.race_engine import RaceEngine

# Start race on Monaco
race = RaceEngine(circuit_id="monaco")
race.start_race()

# Race characteristics:
# - Low tire wear (0.7x)
# - 1 DRS zone
# - Tight street circuit
```

### Example 2: Testing Tire Degradation

```python
# High degradation circuit
race_suzuka = RaceEngine(circuit_id="suzuka")
race_suzuka.start_race()

for _ in range(100):
    race_suzuka.update()

# Cars will need more pit stops due to 1.4x tire wear

# Low degradation circuit
race_monaco = RaceEngine(circuit_id="monaco")
race_monaco.start_race()

for _ in range(100):
    race_monaco.update()

# Cars can run longer stints with 0.7x tire wear
```

### Example 3: DRS Detection

```python
race = RaceEngine(circuit_id="silverstone")
race.start_race()

# After a few laps
race.update()

# Check DRS status for P2 driver
car = race.cars[1]
if car.is_drs_active:
    print(f"{car.driver_short} has DRS!")
    print(f"Speed boost: +{config.DRS_SPEED_BOOST * 100}%")
```

## Testing

Run the integration test to verify all components:

```bash
python test_track_integration.py
```

Tests cover:
1. Circuit loading and metadata
2. Tire degradation multipliers
3. DRS zone detection
4. Car integration
5. Backward compatibility
6. All 6 F1 circuits

## Files Modified

### Core Integration (Subtask 3.3)

- `race/race_engine.py`: Added `circuit_id` parameter to `__init__`
- `main.py`: Updated `_start_race` to support `circuit_id`
- `test_track_integration.py`: Comprehensive integration tests

### Previously Completed (Subtasks 3.1, 3.2)

- `race/car.py`: Tire degradation and DRS logic
- `race/track.py`: Circuit metadata access methods
- `data/circuits.py`: Circuit definitions
- `config.py`: DRS constants

## Next Steps

Phase 4 (Track Selection UI) will:
1. Add real F1 circuits to track selection screen
2. Display circuit previews and characteristics
3. Allow selection of circuits for races
4. Update main menu to pass `circuit_id` when starting races
