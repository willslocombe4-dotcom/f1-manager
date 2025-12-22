# Code Review: Gap Logic Bug

## Summary
The "Gap Bug" is caused by the simulation running at an extremely high speed (approx 20x real-time), resulting in lap times of ~4 seconds. Consequently, large visual gaps (e.g., 20% of the track) correspond to very small time gaps (e.g., 0.9 seconds). The user's intuition ("looks like 5 seconds") is based on a more realistic time scale.

## Files Reviewed
- `race/car.py` - Verified movement logic and pace calculation.
- `race/race_engine.py` - Verified gap calculation logic.
- `config.py` - Identified the root cause in `BASE_SPEED`.
- `reproduce_gap_bug.py` - Confirmed the math.

## Verdict: NEEDS CHANGES 🔄

---

## Issues Found

### 🔴 Critical
1. **Simulation Speed Too Fast** - `config.py:25`
   - Problem: `BASE_SPEED = 0.25` results in a lap time of ~4.33 seconds. This compresses all time gaps. A visual gap of "3 corners" (approx 20% of track) is physically only 0.9 seconds, confusing the user.
   - Fix: Reduce `BASE_SPEED` to `0.045` to achieve a lap time of ~24 seconds. This will make a 20% track gap equal to ~4.8 seconds, matching user expectations.

2. **Pit Stop Time Scaling** - `config.py:105`
   - Problem: `PIT_STOP_BASE_TIME = 22.0` is calibrated for... actually it's huge. With 4s laps, a 22s pit stop is 5 laps! With 24s laps, it's almost 1 lap.
   - Fix: Reduce `PIT_STOP_BASE_TIME` to `6.0` seconds (approx 25% of a lap) to match F1 proportions.

### 🟢 Minor
1. **Potential Crash** - `race/race_engine.py:137`
   - Observation: `leader.lap` is accessed without checking if `leader` is None (though unlikely after init).

---

## The Math
**Current:**
- `BASE_SPEED` = 0.25 waypoints/frame
- Track = 65 waypoints
- Lap Time = 65 / (0.25 * 60) = **4.33 seconds**
- Gap (20% track) = 0.2 * 4.33 = **0.87 seconds**

**Proposed:**
- `BASE_SPEED` = 0.045 waypoints/frame
- Lap Time = 65 / (0.045 * 60) = **24.07 seconds**
- Gap (20% track) = 0.2 * 24.07 = **4.81 seconds**

---

## Handoff

### To @f1-bug-fixer:
Please apply the following changes to `config.py`:

1. Change `BASE_SPEED` to `0.045`.
2. Change `PIT_STOP_BASE_TIME` to `6.0`.
3. Change `PIT_STOP_VARIANCE` to `1.0`.

This will align the visual gaps with the displayed time gaps.
