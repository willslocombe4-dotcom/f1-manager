# Config.py Track-Related Constants Update

## Subtask 5.5: Update config.py with track-related constants

### Summary
Updated config.py to eliminate magic numbers by adding proper constants for DRS and tire degradation track characteristics.

---

## Changes Made

### 1. Added New Constants to config.py

**Location:** Lines 185-188

#### DRS_ENABLED_FROM_LAP
```python
DRS_ENABLED_FROM_LAP = 2  # DRS becomes available from this lap onwards
```
- **Purpose:** Defines from which lap DRS becomes available
- **Value:** 2 (DRS enabled from lap 2 onwards, as per F1 regulations)
- **Replaces:** Hardcoded `self.lap > 1` check in car.py

#### DEFAULT_TIRE_DEG_MULTIPLIER
```python
DEFAULT_TIRE_DEG_MULTIPLIER = 1.0  # Default tire degradation multiplier for custom tracks
```
- **Purpose:** Default tire degradation multiplier for custom/non-F1 tracks
- **Value:** 1.0 (baseline, no modification)
- **Replaces:** Hardcoded `1.0` values in car.py and track.py

---

## Files Modified

### config.py
**Lines 182-188:** Added track-related constants section
- DRS_ENABLED_FROM_LAP = 2
- DEFAULT_TIRE_DEG_MULTIPLIER = 1.0

### race/car.py
**Line 61:** Updated initialization
```python
# Before:
self.track_tire_deg_multiplier = 1.0  # Default multiplier for custom tracks

# After:
self.track_tire_deg_multiplier = config.DEFAULT_TIRE_DEG_MULTIPLIER  # Default multiplier for custom tracks
```

**Line 259:** Updated DRS lap check
```python
# Before:
self.lap > 1 and  # Not on first lap (DRS enabled from lap 2)

# After:
self.lap >= config.DRS_ENABLED_FROM_LAP and  # DRS enabled from configured lap onwards
```

### race/track.py
**Lines 409-413:** Updated tire degradation defaults
```python
# Before:
def get_tire_degradation_multiplier(self):
    """..."""
    if self.circuit_data and "characteristics" in self.circuit_data:
        return self.circuit_data["characteristics"].get("tire_degradation", 1.0)
    return 1.0

# After:
def get_tire_degradation_multiplier(self):
    """..."""
    if self.circuit_data and "characteristics" in self.circuit_data:
        return self.circuit_data["characteristics"].get("tire_degradation", config.DEFAULT_TIRE_DEG_MULTIPLIER)
    return config.DEFAULT_TIRE_DEG_MULTIPLIER
```

---

## Benefits

### Code Quality
✅ **Eliminated Magic Numbers:** All track-related values now use named constants
✅ **Single Source of Truth:** Changes to DRS/tire behavior only need config.py updates
✅ **Self-Documenting:** Constant names clearly describe their purpose
✅ **Maintainability:** Easier to tune game balance by modifying config.py

### Flexibility
✅ **Configurable DRS Lap:** Can easily change when DRS becomes available
✅ **Configurable Default Degradation:** Can adjust baseline tire wear for custom tracks
✅ **No Code Changes Required:** Balance tweaks only require config.py edits

---

## Complete Track-Related Constants in config.py

All track-related constants now properly organized:

```python
# DRS (Drag Reduction System)
DRS_DETECTION_TIME = 1.0           # Gap required to car ahead (in seconds)
DRS_SPEED_BOOST = 0.08             # +8% speed boost when DRS is active
DRS_ENABLED_FROM_LAP = 2           # DRS becomes available from this lap onwards

# Track Characteristics
DEFAULT_TIRE_DEG_MULTIPLIER = 1.0  # Default tire degradation multiplier for custom tracks
```

---

## Circuit-Specific Values

**Note:** Circuit-specific tire degradation values remain in `data/circuits.py` as they are circuit data, not global constants:

- Monaco: 0.7x (low wear - street circuit)
- Monza: 0.8x (low wear - speed circuit)
- Spa: 1.0x (baseline)
- COTA: 1.2x (medium-high wear)
- Silverstone: 1.3x (high wear - fast corners)
- Suzuka: 1.4x (highest wear - technical layout)

---

## Verification

### Manual Code Review ✓
- [x] All magic numbers identified and replaced
- [x] Constants properly defined in config.py
- [x] All usage sites updated (car.py, track.py)
- [x] Documentation/comments updated
- [x] Constant naming follows existing conventions

### Test Coverage ✓
- [x] Verification test script created (test_config_constants.py)
- [x] Tests all constants are defined
- [x] Tests constants are used (no magic numbers)
- [x] Tests F1 circuits use circuit-specific values
- [x] Tests custom tracks use default values

---

## Backward Compatibility

✅ **Fully Backward Compatible**
- Default values match previous hardcoded values (1.0, lap 2)
- F1 circuits continue using circuit-specific values from circuits.py
- Custom tracks continue using baseline tire degradation
- DRS behavior unchanged (still enabled from lap 2)

---

## Acceptance Criteria Met

✅ **All magic numbers eliminated** - DRS lap check and default tire degradation now use constants
✅ **Config.py organized** - Track constants properly grouped and documented
✅ **Code quality improved** - Single source of truth for track-related configuration
✅ **Maintainability enhanced** - Easy to adjust balance without modifying multiple files

---

## Status: ✅ COMPLETE

Subtask 5.5 successfully completed. Config.py now contains all track-related constants with no magic numbers remaining in the codebase.
