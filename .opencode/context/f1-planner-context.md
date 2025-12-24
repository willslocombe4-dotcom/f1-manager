# F1 Planner Context

**Last Updated:** 2025-12-23

---

## Plans Created

| Date | Feature | Steps | Complexity | Result |
|------|---------|-------|------------|--------|
| - | - | - | - | No plans yet |

---

## Codebase Knowledge

### Architecture
```
main.py (F1Manager) → RaceEngine → Cars + Track → UI Components
```

### Key Integration Points
| Add This | Here | Pattern |
|----------|------|---------|
| Constant | config.py | `VALUE = x` |
| Car state | race/car.py __init__ | `self.x = val` |
| Timing column | ui/timing_screen.py render | Add text blit |
| Visual | ui/renderer.py | Add `_draw_x()` method |

### File Purposes
- `main.py` — Game loop, event handling
- `config.py` — All constants
- `race/race_engine.py` — Simulation, owns cars
- `race/car.py` — Car state, movement
- `race/track.py` — Waypoints, positioning
- `ui/renderer.py` — Track + car drawing
- `ui/timing_screen.py` — Timing tower
- `ui/results_screen.py` — End display

---

## Common Patterns

### Adding Car Property
1. Add in `Car.__init__`
2. Update in `Car.update()` if needed
3. Read in timing/renderer

### Adding Timing Column
1. Add header text
2. Add per-car value
3. Adjust x positions if needed

---

## Learnings

### Architecture Insights
<!-- How components connect, data flow discoveries -->
- [2025-12-24] **Insight:** RuntimeConfig is singleton but UI screens cache values at creation | **Impact:** Plans must include cache invalidation when settings change
- [2025-12-24] **Insight:** Cars use negative progress for grid formation (staggered start) | **Impact:** Any progress-related code must handle negative values

### Integration Gotchas
<!-- Hidden dependencies, order-of-operations issues -->
- [2025-12-24] **Gotcha:** Track boundaries (outer/inner points) are relative to track direction, not absolute | **Impact:** Turn direction detection needed for correct gravel/kerb placement
- [2025-12-24] **Gotcha:** Presets load into RuntimeConfig but cached UI screens show old values | **Impact:** Must clear screen cache after preset load

### Estimation Misses
<!-- Plans that were too simple/complex, why -->

### Analysis Patterns
<!-- Approaches that led to better plans -->
- [2025-12-24] **Pattern:** Read ALL files that touch the feature before planning | **Impact:** Prevents missed integration points
- [2025-12-24] **Pattern:** Check for negative/edge case handling in existing code | **Impact:** Reveals hidden assumptions (like int() vs floor())
