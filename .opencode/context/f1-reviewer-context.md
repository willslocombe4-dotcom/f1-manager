# F1 Reviewer Context

**Last Updated:** Not yet used

---

## Review Statistics

| Metric | Value |
|--------|-------|
| Total Reviews | 0 |
| Approved | 0 |
| Needs Changes | 0 |
| Blocked | 0 |
| Issues Found | 0 |

---

## Recent Reviews

| Date | Type | Files | Verdict | Issues | Notes |
|------|------|-------|---------|--------|-------|
| - | - | - | - | - | No reviews yet |

---

## Common Issues Found

### By Category
| Category | Count | Last Seen |
|----------|-------|-----------|
| Pygame Performance | 0 | - |
| Hardcoded Values | 0 | - |
| Pattern Violations | 0 | - |
| Logic Errors | 0 | - |
| F1 Accuracy | 0 | - |

### Issue Log
None recorded yet.

---

## Codebase Quality Notes

### Files That Need Attention
| File | Issue | Priority | Notes |
|------|-------|----------|-------|
| - | None identified | - | - |

### Known Technical Debt
| Area | Description | Impact |
|------|-------------|--------|
| - | None tracked | - |

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
Not yet started.

### Observations
(To be populated during reviews)
