# F1 Builder Context

**Last Updated:** 2025-12-23

---

## Implementation History

### Features
| Date | Feature | Files Changed | Result |
|------|---------|---------------|--------|
| - | - | - | No features yet |

### Bug Fixes
| Date | Bug | Root Cause | Fix |
|------|-----|------------|-----|
| - | - | - | No fixes yet |

---

## Code Patterns

### Pygame Surface Caching
```python
# In __init__
self.surface = pygame.Surface((w, h))
self.font = pygame.font.Font(None, 24)

# In render - just use them
self.screen.blit(self.surface, pos)
```

### Config Usage
```python
from config import SCREEN_WIDTH, VALUE
# or
import config
x = config.SCREEN_WIDTH
```

### Adding Car State
```python
# In Car.__init__
self.new_property = initial_value

# In Car.update
self.new_property = calculated_value
```

---

## Common Issues

None documented yet.

---

## Files Frequently Changed

| File | Purpose | Watch For |
|------|---------|-----------|
| `race/car.py` | Car state | Property init + update |
| `ui/timing_screen.py` | Timing display | Column positioning |
| `config.py` | Constants | Use these, don't hardcode |
