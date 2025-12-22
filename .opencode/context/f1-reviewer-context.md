# F1 Reviewer Context

**Last Updated:** Mon Dec 22 2025

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
| Time Scale | Simulation runs at ~20x speed | Confusing for users expecting real-time |

### Good Patterns to Preserve
| Pattern | Where | Why It's Good |
|---------|-------|---------------|
| Surface caching | ui/renderer.py | Performance |
| Config centralization | config.py | Maintainability |
| Team data structure | data/teams.py | Clean, extensible |

---

## Review Checklist Customizations

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

### 2024 Season Data
- 10 teams, 20 drivers
- Teams in data/teams.py are accurate
- Team colors in assets/colors.py

---

## Review Templates

### Quick Approval
```markdown
# Code Review: [Name]
## Summary
Clean implementation following existing patterns.
## Verdict: APPROVED ✅
## Handoff
@f1-git-manager: Commit with `feat: [description]`
```

### Needs Minor Changes
```markdown
# Code Review: [Name]
## Summary
Good work, minor issues to address.
## Verdict: NEEDS CHANGES 🔄
## Issues
### 🟡 Major
1. [Issue] - `file:line` - [fix]
## Handoff
@f1-feature-coder: Fix listed issues, then return for re-review.
```

---

## Session Notes

### Current Session
Investigated Gap Logic Bug. Found that `BASE_SPEED` was set to 0.25, resulting in 4.33s laps. This caused time gaps to be ~20x smaller than visually expected. Recommended reducing `BASE_SPEED` to 0.045 and adjusting pit stop times.

### Observations
- The 2025 grid data is very detailed and accurate.
- The physics model is robust but needs tuning constants extracted.
