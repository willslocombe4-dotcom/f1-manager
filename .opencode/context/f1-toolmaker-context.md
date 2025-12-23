# F1 Toolmaker Context

**Last Updated:** 2025-12-23

---

## Tools Built

| Date | Tool | Lines | Status |
|------|------|-------|--------|
| Pre-existing | track_editor.py | ~400 | Complete |

---

## Tool Patterns

### Standard Structure
```python
class ToolName:
    def __init__(self):
        pygame.init()
        # Setup window, fonts, state
    
    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()
    
    def _save(self):
        # Save to JSON
    
    def _export(self):
        # Export to game format
```

### Common Constants
```python
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60
BG_COLOR = (15, 15, 15)
TEXT_COLOR = (255, 255, 255)
```

---

## Lessons Learned

None yet — tools pending.
