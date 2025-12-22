# F1 Onboarding Context

**Last Updated:** Not yet used

---

## Briefing Statistics

| Metric | Value |
|--------|-------|
| Total Briefings | 0 |
| Avg Complexity | N/A |
| Files Analyzed | 0 |

---

## Recent Briefings

| Date | Feature | Complexity | Files | Outcome |
|------|---------|------------|-------|---------|
| - | - | - | - | No briefings yet |

---

## Codebase Knowledge Base

### Architecture Understanding

#### Main Loop (main.py)
```
F1Manager class:
- __init__: Creates RaceEngine, TrackRenderer, TimingScreen, ResultsScreen
- handle_events: SPACE=start/pause, R=restart, ESC=quit
- update: Calls race_engine.update() if running
- render: Draws track OR results screen
- run: 60 FPS game loop
```

#### Race Engine (race/race_engine.py)
```
RaceEngine class:
- __init__: Creates Track, shuffles grid, creates 20 Cars
- update: Moves all cars, sorts by position, calculates gaps
- get_cars_by_position: Returns sorted car list
- is_race_finished: leader.lap > total_laps
```

#### Car State (race/car.py)
```
Car class:
- Position tracking: progress (0-1), lap (int), position (1-20)
- Performance: speed (varies), tire_compound, tire_age
- Timing: gap_to_leader, gap_to_ahead, lap_time, best_lap_time
- Visual: lateral_offset (for side-by-side)
- update(): Moves car, handles lap completion, tire degradation
```

#### Track Geometry (race/track.py)
```
Track class:
- waypoints: List of (x,y) tuples forming racing line
- get_position(progress): 0-1 progress → (x,y) screen coords
- get_angle(progress): Direction at that point
- get_offset_position(progress, offset): For side-by-side positioning
- get_track_boundaries(width): Returns outer/inner edge points
```

### Common Patterns

#### Surface Caching
```python
# Pattern from ui/renderer.py
class SomeRenderer:
    def __init__(self, surface):
        self.surface = surface
        self.cached_surface = pygame.Surface((w, h))  # Create ONCE
        self.static_surface = None  # Lazy init for complex static content
```

#### Config Usage
```python
# Pattern everywhere
import config
# or
from config import SPECIFIC_VALUE
```

#### Reading Race State
```python
# Pattern from UI components
def render(self, race_engine):
    cars = race_engine.get_cars_by_position()
    leader = race_engine.get_leader()
    status = race_engine.get_race_status()
```

---

## Integration Point Map

### Adding New Visual Element
1. Create new class in `ui/` or add method to existing renderer
2. Initialize any surfaces in `__init__`
3. Add render call in `F1Manager.render()`
4. Pass `race_engine` for data access

### Adding New Car State
1. Add property to `Car.__init__`
2. Update in `Car.update()` or `RaceEngine.update()`
3. Access from UI via `race_engine.get_cars_by_position()`

### Adding New Config Value
1. Add constant to `config.py`
2. Import where needed
3. Never hardcode values in other files

### Adding New Data
1. Add to appropriate file in `data/`
2. Create accessor function if complex
3. Import where needed

---

## File Dependencies

```
main.py
├── config
├── race/race_engine (RaceEngine)
├── ui/renderer (TrackRenderer)
├── ui/timing_screen (TimingScreen)
└── ui/results_screen (ResultsScreen)

race/race_engine.py
├── config
├── race/track (Track)
├── race/car (Car)
└── data/teams (TEAMS_DATA)

race/car.py
├── config

race/track.py
├── config

ui/renderer.py
├── config
├── assets/colors (get_team_color)

ui/timing_screen.py
├── config
├── assets/colors (get_team_color, get_team_short_name)

ui/results_screen.py
├── config
├── assets/colors (get_team_color, get_team_short_name)
```

---

## Tricky Areas

### Car Positioning
- `progress` is 0.0 to 1.0 around track
- When progress >= 1.0, wraps to 0.0 and lap++
- `lateral_offset` used for side-by-side visual separation
- Total progress for sorting = (lap - 1) + progress

### Gap Calculations
- `gap_to_leader`: Total progress difference
- `gap_to_ahead`: Progress difference to car in front
- Displayed as time estimate or lap count (+1L, +2L)

### Race State Machine
- `race_started = False` → "READY" state
- `race_started = True, !finished` → Racing
- `leader.lap > total_laps` → "FINISHED" state

---

## Session Notes

### Current Session
Not yet started.

### Areas to Explore
(Will be populated during briefing work)
