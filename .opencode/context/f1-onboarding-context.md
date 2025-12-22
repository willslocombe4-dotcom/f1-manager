# Feature Briefing: Race Simulation Overhaul - Phase 1: Foundation

**Prepared by:** @f1-onboarding
**Date:** 2025-12-22
**For:** @f1-feature-planner

---

## Feature Overview

### What It Does
Establishes the core simulation physics and data for the 2025 season. It replaces the current random speed logic with a deterministic yet dynamic system based on:
1.  **2025 Grid**: Real teams/drivers with performance tiers.
2.  **Physics**: Fuel load, tire degradation, and car characteristics.
3.  **Driver Skills**: Individual stats affecting pace and consistency.
4.  **Synergy**: Bonus/penalty for driver-car fit.

### User Interaction
- **Visuals**: Players will see realistic gaps forming based on car performance (Red Bull pulling away, Alpine fighting in midfield).
- **Timing Screen**: Will reflect tire strategies and pace evolution as fuel burns.
- **No direct control** in this phase, but the simulation becomes "watchable" and strategic.

### F1 Context
Reflects the 2025 season dynamics:
- **Rookies**: Antonelli (Merc), Doohan (Alpine), Hadjar (RB), Bearman (Haas), Bortoleto (Sauber).
- **Team Tiers**: Distinct performance gaps (S-Tier to D-Tier).

---

## Codebase Analysis

### Architecture Summary
The current system is simple:
- `data/teams.py` holds a basic list of 2024 drivers.
- `race/car.py` calculates speed once at spawn: `BASE_SPEED` + random variance + grid position bonus.
- `race/race_engine.py` moves cars linearly.

**We need to shift from "Spawn Speed" to "Per-Frame Dynamic Speed".**

### Relevant Files

| File | Purpose | Relevance to Feature |
|------|---------|---------------------|
| `data/teams.py` | Static data source | **CRITICAL**: Needs complete replacement with 2025 grid & stats. |
| `race/car.py` | Car logic | **CRITICAL**: Needs new `update_speed()` logic using the new formula. |
| `config.py` | Constants | **HIGH**: Needs new physics constants (fuel weights, tier modifiers). |
| `race/race_engine.py` | Simulation loop | **MEDIUM**: Needs to pass new data to Car init. |
| `assets/colors.py` | Visuals | **LOW**: Update for Sauber/RB/Alpine colors. |

### Key Code Sections

#### Current Speed Logic (to be replaced)
```python
# race/car.py:24
base_speed = config.BASE_SPEED
speed_modifier = 1.0 + (random.random() * config.SPEED_VARIANCE - config.SPEED_VARIANCE / 2)
position_modifier = 1.0 - (starting_position - 1) * 0.01
self.speed = base_speed * speed_modifier * position_modifier
```
**Why this matters:** This static speed must be replaced by a dynamic property that changes every frame (or lap) based on fuel and tires.

#### Data Structure (to be expanded)
```python
# data/teams.py:5
TEAMS_DATA = [
    {
        "name": "Red Bull Racing",
        "drivers": [...]
    }
]
```
**Why this matters:** This structure is too simple. We need to add `tier`, `characteristics` to teams, and `skill`, `consistency`, `style` to drivers.

---

## Integration Points

### 1. Data Layer (`data/teams.py`)
**Action:** Replace `TEAMS_DATA` with a richer structure.

**Recommended Structure:**
```python
TEAMS_2025 = [
    {
        "name": "Red Bull Racing",
        "tier": "S",
        "characteristics": {"balance": 2, "cornering": 1, "traction": 5},
        "drivers": [
            {"name": "Max Verstappen", "skill": 99, "consistency": 5, "style": "aggressive"},
            ...
        ]
    },
    ...
]
```

### 2. Configuration (`config.py`)
**Action:** Add physics constants.

```python
# Physics
FUEL_START_PENALTY = 0.04  # -4% speed at start
FUEL_BURN_PER_LAP = 0.002  # +0.2% speed per lap
TIER_MODIFIERS = {
    "S": 1.04, "A": 1.02, "B": 1.00, "C": 0.98, "D": 0.95
}
PIT_STOP_BASE_TIME = 22.0
```

### 3. Car Physics (`race/car.py`)
**Action:** Rewrite `__init__` and `update`.

**New Attributes:**
- `self.fuel_load` (starts at 1.0, decreases)
- `self.base_performance` (calculated from Tier + Car Stats)
- `self.driver_factor` (Skill + Synergy)

**New Method `_calculate_current_pace()`:**
```python
def _calculate_current_pace(self):
    # 1. Base Car Pace (Tier)
    pace = config.BASE_SPEED * config.TIER_MODIFIERS[self.team_tier]
    
    # 2. Driver Skill (0.70 to 0.99 factor)
    pace *= (self.driver_skill / 100.0)
    
    # 3. Synergy (±2-4%)
    pace *= self.synergy_factor
    
    # 4. Fuel (Linear penalty removal)
    fuel_penalty = self.current_fuel * config.FUEL_START_PENALTY
    pace *= (1.0 - fuel_penalty)
    
    # 5. Tires (Degradation)
    tire_deg = self.tire_age * config.TIRE_DEG_PER_LAP
    pace *= (1.0 - tire_deg)
    
    return pace
```

---

## Patterns to Follow

### Data Access
Keep data in `data/` modules. Do not hardcode stats in `car.py`.

### Config Usage
All "magic numbers" (burn rate, tier gaps) must go in `config.py` for easy balancing later.

### State Management
The `Car` class should own its state. `RaceEngine` should only call `car.update()`.

---

## Edge Cases to Consider

| Scenario | How to Handle |
|----------|---------------|
| **Pit Stops** | When `tire_age` > threshold, car stops moving for `PIT_STOP_TIME` frames. |
| **Lapped Cars** | The logic already handles position by `total_progress`. Ensure pace formula doesn't break this. |
| **Zero Fuel** | Fuel shouldn't reach 0 (it's a modifier, not a tank). Just ensure it stops burning at 0%. |

---

## Testing Scenarios

1.  **Tier Check**: Verify Red Bull (Tier S) is consistently faster than Sauber (Tier D) over 1 lap.
2.  **Fuel Burn**: Verify lap times improve slightly each lap (ignoring tire wear).
3.  **Synergy**: Create two identical cars/drivers, give one +Synergy and one -Synergy. Verify the gap.
4.  **Rookie Check**: Ensure all 5 rookies appear on the grid.

---

## Estimated Complexity

**Level:** Medium
**Reasoning:** The logic isn't complex, but it touches the core movement loop and requires a full data rewrite.
**Estimated Files Changed:** 4 (`teams.py`, `config.py`, `car.py`, `colors.py`)

---

## Handoff

This briefing is ready for @f1-feature-planner.

### Key Decisions Needed
- **Pit Logic**: Should we implement actual pit stops (car stops on track) or just add time to the lap? *Recommendation: For Phase 1, just add time to `self.lap_time` and reset tires.*
- **Synergy Calculation**: How is it determined? *Recommendation: Random assignment at start (High/Neutral/Low) for now, or based on "Style" match.*

### Open Questions
- None. The requirements are clear.
