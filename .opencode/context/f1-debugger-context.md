# F1 Debugger Context

**Last Updated:** Not yet used

---

## Debug Statistics

| Metric | Value |
|--------|-------|
| Bugs Analyzed | 0 |
| Root Causes Found | 0 |
| High Confidence | 0 |
| Required Escalation | 0 |

---

## Bug History

| Date | Bug | Root Cause | File:Line | Fix Verified |
|------|-----|------------|-----------|--------------|
| - | - | - | - | No bugs analyzed yet |

---

## Known Bug-Prone Areas

### race/car.py
| Area | Risk | Why |
|------|------|-----|
| progress wrap | Medium | Edge case at exactly 1.0 |
| tire degradation | Low | Simple linear calculation |
| speed calculation | Medium | Multiple modifiers compound |

### race/race_engine.py
| Area | Risk | Why |
|------|------|-----|
| position sorting | Medium | Relies on get_total_progress() |
| gap calculations | Medium | Loop through all cars |
| lateral_offset | High | Complex proximity logic |

### race/track.py
| Area | Risk | Why |
|------|------|-----|
| waypoint indexing | Medium | Modulo arithmetic |
| angle calculation | Low | Standard math |
| offset positioning | Medium | Trigonometry edge cases |

### ui/renderer.py
| Area | Risk | Why |
|------|------|-----|
| car drawing | Low | Simple circles |
| track boundaries | Medium | Complex polygon math |
| surface caching | Low | Already implemented |

### ui/timing_screen.py
| Area | Risk | Why |
|------|------|-----|
| gap display | Medium | Format string logic |
| row positioning | Low | Simple arithmetic |

---

## Common Bug Patterns

### Pattern 1: Off-by-One in Laps
**Symptom:** Lap count seems wrong
**Cause:** Lap starts at 1, not 0
**Fix:** Check if code assumes 0-indexed laps

### Pattern 2: Progress Overflow
**Symptom:** Car teleports or disappears
**Cause:** progress >= 1.0 not handled
**Fix:** Ensure wrap-around logic is correct

### Pattern 3: Sort Instability
**Symptom:** Positions flicker
**Cause:** Ties in get_total_progress()
**Fix:** Add secondary sort key

### Pattern 4: Stale Reference
**Symptom:** Wrong car data displayed
**Cause:** Holding reference to car that was re-sorted
**Fix:** Re-fetch after sort

---

## Debug Checklist

### For Any Bug
- [ ] Can reproduce consistently?
- [ ] Read all potentially involved files
- [ ] Traced data flow from origin to symptom
- [ ] Identified exact line where data becomes wrong
- [ ] Verified fix doesn't break other cases
- [ ] Documented edge cases for testing

### For Visual Bugs
- [ ] Check render() is getting correct data
- [ ] Check coordinate calculations
- [ ] Check draw order

### For Logic Bugs
- [ ] Check all conditional branches
- [ ] Check loop bounds
- [ ] Check initialization

### For State Bugs
- [ ] Check __init__ values
- [ ] Check all places state is modified
- [ ] Check for race conditions (unlikely in pygame)

---

## Variable Reference

### Car State
```python
car.driver_number      # int: 1, 44, etc.
car.driver_name        # str: "Max Verstappen"
car.driver_short       # str: "VER"
car.team              # str: "Red Bull Racing"
car.position          # int: 1-20 (current race position)
car.starting_position # int: 1-20 (grid position)
car.progress          # float: 0.0-0.999... (position on track)
car.lap               # int: starts at 1
car.speed             # float: ~0.2-0.3
car.tire_compound     # str: "SOFT"/"MEDIUM"/"HARD"
car.tire_age          # int: laps on current tires
car.gap_to_leader     # float: total progress difference
car.gap_to_ahead      # float: progress diff to car ahead
car.lateral_offset    # int: -15, 0, or 15
```

### Race State
```python
race_engine.cars           # list[Car]: all 20 cars
race_engine.track          # Track: the circuit
race_engine.race_started   # bool
race_engine.race_time      # float: seconds elapsed
race_engine.total_laps     # int: 20
```

---

## Session Notes

### Current Session
Not yet started.

### Active Investigation
None.

### Observations
(To be populated during debugging)
