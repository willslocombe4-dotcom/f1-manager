# Feature Coder Context

Last updated: 2025-12-21
STATUS: IDLE

## Currently Implementing

*Nothing in progress*

## Recently Completed

- Enhanced Track Visuals (2025-12-21)
  - Added two-tone grass background with random patches
  - Implemented gravel traps at corners (detected by curvature threshold)
  - Added red-and-white striped kerbs at inner corners
  - Implemented checkered start/finish line pattern
  - Added static surface caching for performance optimization
  - Files modified: config.py, race/track.py, ui/renderer.py
  - Implementation confidence: HIGH (95%)
  - Testing: Game runs without errors, visuals render correctly

- Results screen scrolling (2025-12-21)
  - Added scroll state tracking (scroll_offset, visible_rows=15, max_scroll)
  - Implemented keyboard scrolling (UP/DOWN arrow keys)
  - Implemented mouse wheel scrolling
  - Added scroll indicators (up/down arrows and position counter)
  - Only renders visible rows for performance
  - Scroll resets when starting new race or restarting
  - All 20 drivers now accessible via scrolling

- Basic race visualization (Phase 1)
  - Track rendering with 62 waypoints
  - Car movement with progress system
  - Timing screen with gaps
  - Results screen
  - Speed tuning (BASE_SPEED = 0.25)

## Known Issues

*None currently*

## Code Conventions

### Imports
```python
import pygame
import config
from race.race_engine import RaceEngine
```

### Class Structure
```python
class ClassName:
    """Docstring"""

    def __init__(self):
        pass

    def public_method(self):
        pass

    def _private_method(self):
        pass
```

### Drawing Pattern
```python
def render(self, race_engine):
    # Get data from race_engine
    cars = race_engine.cars

    # Draw stuff
    pygame.draw.circle(...)
```

### Config Pattern
```python
# In config.py
CONSTANT_NAME = value

# Usage
import config
x = config.CONSTANT_NAME
```

## File Locations

- New UI components go in `ui/`
- Race logic goes in `race/`
- Data files go in `data/`
- Main entry point is `main.py`

## Testing

Run with: `python main.py`

Controls:
- SPACE: Start race / Pause / New race (after finish)
- R: Restart race
- UP/DOWN arrows: Scroll results (when race finished)
- Mouse wheel: Scroll results (when race finished)
- ESC: Quit

## Gotchas

- Track waypoints form closed loop - last connects to first
- Progress resets to 0 when completing lap
- Cars sorted by total_progress for race order
- Pygame Y axis is inverted (0 at top)

## Performance Notes

- 60 FPS target
- 20 cars updating each frame
- Track polygon redrawn each frame

## Next Up

*Waiting for plans*
