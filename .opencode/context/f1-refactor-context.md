# F1 Refactor Context

**Last Updated:** Not yet used

---

## Refactor Statistics

| Metric | Value |
|--------|-------|
| Plans Created | 0 |
| Refactors Completed | 0 |
| Lines Changed | 0 |

---

## Refactor History

| Date | Target | Status | Steps | Notes |
|------|--------|--------|-------|-------|
| - | - | - | - | No refactors yet |

---

## Architecture Analysis

### Current Structure Assessment

#### Strengths
- Clean separation of concerns (race/ vs ui/ vs data/)
- Config centralized in config.py
- RaceEngine owns all simulation state
- UI components are read-only viewers

#### Areas for Improvement
| Area | Current | Ideal | Priority |
|------|---------|-------|----------|
| Event handling | In main.py | Could be separate EventManager | Low |
| State management | RaceEngine | Could add GameState class | Medium |
| Audio | None | Could add AudioManager | Low |

#### Technical Debt
| Item | Location | Impact | Effort to Fix |
|------|----------|--------|---------------|
| - | - | None tracked | - |

---

## Dependency Map

### Core Flow
```
User Input → F1Manager.handle_events()
              ↓
          RaceEngine.update()
              ↓
          Car.update() × 20
              ↓
          UI.render()
```

### Module Coupling
```
High Coupling (Many Dependencies):
- main.py (imports everything)
- race_engine.py (creates many objects)

Low Coupling (Few Dependencies):
- config.py (no imports)
- data/teams.py (no imports)
- assets/colors.py (no imports)
```

---

## Potential Refactoring Targets

### High Value, Low Risk
| Target | Benefit | Risk |
|--------|---------|------|
| Extract timing format logic | Reusable, testable | Low - isolated |
| Extract config sections | Better organization | Low - just splitting |

### High Value, Medium Risk
| Target | Benefit | Risk |
|--------|---------|------|
| Extract GameState | Cleaner main.py | Medium - touches many files |
| Add AudioManager | Enable sound effects | Medium - new subsystem |

### Low Priority
| Target | Reason to Defer |
|--------|-----------------|
| Major architecture change | Working fine for now |
| Performance optimization | Not currently needed |

---

## Naming Conventions

### Current Patterns
```python
# Classes: PascalCase
class RaceEngine:
class TrackRenderer:

# Functions/Methods: snake_case
def get_cars_by_position():
def _draw_track():  # Private with underscore

# Constants: UPPER_SNAKE_CASE
SCREEN_WIDTH = 1600
BASE_SPEED = 0.25

# Variables: snake_case
race_time = 0.0
current_lap = 1
```

### File Organization
```
# Modules: snake_case
race_engine.py
timing_screen.py

# Directories: snake_case
race/
ui/
data/
```

---

## Code Style Notes

### Pygame Patterns
```python
# Surface initialization in __init__
def __init__(self, surface):
    self.surface = surface
    self.cached_surface = pygame.Surface((w, h))

# Render reads from race_engine, doesn't modify
def render(self, race_engine):
    cars = race_engine.get_cars_by_position()
    # draw stuff, never modify race_engine
```

### Error Handling
```python
# Currently minimal error handling
# Consider adding for:
# - File I/O (track loading)
# - Invalid config values
# - Edge cases in calculations
```

---

## Session Notes

### Current Session
Not yet started.

### Ideas to Consider
(Will be populated during refactoring work)
