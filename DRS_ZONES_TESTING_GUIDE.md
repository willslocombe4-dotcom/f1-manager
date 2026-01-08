# DRS Zones Testing & Balance Verification Guide

## Overview
This guide provides comprehensive testing procedures for the DRS (Drag Reduction System) implementation. DRS is a critical F1 feature that creates overtaking opportunities by giving following cars a speed boost in designated zones.

---

## Implementation Summary

### Core Constants (config.py)
```python
DRS_DETECTION_TIME = 1.0      # Gap required to car ahead (in seconds)
DRS_SPEED_BOOST = 0.08        # +8% speed boost when DRS is active
```

### Car State Variables
- `is_drs_available`: True if car is within 1 second of car ahead
- `is_drs_active`: True if DRS available AND car is in a DRS zone

### DRS Activation Requirements
All four conditions must be met:
1. **Position > 1** (not the race leader)
2. **Lap > 1** (DRS enabled from lap 2 onwards)
3. **Gap to ahead <= 1.0s** (within detection window)
4. **Currently in a DRS zone** on the track

---

## DRS Zones per Circuit

| Circuit | Zones | Zone Ranges | Strategic Notes |
|---------|-------|-------------|-----------------|
| **Monaco** | 1 | 0.00 → 0.08 | Street circuit, limited overtaking opportunities |
| **Silverstone** | 2 | 0.42 → 0.58, 0.00 → 0.12 | Hangar Straight & Wellington Straight |
| **Spa-Francorchamps** | 2 | 0.28 → 0.42, 0.00 → 0.10 | Kemmel Straight & main straight |
| **Monza** | 2 | 0.00 → 0.25, 0.52 → 0.65 | Temple of Speed, longest DRS zones |
| **Suzuka** | 1 | 0.00 → 0.12 | Technical circuit, single DRS zone |
| **COTA** | 2 | 0.00 → 0.15, 0.48 → 0.62 | Main straight & back straight |

---

## Testing Procedures

### 1. Code Verification

**File: config.py**
```bash
grep -A 2 "DRS" config.py
```
Expected output:
- `DRS_DETECTION_TIME = 1.0`
- `DRS_SPEED_BOOST = 0.08`

**File: race/car.py**
Check these key sections:
- Line ~64-65: DRS state variables initialized
- Line ~254-265: DRS detection logic in `update()` method
- Line ~174-175: DRS speed boost applied in `_calculate_current_pace()`

**File: race/track.py**
- Line ~415-425: `get_drs_zones()` method
- Line ~427-451: `is_in_drs_zone()` method with wrap-around handling

**File: data/circuits.py**
- All 6 circuits have `drs_zones` defined
- Zones use progress values (0.0 to 1.0)

---

### 2. Automated Test Suite

Run the comprehensive test suite:
```bash
python test_drs_zones.py
```

**Expected Test Results:**

**Test 1: All Circuits Have DRS Zones**
- ✓ All 6 circuits should have at least 1 DRS zone
- Monaco, Suzuka: 1 zone
- Silverstone, Spa, Monza, COTA: 2 zones

**Test 2: DRS Zone Detection**
- Each zone tested at start, middle, and end positions
- Detection should be accurate within zone boundaries
- Should correctly handle zones that cross start/finish line

**Test 3: DRS Availability (Gap Detection)**
- Gap 0.5s: DRS AVAILABLE ✓
- Gap 0.9s: DRS AVAILABLE ✓
- Gap 1.0s: DRS AVAILABLE ✓
- Gap 1.1s: DRS NOT AVAILABLE ✓
- Gap 2.0s: DRS NOT AVAILABLE ✓
- Lap 1, Gap 0.5s: DRS NOT AVAILABLE ✓

**Test 4: DRS Activation (Available + In Zone)**
- DRS should only be ACTIVE when both available AND in zone
- Outside zones: Available but NOT Active
- Inside zones: Available AND Active ✓

**Test 5: DRS Speed Boost**
- Expected boost: +8.0%
- Actual boost: +8.0% (should match within 0.1%)
- Result: ✓ PASS (boost matches expected)

---

### 3. Manual In-Game Testing

**Test Procedure:**

1. **Launch the game:**
   ```bash
   python main.py
   ```

2. **Select a circuit with multiple DRS zones:**
   - Recommended: Monza (2 zones, long straights, easy to observe)
   - Alternative: Silverstone or COTA

3. **Start the race and observe:**

**What to Look For:**

**Lap 1 Observation (DRS Disabled):**
- DRS should NOT activate on first lap
- All cars travel at same relative pace
- No speed differences in straight sections

**Lap 2+ Observation (DRS Enabled):**
- Cars within 1 second of car ahead should get speed boost in DRS zones
- Following cars should close gaps noticeably in DRS zones
- Leader has no DRS advantage

**Visual Indicators:**
- Watch car positions on the timing screen
- Following cars should reduce their gap in DRS zones
- Gaps should stabilize or increase outside DRS zones

**Balance Check:**
- Cars should NOT pass immediately with DRS
- DRS should create overtaking *opportunities*, not automatic passes
- Multiple laps with DRS should be needed to close significant gaps

---

## Expected Behavior & Balance

### DRS Speed Impact

