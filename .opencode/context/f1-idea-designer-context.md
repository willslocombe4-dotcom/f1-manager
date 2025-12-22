# F1 Idea Designer Context

**Last Updated:** 2025-12-22

---

## Design Statistics

| Metric | Value |
|--------|-------|
| Ideas Explored | 1 |
| Designs Completed | 1 |
| Implemented | 0 |
| Backlogged | 1 |

---

## Completed Designs

| Date | Feature | Complexity | Status | Notes |
|------|---------|------------|--------|-------|
| 2025-12-22 | Race Simulation Overhaul | LARGE | Backlogged | 4 phases, complete F1 sim |

### Design Archive

*(Full designs are saved below when approved)*

---

## Design #1: Race Simulation Overhaul

**Date:** 2025-12-22
**Status:** ✅ COMPLETE - Saved to Backlog
**Priority:** HIGH
**Complexity:** LARGE (4 phases)
**Estimated Implementation:** 15-20 sessions

### Overview

Transform basic racing into a complete F1 simulation with authentic team/driver performance, tire strategy, wheel-to-wheel racing dynamics, and dramatic race events. Four interconnected phases creating emergent drama through systems under pressure.

### User Vision
- **Current Role:** Spectator mode
- **Future Role:** Team Principal / Manager
- **Feel:** Simcade (between simulation and arcade)
- **Priority:** Drama-filled races like real F1

---

### Phase 1: Foundation ✅

**Purpose:** The building blocks of authentic F1

| System | Description |
|--------|-------------|
| **2025 Grid** | 20 drivers, 10 teams, 5 rookies (Antonelli, Doohan, Hadjar, Bearman, Bortoleto) |
| **Team Tiers** | S/A/B/C/D performance (+4% to -5% pace) |
| **Car Characteristics** | Balance (-2 to +2), Corner Speed (-2 to +2), Traction (1-5) |
| **Driver Profiles** | Skill (70-99), Consistency (1-5), Racecraft (1-5), Style prefs |
| **Synergy System** | Car-driver match = ±2% to ±4% pace modifier |
| **Fuel Load** | -4% at start → 0% at end (+0.2%/lap) |
| **Pit Stops** | 22s base, AI timing by compound |

**Key Formula:**
```
FINAL PACE = BASE_CAR_SPEED × DRIVER_SKILL × SYNERGY × FUEL_MODIFIER
```

**2025 Team Tiers:**
- 🥇 S: Red Bull, McLaren
- 🥈 A: Ferrari, Mercedes
- 🥉 B: Aston Martin, Williams
- 🔷 C: RB, Alpine, Haas
- 🔹 D: Sauber

---

### Phase 2: Tire System ✅

**Purpose:** Strategy through rubber management

| System | Description |
|--------|-------------|
| **Compounds** | Soft (~10 laps), Medium (~15 laps), Hard (~22 laps) |
| **Grip Levels** | Soft +0%, Medium -4%, Hard -8% |
| **Degradation** | Non-linear curve with cliff at ~100% life |
| **Wear Display** | Percentage (0% fresh → 100% cliff) |
| **Interactions** | Car traction + Driver skill = ±35% wear rate |

**Degradation Phases:**
1. Green (warming) - First 1-2 laps
2. Peak (optimal) - Best performance
3. Degradation (gradual) - Losing grip
4. Cliff (danger) - Sudden dramatic drop

**Condition Icons:** 🟢 Fresh → 🟡 Used → 🟠 Worn → 🔴 Critical → 💀 Cliff

---

### Phase 3: Proximity Racing ✅

**Purpose:** The art of following and overtaking

| System | Description |
|--------|-------------|
| **Proximity Scaling** | Gap 0-2s drives ALL effects |
| **Straights** | +2% to +12% speed (DRS + slipstream) |
| **Corners - Dirty Air** | -1% to -10% grip, +10% to +40% tire wear |
| **Corner Types** | High-speed = 1.6× danger multiplier |
| **Alternative Lines** | Skilled drivers avoid dirty air (up to 90% reduction) |
| **Dirty Air Skill** | Derived from traction + consistency + balance |
| **Overtaking** | Hard by default (~15%), skill + DRS = ~50% |

