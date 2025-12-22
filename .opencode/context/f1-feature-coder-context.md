# F1 Feature Coder Context

**Last Updated:** Not yet used

---

## Implementation Statistics

| Metric | Value |
|--------|-------|
| Features Implemented | 0 |
| Lines Added | 0 |
| Lines Modified | 0 |
| Files Changed | 0 |

---

## Implementation History

| Date | Feature | Files | Lines | Notes |
|------|---------|-------|-------|-------|
| - | - | - | - | No implementations yet |

---

## Code Patterns Library

### UI Component Template
```python
class NewComponent:
    def __init__(self, surface):
        self.surface = surface
        # Cache surfaces
        self.component_surface = pygame.Surface((width, height))
        # Cache fonts
        self.font = pygame.font.Font(None, 24)
    
    def render(self, race_engine):
        # Clear or prepare
        self.component_surface.fill(color)
        # Draw elements
        self._draw_elements(race_engine)
        # Blit to main surface
        self.surface.blit(self.component_surface, (x, y))
    
    def _draw_elements(self, race_engine):
        # Implementation
        pass
```

### Car State Extension
```python
# In Car.__init__, add:
self.new_property = initial_value

# In Car.update, update:
self.new_property = self._calculate_new_property()

# Add calculation method:
def _calculate_new_property(self):
    return calculated_value
```

### Config Addition
```python
# In config.py
# Section: [Section Name]
NEW_CONSTANT = value
NEW_COLOR = (r, g, b)
```

### Event Handling
```python
# In F1Manager.handle_events
elif event.key == pygame.K_x:
    if self.some_condition:
        self.do_action()
```

---

## Common Integration Points

### Adding to Timing Screen
1. Add data calculation in `Car` or `RaceEngine`
2. Add column in `TimingScreen._draw_header()`
3. Add data display in `TimingScreen._draw_timing_rows()`

### Adding to Track View
1. Add render method in `TrackRenderer`
2. Call from `TrackRenderer.render()`
3. Use race_engine for data access

### Adding New Game State
1. Add state variable in `F1Manager.__init__()`
2. Add state transitions in `handle_events()`
3. Add state-specific rendering in `render()`

---

## File Modification Guide

### main.py
- Add imports at top
- Add __init__ code for new components
- Add handle_events code for new controls
- Add render code for new displays

### config.py
- Add constants in appropriate section
- Use UPPER_SNAKE_CASE
- Add comments for clarity

### race/race_engine.py
- Add car management in update()
- Add new accessor methods as needed

### race/car.py
- Add state in __init__
- Update in update()
- Add calculation methods

### ui/*.py
- Cache surfaces in __init__
- Use render(race_engine) pattern
- Break into _draw_*() methods

---

## Testing Checklist

### After Any Implementation
- [ ] `python main.py` runs
- [ ] No pygame errors in console
- [ ] Game starts and shows correctly
- [ ] New feature visible/functional
- [ ] Existing features still work
- [ ] Race completes normally
- [ ] Results show correctly

---

## Current State

### Active Implementation
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
