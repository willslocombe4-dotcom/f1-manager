# Bug Analysis: Gap Logic Completely Wrong

**Analyzed by:** @f1-debugger
**Date:** 2025-12-22
**Severity:** Major

---

## Symptoms

### What User Sees
1. **Gap displays in tenths instead of seconds** - A 1-second gap shows as "0.23" or similar.
2. **Incorrect LAPPED display** - User reports seeing "LAPPED" behavior when only slightly behind (likely misinterpreting the small decimal values or the "+1L" logic is confusing due to unit mismatch).

### When It Happens
- During race, especially visible when gaps are small.

### Expected vs Actual
| Expected | Actual |
|----------|--------|
| Gap shows in seconds (e.g., "+1.000") | Gap shows in lap progress units (e.g., "+0.230") |
| 1.0 means 1 second | 1.0 means 1 Lap (~4.3 seconds) |

---

## Root Cause

### Location
**File:** `race/race_engine.py`
**Line(s):** 75-81
**Function:** `update()`

### The Problem
```python
# Current code calculates gaps in PROGRESS units (0.0 to 1.0 per lap)
car.gap_to_leader = leader_progress - car.get_total_progress()
car.gap_to_ahead = ahead.get_total_progress() - car.get_total_progress()
```

**File:** `ui/timing_screen.py`
**Line(s):** 105, 114
```python
# Displaying progress units directly as if they were seconds
gap_str = f"+{car.gap_to_ahead:.3f}"
```

### Why It's Wrong
The game calculates position based on "progress" where 1.0 = 1 Lap.
Based on `config.BASE_SPEED` (0.25) and `track.track_length` (65 waypoints) at 60 FPS:
- **1 Lap Time** ≈ 4.33 seconds
- **1 Second** ≈ 0.23 progress units

So when a car is 1 second behind, the system calculates a gap of 0.23. The UI displays this as "+0.230", which the user interprets as 2 tenths of a second, when it's actually 1 full second.

The "LAPPED" confusion likely stems from this unit mismatch. If the user sees "+0.900", they might think "0.9 seconds", but it actually means "0.9 laps" (almost lapped).

---

## Code Path Trace

1. `race/car.py:update` - Car moves `0.25 / 65` progress per frame.
2. `race/race_engine.py:update` - Calculates `gap_to_ahead` as difference in progress (e.g., 0.23).
3. `ui/timing_screen.py:render` - ⚠️ **BUG HERE** - Takes 0.23 and displays `+0.230`.
4. User sees `+0.230` and expects `+1.000`.

---

## Fix Required

### Primary Fix 1: Add Time Gap Attributes
**File:** `race/car.py`
**Function:** `__init__`

Initialize new attributes to store time-based gaps.

```python
        self.gap_to_leader = 0.0
        self.gap_to_ahead = 0.0
        # Add these:
        self.gap_to_leader_time = 0.0
        self.gap_to_ahead_time = 0.0
```

### Primary Fix 2: Calculate Time Gaps
**File:** `race/race_engine.py`
**Function:** `update`

Convert progress gaps to time gaps using the track length and base speed.

```python
        # Calculate conversion factor (Seconds per 1.0 Progress)
        # Speed (prog/sec) = (BASE_SPEED / track_length) * FPS
        # Seconds per Lap = 1.0 / Speed
        speed_prog_per_sec = (config.BASE_SPEED / self.track.track_length) * config.FPS
        seconds_per_lap = 1.0 / speed_prog_per_sec if speed_prog_per_sec > 0 else 0

        for i, car in enumerate(self.cars):
            # ... existing position logic ...

            # Calculate gaps (Progress)
            car.gap_to_leader = leader_progress - car.get_total_progress()
            
            if i > 0:
                ahead = self.cars[i - 1]
                car.gap_to_ahead = ahead.get_total_progress() - car.get_total_progress()
            else:
                car.gap_to_ahead = 0.0

            # Calculate gaps (Time)
            car.gap_to_leader_time = car.gap_to_leader * seconds_per_lap
            car.gap_to_ahead_time = car.gap_to_ahead * seconds_per_lap
```

### Primary Fix 3: Display Time Gaps
**File:** `ui/timing_screen.py`
**Function:** `_draw_timing_rows`

Use the time-based gaps for display, but keep progress-based gap for "LAPPED" check.

```python
            # Gap to leader or ahead
            if car.position == 1:
                gap_text = self.font_medium.render("LEADER", True, config.TEXT_COLOR)
            # Check if close (using time now, e.g. < 0.5s)
            elif car.gap_to_ahead_time < 0.5:
                gap_str = f"+{car.gap_to_ahead_time:.3f}"
                gap_text = self.font_medium.render(gap_str, True, config.TEXT_GRAY)
            else:
                # Show gap to leader in laps if more than 1 lap (keep using progress gap)
                if car.gap_to_leader >= 1.0:
                    laps_down = int(car.gap_to_leader)
                    gap_str = f"+{laps_down}L"
                    gap_text = self.font_medium.render(gap_str, True, (255, 100, 100))
                else:
                    # Show time gap
                    gap_str = f"+{car.gap_to_ahead_time:.3f}"
                    gap_text = self.font_medium.render(gap_str, True, config.TEXT_GRAY)
```

---

## Testing Scenarios

1. **Start Race:** Verify gaps start at 0.0 and grow in reasonable seconds (not tenths).
2. **1 Second Gap:** When a car is visually ~1/4 lap behind (assuming 4s lap), gap should show ~1.0s.
3. **Lapped Car:** Ensure "+1L" still appears when a car is fully lapped (gap > 4.3s).
4. **Close Racing:** Verify cars very close show small time gaps (e.g., +0.100s).

---

## Confidence Level

**Certainty:** High
**Reasoning:** The math confirms the unit mismatch (Progress vs Seconds). 1.0 Progress ≈ 4.3 Seconds. The display was showing raw progress.

---

## Handoff

This analysis is ready for @f1-bug-fixer.