**The Core Tension:**
- Close on straights = GOOD (speed boost)
- Close in corners = DANGEROUS (grip loss, tire wear, errors)
- Skill determines who can follow closely and when

**Alternative Lines:**
- Attempt rate: 25% (low skill) to 80% (high skill)
- Success: Avoid dirty air, stay close
- Failure: Lose time, higher error chance

---

### Phase 4: Drama ✅

**Purpose:** Where legends are made and hearts are broken

#### Driver Errors
| Trigger | Effect |
|---------|--------|
| Dirty air in corners | +error chance (high-speed = worse) |
| Worn tires (>60%) | +error chance (cliff = dangerous) |
| Pressure (defending) | +error chance |
| Low consistency | Multiplies all error chances |

**Error Types:** Lock-up (45%) → Run wide (28%) → Snap (15%) → Spin (9%) → Crash (3%)

#### Last Lap Aggression
- Stakes-based multiplier: 1.3× to 2.5×
- Win/podium fights = maximum aggression
- Points bubble (P10/P11) = desperate
- Higher error chance, more overtakes, more contact

#### Heat System
| Component | Sensitivity | Failure Type |
|-----------|-------------|--------------|
| Engine | Baseline | Power loss / DNF |
| Brakes | 1.3× faster | Brake failure / DNF |
| Gearbox | 0.8× slower | Stuck gear / DNF |

- Heat accumulates from dirty air exposure
- Team reliability: 0.75 (Sauber) to 0.92 (Mercedes)
- Warning → Danger → Critical → Failure

#### Heat Management Options
1. **Back off** - Cool down, lose position
2. **Send it & pass** - Get clean air (if available ahead)
3. **Lift & coast** - -3% pace, -60% heat gain
4. **Train leader breakaway** - Manage, let train cook, then push

#### DRS Trains
- 3+ cars within 1.5s = trapped
- Can't back off (car behind will pass)
- All accumulating heat
- Only options: send it or lift & coast

#### Safety Car
| Phase | Effect |
|-------|--------|
| Deployment | Triggered by crashes/incidents |
| During SC | Gaps compress, tires cool (-15%/lap), FREE pit window |
| Restart | Cold tires (-15% grip), aggression spike (1.8×+) |
| Post-restart | Feeding frenzy for 2-3 laps, chaos multiplier |

**Restart Chaos Formula:**
```
CHAOS = Cold Tires × Aggression × Pack Density × Battle Pressure
      = Up to 8× error multiplier!
```

---

### System Connections

```
PHASE 1 (Foundation)
    │ Team pace, driver skill, synergy
    ▼
PHASE 2 (Tires)
    │ Degradation forces strategy
    ▼
PHASE 3 (Proximity)
    │ Following = boost + danger
    ▼
PHASE 4 (Drama)
    │ Pressure → Errors → Incidents → Safety Car
    ▼
EMERGENT DRAMA
```

---

### Implementation Notes

**Suggested Build Order:**
1. Phase 1 first (foundation for everything)
2. Phase 2 (tires create strategy)
3. Phase 3 (racing dynamics)
4. Phase 4 (drama systems)

**Data Files Needed:**
- `data/teams_2025.py` - Updated grid
- `data/drivers.py` - Driver profiles
- `data/cars.py` - Car characteristics

**New Systems:**
- Synergy calculator
- Tire degradation engine
- Proximity effect system
- Heat accumulation tracker
- Error probability calculator
- Safety car state machine

---

## Feature Backlog

### High Priority
| Feature | Description | Complexity |
|---------|-------------|------------|
| Race Simulation Overhaul | Complete F1 sim - 4 phases | LARGE |

### Medium Priority
| Feature | Description | Complexity |
|---------|-------------|------------|
| - | None yet | - |

### Low Priority / Future
| Feature | Description | Complexity |
|---------|-------------|------------|
| Weather System | Rain, wet tires, chaos multiplier | MEDIUM |
| Team Orders | Swap positions, driver obedience | SMALL |
| Pit Stop Variance | Perfect/slow/disaster stops | SMALL |
| Fastest Lap Hunt | +1 point, purple sectors | SMALL |

