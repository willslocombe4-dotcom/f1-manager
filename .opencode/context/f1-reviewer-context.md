# F1 Reviewer Context

**Last Updated:** 2025-12-28

---

## Review Statistics

| Metric | Value |
|--------|-------|
| Total Reviews | 5 |
| Approved | 1 |
| Needs Changes | 4 |
| Blocked | 0 |
| Issues Found | 14 |

---

## Recent Reviews

| Date | Type | Files | Verdict | Issues | Notes |
|------|------|-------|---------|--------|-------|
| Dec 28 | Bug Fix | main.py, config.py, ui/settings_display_simple.py, settings/* | NEEDS CHANGES | 7 | 4K Display Unplayable. Forced fullscreen, no display settings persistence. |
| Dec 25 | Feature | ui/track_selection.py | NEEDS CHANGES | 2 | Scrollable Track Selection. Empty list edge case, Page Up/Down optimization. |
| Dec 25 | Feature | config.py, race/track.py, ui/renderer.py | APPROVED | 0 | Smart Track Boundaries. Clean geometry math, proper edge case handling. |
| Dec 22 | Bug Fix | config.py, race/car.py, race/race_engine.py | NEEDS CHANGES | 2 | Gap Logic Bug. Simulation speed too fast. |
| Dec 22 | Feature | config.py, data/teams.py, assets/colors.py, race/car.py, race/race_engine.py, ui/renderer.py | NEEDS CHANGES | 3 | Phase 1 Foundation. Critical font performance issue. |

---

## Common Issues Found

### By Category
| Category | Count | Last Seen |
|----------|-------|-----------|
| Display/Resolution | 3 | Dec 28 |
| Pygame Performance | 2 | Dec 28 |
| Hardcoded Values | 2 | Dec 28 |
| Simulation Logic | 1 | Dec 22 |
| Pattern Violations | 0 | - |
| F1 Accuracy | 0 | - |

### Issue Log
- **Dec 28**: `main.py` forces fullscreen at native resolution, making 4K displays unplayable (Critical).
- **Dec 28**: `ui/settings_display_simple.py` is read-only, users cannot change display settings (Critical).
- **Dec 28**: `main.py:319` creates font every frame for FPS display (Minor).
- **Dec 28**: Display settings not persisted in `user_config.json` (Major).
- **Dec 22**: `config.py` `BASE_SPEED` set too high (0.25), causing 4s laps and tiny time gaps (Critical).
- **Dec 22**: `ui/renderer.py` creating `pygame.font.Font` inside render loop (Critical).
- **Dec 22**: `race/car.py` using hardcoded magic numbers for physics (Major).

---

## Common Issues to Watch

### Critical
- Crashes / exceptions
- Infinite loops
- Data corruption
- **Display initialization that forces fullscreen without user option**

### Pygame Performance
- Surface creation in render loops
- Font creation every frame
- Surfaces cached in __init__
- Fonts cached in __init__

### Patterns
- Values should come from config.py
- Colors from assets/colors.py
- Follow existing code style
- **Display settings must be persisted and loaded before pygame.display.set_mode()**

---

## Codebase Quality Notes

### Files That Need Attention
| File | Issue | Priority | Notes |
|------|-------|----------|-------|
| `main.py` | Forced fullscreen, font in render loop | Critical | 4K displays unplayable |
| `ui/settings_display_simple.py` | Read-only display settings | Critical | Users can't change resolution |
| `settings/runtime_config.py` | Missing display settings | Major | Need width, height, fullscreen |
| `config.py` | Missing SUPPORTED_RESOLUTIONS | Minor | Add resolution options |

### Known Technical Debt
| Area | Description | Impact |
|------|-------------|--------|
| Display | Forced fullscreen at native resolution | 4K users can't play |
| Display | No display settings persistence | Settings lost on restart |
| Physics | High frequency variance (60Hz) | Jittery movement |
| Time Scale | Simulation runs at ~20x speed | Confusing for users |

### Good Patterns to Preserve
| Pattern | Where | Why It's Good |
|---------|-------|---------------|
| Surface caching | ui/renderer.py | Performance |
| Config centralization | config.py | Maintainability |
| Team data structure | data/teams.py | Clean, extensible |
| Settings persistence | settings/persistence.py | Extensible for display settings |

---

## Review Checklist

### Project-Specific Rules
1. All colors must come from config.py or assets/colors.py
2. All speeds/sizes must come from config.py
3. Car state changes only in race_engine.update() loop
4. UI renders read-only from race_engine state
5. **Display settings must be loaded before creating pygame display**
6. **Game should start in windowed mode by default**

### Known Edge Cases
| Area | Edge Case | How to Handle |
|------|-----------|---------------|
| Car progress | progress = 1.0 exactly | Wraps to 0.0, lap increments |
| Race end | leader.lap > total_laps | is_race_finished() returns True |
| Position calc | Two cars same progress | lateral_offset separates visually |
| Gap Display | Fast simulation speed | Ensure time gaps match visual expectations |
| **Display** | **4K/high-DPI screens** | **Start windowed, let user choose fullscreen** |

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
- [2025-12-25] **Easy to Miss:** Empty list edge cases with `len(list) - 1` | **Check:** Any `list[-1]` or `len(list) - 1` when list could be empty
- [2025-12-28] **Easy to Miss:** Display initialization that forces fullscreen | **Check:** Verify games start in reasonable windowed mode with user-configurable display settings

### False Positives
<!-- Things flagged that weren't actually issues -->

### Review Patterns
<!-- Checks that consistently find problems -->
- [2025-12-24] **Pattern:** Check all new Surface/Font creations are in __init__ | **Catches:** Performance issues
- [2025-12-24] **Pattern:** Trace data flow from RuntimeConfig to UI | **Catches:** Stale cache issues
- [2025-12-24] **Pattern:** Test edge cases mentally (negative, zero, max) | **Catches:** Boundary bugs
- [2025-12-25] **Pattern:** For geometry code, verify division-by-zero guards | **Catches:** Math errors at edge cases
- [2025-12-25] **Pattern:** Check docstrings match implementation after deviations | **Catches:** Misleading documentation
- [2025-12-25] **Pattern:** For scrollable lists, verify: empty list, fewer items than visible, exactly visible, many items | **Catches:** Scroll boundary bugs
- [2025-12-25] **Pattern:** For mouse interaction with scrolled lists, trace index mapping carefully | **Catches:** Wrong item selection
- [2025-12-28] **Pattern:** For display/resolution code, test on multiple screen sizes (1080p, 1440p, 4K) | **Catches:** Scaling and positioning bugs
- [2025-12-28] **Pattern:** Verify display settings are loaded BEFORE pygame.display.set_mode() | **Catches:** Settings not applied on startup

### Codebase Rules
<!-- Project-specific rules to enforce -->
- All constants in config.py, never hardcoded
- All colors from assets/colors.py or config.py
- Car state changes only in Car.update()
- UI components are read-only from race_engine
- Geometry helpers should handle zero-length segments gracefully
- **Display settings must be persisted and loaded before creating the display**
- **Game should default to windowed mode at base resolution (1600x900)**
