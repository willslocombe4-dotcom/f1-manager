# Visual Circuit Testing - Instructions

This document explains how to perform visual testing for all 6 F1 circuits.

## Quick Start

### Step 1: Run Automated Geometry Analysis

```bash
python analyze_circuit_geometry.py
```

This will analyze waypoint geometry and predict visual quality **without running the game**. It checks for:
- Waypoint smoothness
- Spacing consistency
- Track shape characteristics
- Potential visual issues

### Step 2: Run Technical Validation

```bash
python test_circuit_visuals.py
```

This validates technical requirements:
- Waypoint counts
- Track bounds (fits in display)
- DRS zone configuration
- Tire degradation values
- Track characteristics

### Step 3: Manual Visual Testing

```bash
python main.py
```

Then for **each of the 6 circuits**:

1. Select circuit from track selection screen
2. Observe the preview (should look recognizable)
3. Start a race
4. Watch for 2-3 laps
5. Verify against checklist (see CIRCUIT_VISUAL_TESTING_GUIDE.md)

## Testing Checklist

Use this to track your progress:

```
[ ] Monaco - Circuit de Monaco
    [ ] Automated geometry analysis passed
    [ ] Technical validation passed
    [ ] Manual visual testing passed
    [ ] Racing line smooth
    [ ] Famous corners recognizable

[ ] Silverstone Circuit
    [ ] Automated geometry analysis passed
    [ ] Technical validation passed
    [ ] Manual visual testing passed
    [ ] Racing line smooth
    [ ] Famous corners recognizable

[ ] Spa-Francorchamps
    [ ] Automated geometry analysis passed
    [ ] Technical validation passed
    [ ] Manual visual testing passed
    [ ] Racing line smooth
    [ ] Famous corners recognizable

[ ] Monza (Autodromo Nazionale di Monza)
    [ ] Automated geometry analysis passed
    [ ] Technical validation passed
    [ ] Manual visual testing passed
    [ ] Racing line smooth
    [ ] Famous corners recognizable

[ ] Suzuka Circuit
    [ ] Automated geometry analysis passed
    [ ] Technical validation passed
    [ ] Manual visual testing passed
    [ ] Racing line smooth
    [ ] Famous corners recognizable

[ ] COTA (Circuit of the Americas)
    [ ] Automated geometry analysis passed
    [ ] Technical validation passed
    [ ] Manual visual testing passed
    [ ] Racing line smooth
    [ ] Famous corners recognizable
```

## What to Look For

### Good Circuit Indicators ✅

- Track shape immediately recognizable
- Famous corners are visually identifiable
- Racing line flows smoothly without jerky movements
- Cars navigate corners naturally
- Start/finish line connects seamlessly
- Track fits well in display area
- Appropriate number of straights for overtaking

### Bad Circuit Indicators ❌

- Track shape doesn't match real circuit
- Jagged or angular corners
- Cars jump between waypoints
- Unnatural car positioning
- Gap at start/finish line
- Track too small or too large
- No clear overtaking opportunities

## Circuit-Specific Notes

### Monaco 🇲🇨
**What makes it authentic:**
- Very compact and tight
- Lots of 90-degree corners (street circuit)
- Grand Hotel Hairpin clearly the tightest corner
- Minimal straights (hard to overtake)

### Silverstone 🇬🇧
**What makes it authentic:**
- Fast, flowing layout
- Long straights (2 DRS zones)
- Maggotts-Becketts complex visible
- High-speed character throughout

### Spa 🇧🇪
**What makes it authentic:**
- Longest track (feels expansive)
- Eau Rouge/Raidillon uphill section distinctive
- Very long Kemmel Straight
- Triangle-ish overall shape

### Monza 🇮🇹
**What makes it authentic:**
- Temple of Speed - longest straights
- Rectangular layout with chicanes
- Parabolica long sweeping corner
- Very few tight corners

### Suzuka 🇯🇵
**What makes it authentic:**
- Figure-8 layout (track crosses itself)
- S Curves flow naturally
- 130R fast sweeping left
- Mix of technical and high-speed

### COTA 🇺🇸
**What makes it authentic:**
- Turn 1 uphill section
- Esses like Silverstone's Maggotts-Becketts
- Stadium section is tight
- Modern, balanced design

## Common Issues and Fixes

### Issue: Track looks jagged
**Cause:** Too few waypoints or waypoints too far apart
**Fix:** Add more waypoints in that section (in data/circuits.py)

### Issue: Track doesn't look like the real circuit
**Cause:** Waypoints don't match real track layout
**Fix:** Adjust waypoint coordinates to match real circuit shape

### Issue: Cars jump or wobble
**Cause:** Waypoints too far apart or inconsistent spacing
**Fix:** Add waypoints or redistribute them more evenly

### Issue: Start/finish line has a gap
**Cause:** First and last waypoints are far apart
**Fix:** Adjust first/last waypoints to be closer together

### Issue: Track too small/large
**Cause:** Waypoint coordinates out of optimal range
**Fix:** Scale all waypoints proportionally

## Files Created for Testing

1. **test_circuit_visuals.py** - Automated technical validation
2. **analyze_circuit_geometry.py** - Geometry analysis (predicts visual quality)
3. **CIRCUIT_VISUAL_TESTING_GUIDE.md** - Detailed manual testing guide
4. **VISUAL_TESTING_README.md** (this file) - Quick start instructions

## After Testing

### If All Circuits Pass:

1. ✅ Mark subtask 5.1 as completed in implementation_plan.json
2. ✅ Update build-progress.txt with results
3. ✅ Commit changes
4. ✅ Move to next testing phase (5.2 - tire degradation)

### If Circuits Need Fixes:

1. Document issues found
2. Update waypoints in `data/circuits.py`
3. Re-run automated tests
4. Re-do manual visual testing
5. Repeat until all pass

## Success Criteria

All 6 circuits must:
- ✅ Pass automated geometry analysis
- ✅ Pass technical validation
- ✅ Look recognizable as their real-world counterparts
- ✅ Have smooth racing lines
- ✅ Show famous corners clearly
- ✅ Provide appropriate overtaking opportunities

---

**Good luck with testing!** 🏁
