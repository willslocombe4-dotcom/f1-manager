# F1 Circuit Visual Testing Guide

This guide provides detailed instructions for manually testing each F1 circuit for visual accuracy and racing line quality.

## Testing Procedure

### 1. Run the Game
```bash
python main.py
```

### 2. For Each Circuit

1. **Select the circuit** from the track selection screen
2. **Observe the track preview** (should show recognizable shape)
3. **Start a race** (default settings are fine)
4. **Watch for 2-3 laps** to see:
   - Track shape accuracy
   - Racing line smoothness
   - Car spacing and positioning
   - Visual flow of the circuit

### 3. Visual Accuracy Checklist

For each circuit, verify:

- [ ] Track shape is **recognizable** as the real circuit
- [ ] Famous corners are **visually identifiable**
- [ ] Racing line **flows naturally** without sharp angles
- [ ] Cars **navigate smoothly** through all corners
- [ ] No **visual glitches** (cars jumping, clipping, etc.)
- [ ] Track **fits well** in the display area
- [ ] **Start/finish line** connects properly (no gap)

---

## Circuit-Specific Testing Details

### 🇲🇨 Monaco (Circuit de Monaco)

**Key Visual Features to Verify:**
- Compact, tight street circuit layout
- Famous **Casino Square** sweeping section
- Iconic **Grand Hotel Hairpin** (slowest corner in F1)
- **Tunnel** section (should be visible as a distinctive section)
- Tight **Swimming Pool** complex at the end

**Expected Characteristics:**
- Very tight and technical
- Minimal straight sections
- Lots of 90-degree corners (street circuit)
- Cars should be close together (short track)

**What to Look For:**
```
✓ Track stays in Monte Carlo harbor area (tight layout)
✓ Hairpin is clearly the tightest corner
✓ Track has characteristic Monaco "shape" (recognizable from broadcasts)
✓ No long straights (matches street circuit character)
```

---

### 🇬🇧 Silverstone Circuit

**Key Visual Features to Verify:**
- Fast, flowing layout
- High-speed **Copse** corner at start
- Distinctive **Maggotts-Becketts-Chapel** complex (series of fast corners)
- **Hangar Straight** (long straight for overtaking)
- Fast **Club** corner section at end

**Expected Characteristics:**
- Wide, sweeping corners
- Multiple long straights
- High-speed character throughout
- Open, flowing layout

**What to Look For:**
```
✓ Track has characteristic "boot" or complex shape
✓ Long straights are clearly visible (2 DRS zones)
✓ Fast, flowing corner sections (not tight hairpins)
✓ Cars maintain high speed through most corners
```

---

### 🇧🇪 Spa-Francorchamps

**Key Visual Features to Verify:**
- **La Source** hairpin at start
- Legendary **Eau Rouge/Raidillon** uphill section (distinctive shape)
- Very long **Kemmel Straight**
- Fast **Pouhon** double-apex corner
- High-speed **Blanchimont** corner
- **Bus Stop** chicane at end

**Expected Characteristics:**
- Longest track (should feel expansive)
- Mix of tight hairpin and very fast corners
- Very long straights
- Natural, flowing layout

**What to Look For:**
```
✓ Track has distinctive "triangle" shape
✓ Eau Rouge section clearly visible (uphill left-right)
✓ Kemmel Straight is one of the longest sections
✓ Mix of tight and fast corners
✓ Overall layout feels "big" and expansive
```

---

### 🇮🇹 Monza (Autodromo Nazionale di Monza)

**Key Visual Features to Verify:**
- "Temple of Speed" - very long straights
- **First chicane** (Variante del Rettifilo)
- **Curva Grande** sweeping corner
- **Lesmo** corners (two medium-speed rights)
- **Ascari** chicane
- Famous **Parabolica** long right-hander onto main straight

**Expected Characteristics:**
- Longest straights of any circuit
- Minimal braking zones
- Fast, flowing nature
- Rectangular-ish layout with chicanes

**What to Look For:**
```
✓ Extremely long straights dominate the layout
✓ Main straight is clearly the longest section
✓ Parabolica is a distinctive long sweeping corner
✓ Very few tight corners (mostly chicanes and fast corners)
✓ Cars reach high speeds on straights
```

---

### 🇯🇵 Suzuka Circuit

**Key Visual Features to Verify:**
- Unique **figure-8** layout (track crosses over itself)
- Fast **S Curves** section
- **Degner Curve** complex
- Tight **Hairpin**
- **Spoon Curve** (double-apex left)
- Legendary **130R** (very fast left-hander)
- **Casio Triangle** chicane

**Expected Characteristics:**
- Figure-8 shape is distinctive
- Mix of technical and high-speed sections
- Crossover point should be visible
- Balanced layout (not street circuit, not pure speed)

