# F1 Reviewer Context

**Last Updated:** 2025-12-23

---

## Review Statistics

| Metric | Value |
|--------|-------|
| Total Reviews | 2 |
| Approved | 0 |
| Needs Changes | 2 |
| Blocked | 0 |
| Issues Found | 5 |

---

## Recent Reviews

| Date | Type | Files | Verdict | Issues | Notes |
|------|------|-------|---------|--------|-------|
| Dec 22 | Bug Fix | config.py, race/car.py, race/race_engine.py | NEEDS CHANGES 🔄 | 2 | Gap Logic Bug. Simulation speed too fast. |
| Dec 22 | Feature | config.py, data/teams.py, assets/colors.py, race/car.py, race/race_engine.py, ui/renderer.py | NEEDS CHANGES 🔄 | 3 | Phase 1 Foundation. Critical font performance issue. |

---

## Common Issues Found

### By Category
| Category | Count | Last Seen |
|----------|-------|-----------|
| Pygame Performance | 1 | Dec 22 |
| Hardcoded Values | 1 | Dec 22 |
| Simulation Logic | 1 | Dec 22 |
| Pattern Violations | 0 | - |
| F1 Accuracy | 0 | - |

### Issue Log
- **Dec 22**: `config.py` `BASE_SPEED` set too high (0.25), causing 4s laps and tiny time gaps (Critical).
- **Dec 22**: `ui/renderer.py` creating `pygame.font.Font` inside render loop (Critical).
- **Dec 22**: `race/car.py` using hardcoded magic numbers for physics (Major).

---

## Common Issues to Watch

### 🔴 Critical
- Crashes / exceptions
- Infinite loops
- Data corruption

### 🟡 Pygame Performance
- ❌ Surface creation in render loops
- ❌ Font creation every frame
- ✅ Surfaces cached in __init__
- ✅ Fonts cached in __init__

### 🟡 Patterns
- Values should come from config.py
- Colors from assets/colors.py
- Follow existing code style

---

## Codebase Quality Notes

### Files That Need Attention
| File | Issue | Priority | Notes |
|------|-------|----------|-------|
| `config.py` | Incorrect simulation constants | Critical | Fixes gap display bug |
| `ui/renderer.py` | Font creation in loop | Critical | Must fix before merge |
| `race/car.py` | Hardcoded physics constants | Major | Should move to config |

### Known Technical Debt
| Area | Description | Impact |
|------|-------------|--------|
| Physics | High frequency variance (60Hz) | Jittery movement |
| Time Scale | Simulation runs at ~20x speed | Confusing for users |

### Good Patterns to Preserve
| Pattern | Where | Why It's Good |
|---------|-------|---------------|
| Surface caching | ui/renderer.py | Performance |
| Config centralization | config.py | Maintainability |
| Team data structure | data/teams.py | Clean, extensible |

---

## Review Checklist

### Project-Specific Rules
1. All colors must come from config.py or assets/colors.py
2. All speeds/sizes must come from config.py
3. Car state changes only in race_engine.update() loop
4. UI renders read-only from race_engine state

### Known Edge Cases
| Area | Edge Case | How to Handle |
|------|-----------|---------------|
| Car progress | progress = 1.0 exactly | Wraps to 0.0, lap increments |
| Race end | leader.lap > total_laps | is_race_finished() returns True |
| Position calc | Two cars same progress | lateral_offset separates visually |
| Gap Display | Fast simulation speed | Ensure time gaps match visual expectations |

---

## F1 Domain Knowledge

### Correct Terminology
| Term | Meaning | Usage |
|------|---------|-------|
| DRS | Drag Reduction System | Rear wing opens on straights |
| Stint | Period on one set of tires | Between pit stops |
| Undercut | Pit early to gain advantage | Strategy term |
| Overcut | Pit late to gain advantage | Strategy term |
| Blue flag | Let faster car pass | For lapped cars |

### 2024/2025 Season Data
- 10 teams, 20 drivers
- Teams in data/teams.py
- Team colors in assets/colors.py

---

## Learnings

### Easy to Miss
<!-- Issues that slipped past, how to catch them -->
- [2025-12-24] **Missed:** Font creation in render loop | **Check:** Grep for `pygame.font.Font` in any render/draw method
- [2025-12-24] **Missed:** int() vs math.floor() for negative numbers | **Check:** Any index calculation with potentially negative values

### False Positives
<!-- Things flagged that weren't actually issues -->

### Review Patterns
<!-- Checks that consistently find problems -->
- [2025-12-24] **Pattern:** Check all new Surface/Font creations are in __init__ | **Catches:** Performance issues
- [2025-12-24] **Pattern:** Trace data flow from RuntimeConfig to UI | **Catches:** Stale cache issues
- [2025-12-24] **Pattern:** Test edge cases mentally (negative, zero, max) | **Catches:** Boundary bugs

### Codebase Rules
<!-- Project-specific rules to enforce -->
- All constants in config.py, never hardcoded
- All colors from assets/colors.py or config.py
- Car state changes only in Car.update()
- UI components are read-only from race_engine