**Base Scenario (no DRS):**
- Car traveling at BASE_SPEED = 0.014 (from config.py)
- With tier/skill/fuel/tire modifiers: ~0.012-0.015 pace

**With DRS Active:**
- Pace multiplied by 1.08 (+8%)
- Example: 0.014 × 1.08 = 0.01512
- Per frame speed increase: ~0.0012 (8% of base)

### Overtaking Dynamics

**Gap Closure Rate:**
- Following car with DRS: +8% pace
- In a typical DRS zone (8-25% of lap):
  - Monza Zone 1: 0.0 → 0.25 = 25% of lap
  - Monaco Zone: 0.0 → 0.08 = 8% of lap

**Expected Time to Close 1-Second Gap:**
- With 8% boost active ~20% of lap time
- Estimated: 5-10 laps to close a 1-second gap
- Requires sustained pressure, not instant pass

### Balance Verification

**Too Weak (needs adjustment if observed):**
- Cars with DRS cannot close gaps over 10+ laps
- No overtakes occur even with persistent DRS activation
- DRS seems to have no visible impact on race

**Balanced (expected behavior):**
- Following cars can close 0.5-1.0s gaps over 5-10 laps
- DRS creates overtaking opportunities, not guarantees
- Exciting close racing with position changes
- Leader still has defensive capability

**Too Strong (needs adjustment if observed):**
- Cars pass immediately with DRS activation
- Following car overtakes in single DRS zone
- Leader cannot defend position at all
- Race becomes parade of DRS passes

---

## Strategic Implications per Circuit

### Monaco (1 DRS zone, 8% of lap)
- **Overtaking Difficulty:** Very High (even with DRS)
- **Strategic Impact:** Minimal, qualifying crucial
- **Expected Behavior:** DRS helps but position changes rare

### Monza (2 DRS zones, 38% of lap)
- **Overtaking Difficulty:** Low
- **Strategic Impact:** Very High, exciting racing
- **Expected Behavior:** Multiple position changes per lap possible

### Silverstone (2 DRS zones, ~28% of lap)
- **Overtaking Difficulty:** Medium
- **Strategic Impact:** High, balanced racing
- **Expected Behavior:** Strategic overtaking opportunities

### Spa-Francorchamps (2 DRS zones, ~24% of lap)
- **Overtaking Difficulty:** Medium
- **Strategic Impact:** High, Kemmel Straight battles
- **Expected Behavior:** Classic slipstream + DRS overtakes

### Suzuka (1 DRS zone, 12% of lap)
- **Overtaking Difficulty:** High
- **Strategic Impact:** Medium, technical circuit
- **Expected Behavior:** DRS helps but difficult to overtake

### COTA (2 DRS zones, ~29% of lap)
- **Overtaking Difficulty:** Medium
- **Strategic Impact:** High, long back straight
- **Expected Behavior:** Good overtaking opportunities

---

## Common Issues & Troubleshooting

### Issue: DRS Never Activates

**Check:**
1. Are cars on lap 2 or later? (DRS disabled lap 1)
2. Is gap to ahead <= 1.0s?
3. Is car position > 1? (leader has no DRS)
4. Is car in a DRS zone?

**Debug:**
```python
# In Car.update() method
print(f"P{self.position} Lap{self.lap}: Gap={self.gap_to_ahead_time:.2f}s, "
      f"In Zone={track.is_in_drs_zone(self.progress)}, "
      f"Available={self.is_drs_available}, Active={self.is_drs_active}")
```

### Issue: DRS Too Powerful

**Solution:** Reduce DRS_SPEED_BOOST in config.py
- Try: 0.06 (6%) for more conservative boost
- Or: 0.05 (5%) for minimal impact

### Issue: DRS Too Weak

**Solution:** Increase DRS_SPEED_BOOST in config.py
- Try: 0.10 (10%) for stronger boost
- Or: 0.12 (12%) for maximum impact

### Issue: DRS Detection Inconsistent

**Check:**
1. Gap calculation in RaceEngine (should update every frame)
2. Track.is_in_drs_zone() handling of wrap-around zones
3. Frame timing and update order

---

## Success Criteria

Mark this subtask as COMPLETE when:

- ✅ All automated tests pass (test_drs_zones.py)
- ✅ All 6 circuits have DRS zones defined
- ✅ DRS activates correctly based on all 4 conditions
- ✅ Speed boost matches configured value (+8%)
- ✅ Manual testing shows balanced overtaking dynamics
- ✅ DRS creates opportunities without being overpowered
- ✅ Different circuits have appropriate DRS impact

---

## Files to Review

**Implementation:**
- `config.py` - DRS constants
- `race/car.py` - DRS state and speed boost
- `race/track.py` - DRS zone detection
- `data/circuits.py` - DRS zone definitions per circuit

**Testing:**
- `test_drs_zones.py` - Automated test suite
- `DRS_IMPLEMENTATION.md` - Implementation documentation
- This file - Testing and verification guide

---

## Notes

- DRS detection uses gap from previous frame (60 FPS = ~16ms lag, negligible)
- DRS zones match real F1 configurations for authenticity
- 8% boost balances realism and gameplay excitement
- Street circuits (Monaco) have fewer/shorter zones than speed circuits (Monza)
- Zone ranges use progress values (0.0 to 1.0 around track)
- Zones can wrap around start/finish line (handled correctly in code)