**What to Look For:**
```
✓ Clear figure-8 shape (track crosses itself)
✓ S Curves section flows naturally
✓ 130R is a fast, sweeping left corner
✓ Hairpin is clearly the tightest corner
✓ Mix of corner types (technical + high-speed)
```

---

### 🇺🇸 COTA (Circuit of the Americas)

**Key Visual Features to Verify:**
- Dramatic uphill **Turn 1** (steep climb)
- **Esses** section (inspired by Maggotts-Becketts)
- **Turn 10** hairpin
- Long **back straight**
- Tight **Stadium Section** with hairpin complex

**Expected Characteristics:**
- Modern circuit design (wide, safe)
- Combination of elements from other famous tracks
- Good mix of technical and high-speed sections
- Multiple overtaking opportunities

**What to Look For:**
```
✓ Turn 1 is distinctive (would be uphill in reality)
✓ Esses section flows like Silverstone
✓ Stadium section is visibly tighter
✓ Good balance of straights and technical sections
✓ Modern, purpose-built circuit character
```

---

## Racing Line Quality Assessment

For **all circuits**, the racing line should:

1. **Flow smoothly** - No sudden direction changes
2. **Be predictable** - Cars follow natural paths through corners
3. **Look realistic** - Mimics real F1 racing lines (outside-inside-outside)
4. **Handle side-by-side racing** - Cars can race alongside each other
5. **No glitches** - No cars jumping or clipping

### Good Racing Line Indicators:
- Cars take wide entry into corners
- Hit apex naturally
- Exit wide for acceleration
- Smooth transitions between corners
- Consistent lap times

### Poor Racing Line Indicators:
- Cars make sharp, jerky movements
- Inconsistent corner entry/exit
- Cars appear to "jump" between waypoints
- Unnatural positioning

---

## DRS Zone Verification

For each circuit's DRS zones:

1. **Locate the zones** (should be on straights)
2. **Watch cars in race** (position 2+ within 1 second)
3. **Observe speed boost** when DRS activates
4. **Verify placement** makes sense for overtaking

### DRS Zone Locations:

| Circuit | DRS Zones | Expected Location |
|---------|-----------|-------------------|
| Monaco | 1 zone | Main straight only |
| Silverstone | 2 zones | Hangar Straight + Wellington Straight |
| Spa | 2 zones | Kemmel Straight + main straight |
| Monza | 2 zones | Main straight + back straight |
| Suzuka | 1 zone | Main straight |
| COTA | 2 zones | Main straight + back straight |

---

## Common Issues to Watch For

### Visual Issues:
- **Jagged corners** → Too few waypoints in that section
- **Track doesn't close** → Gap between first/last waypoint
- **Cars jump** → Waypoints too far apart
- **Unrecognizable shape** → Waypoints don't match real circuit

### Racing Line Issues:
- **Cars wobble** → Waypoints not smooth enough
- **Unnatural cornering** → Wrong waypoint placement
- **Inconsistent spacing** → Waypoint density varies too much

### Gameplay Issues:
- **Too easy to overtake** → DRS zones too strong or numerous
- **Impossible to overtake** → No DRS zones or too short
- **Unrealistic tire wear** → Degradation multiplier wrong

---

## Testing Results Template

Use this template to record your observations:

```
Circuit: _________________
Date: ___________________

Visual Accuracy:        [ ] Pass  [ ] Fail
Racing Line Quality:    [ ] Pass  [ ] Fail
DRS Zones:             [ ] Pass  [ ] Fail
Famous Corners Visible: [ ] Pass  [ ] Fail

Notes:
- _________________________________
- _________________________________
- _________________________________

Issues Found:
- _________________________________
- _________________________________

Overall Result: [ ] APPROVED  [ ] NEEDS FIXES
```

---

## Approval Criteria

A circuit is approved when:

1. ✅ **Technically validated** (test_circuit_visuals.py passes)
2. ✅ **Visually recognizable** (looks like the real circuit)
3. ✅ **Racing line smooth** (no glitches or jagged movement)
4. ✅ **DRS zones functional** (activate on straights, provide overtaking)
5. ✅ **Famous corners identifiable** (key sections are visible)
6. ✅ **Gameplay feels appropriate** (matches circuit character)

---

## Next Steps After Testing

If all circuits pass:
1. Update `implementation_plan.json` - mark subtask 5.1 as completed
2. Document any minor adjustments needed
3. Proceed to next testing phase (tire degradation, DRS balance)

If circuits need fixes:
1. Document specific issues found
2. Adjust waypoints in `data/circuits.py`
3. Re-test affected circuits
4. Repeat until all circuits pass
