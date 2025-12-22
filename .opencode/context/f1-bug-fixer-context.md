# F1 Bug Fixer Context

**Last Updated:** Not yet used

---

## Fix Statistics

| Metric | Value |
|--------|-------|
| Bugs Fixed | 0 |
| First-Try Success | 0 |
| Required Revision | 0 |
| Lines Changed | 0 |

---

## Bug Fix History

| Date | Bug | File:Line | Fix Applied | Testing | Notes |
|------|-----|-----------|-------------|---------|-------|
| - | - | - | - | - | No fixes yet |

---

## Common Fix Patterns Used

### By Type
| Pattern | Times Used | Last Used |
|---------|------------|-----------|
| Off-by-one | 0 | - |
| Null check | 0 | - |
| Wrap-around | 0 | - |
| State reset | 0 | - |
| Type conversion | 0 | - |
| Surface caching | 0 | - |

---

## Files Most Frequently Fixed

| File | Fixes | Common Issues |
|------|-------|---------------|
| - | 0 | No data yet |

---

## Testing Checklist

### Basic Tests (Every Fix)
- [ ] `python main.py` runs without error
- [ ] Game starts and shows track
- [ ] Space starts race
- [ ] Cars move
- [ ] Timing screen updates
- [ ] Race ends correctly

### Feature-Specific Tests
(Add as bugs are fixed in specific areas)

---

## Lessons Learned

### What Works
(To be populated as fixes are made)

### Pitfalls to Avoid
(To be populated from experience)

---

## Code Snippets Reference

### Safe Progress Handling
```python
# When updating car progress
self.progress += speed_per_frame
if self.progress >= 1.0:
    self.progress -= 1.0  # Wrap around
    self.lap += 1         # Increment lap
```

### Safe Position Access
```python
# When accessing car by position
if i < len(self.cars):
    car = self.cars[i]
```

### Safe Config Access
```python
# Always import specific values
from config import SCREEN_WIDTH, CAR_SIZE
# Don't hardcode values
```

---

## Current State

### Active Fix
None

### Pending Review
None

### Recently Completed
None

---

## Session Notes

### Current Session
Not yet started.

### In Progress
None.
