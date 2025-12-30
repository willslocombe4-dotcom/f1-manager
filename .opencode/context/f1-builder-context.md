# F1 Builder Context

**Last Updated:** 2025-12-28

---

## Implementation History

### Features
| Date | Feature | Files Changed | Result |
|------|---------|---------------|--------|
| - | - | - | No features yet |

### Bug Fixes
| Date | Bug | Root Cause | Fix |
|------|-----|------------|-----|
| 2025-12-28 | Game unplayable on 4K screens | Started in fullscreen at native resolution | Start in windowed 1600x900 by default |
| 2025-12-28 | Display settings not working | Window not resizable, apply button didn't resize | Added pygame.RESIZABLE flag, handle VIDEORESIZE event |
| 2025-12-28 | Display settings not persisting | Settings only saved when leaving config screen | Save on window resize and game exit |

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

## Learnings

### Pygame Gotchas
<!-- Performance traps, API quirks, rendering issues -->
- [2025-12-24] **Gotcha:** Creating fonts/surfaces in render loop kills performance | **Fix:** Cache in __init__, only blit in render
- [2025-12-24] **Gotcha:** pygame.draw coords should be ints for older pygame | **Fix:** Use int() or let pygame-ce handle floats
- [2025-12-28] **Gotcha:** Window resize requires recreating UI components | **Fix:** Recreate all UI objects in _handle_window_resize()

### Python Gotchas
<!-- Language quirks that caused bugs -->
- [2025-12-24] **Gotcha:** int() rounds toward zero, not down | **Fix:** Use math.floor() for negative numbers (e.g., car progress)
- [2025-12-24] **Gotcha:** Dict/list default args are mutable and shared | **Fix:** Use None default, create in function

### Debug Wins
<!-- How you found tricky bugs, what to check first -->
- [2025-12-24] **Win:** Lap 1 corner cutting was negative progress + int() | **Check:** Always test with negative values when progress/index involved
- [2025-12-24] **Win:** Gravel on wrong side was fixed perpendicular direction | **Check:** Use cross product to detect turn direction
- [2025-12-28] **Win:** Settings not persisting found by checking save() calls | **Check:** Trace when settings are saved vs when they change

### Code Patterns
<!-- Implementations that worked well -->
- [2025-12-24] **Pattern:** Cross product for turn direction: `(x2-x1)*(y3-y2) - (y2-y1)*(x3-x2)` | **Use:** Positive=left turn, negative=right turn
- [2025-12-24] **Pattern:** Waypoint interpolation for smooth movement | **Use:** `t = exact_index - math.floor(exact_index)` then lerp
- [2025-12-28] **Pattern:** Load settings before creating display | **Use:** SettingsPersistence.load() before pygame.display.set_mode()
- [2025-12-28] **Pattern:** Interactive settings with visual feedback | **Use:** Arrows show selector, color changes for toggles
- [2025-12-28] **Pattern:** Handle window resize events | **Use:** VIDEORESIZE event, recreate surfaces, update config values
- [2025-12-28] **Pattern:** Save settings on state changes | **Use:** Save on window resize, game exit, not just config screen exit

---

## Files Frequently Changed

| File | Purpose | Watch For |
|------|---------|-----------|
| `race/car.py` | Car state | Property init + update |
| `ui/timing_screen.py` | Timing display | Column positioning |
| `config.py` | Constants | Use these, don't hardcode |