---

## User Preferences

### Observed Preferences
- Loves drama and chaos
- Wants systems that interact and create emergent stories
- Prefers simcade (deep but accessible)
- Values authenticity to real F1
- Excited by: last lap battles, safety cars, mechanical failures
- Wants driver skill to matter significantly

### Style Preferences
- Visual style: F1 broadcast aesthetic
- Complexity preference: Simcade (deep systems, simple interface)
- F1 accuracy level: High (2025 grid, real characteristics)

---

## Game Vision Notes

### Current Theme
- 2D top-down racing
- F1 broadcast aesthetic
- Sprint race format (20 laps)
- Focus on visualization, not management

### Potential Directions
- Add strategy/management elements
- Add audio/immersion
- Add more race types
- Add season progression

---

## F1 Feature Reference

### Already Implemented
- [x] Live timing tower
- [x] Position tracking
- [x] Gap calculation
- [x] Tire compounds (visual)
- [x] Tire degradation (basic)
- [x] Lap counting
- [x] Results screen

### Not Yet Implemented
- [ ] Pit stops
- [ ] DRS
- [ ] Weather
- [ ] Qualifying
- [ ] Safety car
- [ ] Flags
- [ ] Radio messages
- [ ] Audio
- [ ] Sector times
- [ ] Speed traps
- [ ] Car setup
- [ ] Season mode

---

## Idea Templates

### Simple Visual Addition
```
Feature: [Name]
Location: [Where]
Visual: [What it looks like]
Behavior: [What it does]
Priority: [High/Med/Low]
```

### Gameplay Feature
```
Feature: [Name]
Mechanic: [How it works]
User Action: [What player does]
Effect: [What happens]
Risk/Reward: [Strategy element]
Priority: [High/Med/Low]
```

---

## Session Notes

### Current Session
Not yet started.

### Ideas Discussed
(To be populated during brainstorming)

---

## Design #2: Smooth Car Motion

**Date:** 2025-12-22
**Status:** ✅ COMPLETE - Sent to Pipeline
**Priority:** HIGH
**Complexity:** SMALL

### Overview
Fix the "laggy" feeling of car dots by implementing position interpolation, variance smoothing, and sub-pixel rendering.

### Root Cause Analysis
| Issue | Location | Problem |
|-------|----------|---------|
| **Pixel Snapping** | `renderer.py` line 258 | `int(x), int(y)` truncates to nearest pixel |
| **Speed Variance** | `car.py` line 159 | Random variance applied every frame causes jitter |
| **Discrete Updates** | `car.py` line 250 | Position jumps directly, no smoothing |

### Solution: Three-Part Fix

#### 1. Position Interpolation (Lerp)
Store previous position and smoothly interpolate toward target:
```python
# In Car class:
self.display_x = 0.0  # Smoothed display position
self.display_y = 0.0
self.target_x = 0.0   # Actual calculated position
self.target_y = 0.0

# Each frame:
SMOOTHING = 0.15  # Lower = smoother but more lag
self.display_x += (self.target_x - self.display_x) * SMOOTHING
self.display_y += (self.target_y - self.display_y) * SMOOTHING
```

#### 2. Variance Smoothing
Apply variance per LAP, not per frame:
```python
# Set once per lap in lap completion:
self.current_lap_variance = 1.0 + (random.random() * 2 - 1) * variance_factor

# Use stored value in pace calculation:
pace *= self.current_lap_variance
```

#### 3. Sub-Pixel Rendering
Remove int() truncation - pygame-ce supports floats:
```python
# Fixed (smooth):
pygame.draw.circle(..., (x, y), ...)  # No int()
```

### Files to Change
| File | Change |
|------|--------|
| `race/car.py` | Add display positions, lap variance, lerp logic |
| `ui/renderer.py` | Remove `int()` from draw calls |
| `config.py` | Add `CAR_SMOOTHING = 0.15` constant |

### Acceptance Criteria
- [ ] Cars move smoothly around the track
- [ ] No visible jumping/stuttering
- [ ] Natural, fluid motion
