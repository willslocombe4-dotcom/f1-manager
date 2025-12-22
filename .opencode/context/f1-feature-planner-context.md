# F1 Feature Planner Context

**Last Updated:** Not yet used

---

## Planning Statistics

| Metric | Value |
|--------|-------|
| Plans Created | 0 |
| Avg Steps per Plan | N/A |
| Successfully Implemented | 0 |
| Required Revision | 0 |

---

## Plan History

| Date | Feature | Steps | Complexity | Outcome |
|------|---------|-------|------------|---------|
| - | - | - | - | No plans yet |

---

## Architecture Knowledge

### Adding New Features - Decision Tree

```
New Feature
├── Is it visual only?
│   └── Add to ui/*.py, maybe config.py
├── Is it simulation logic?
│   └── Add to race/*.py, maybe config.py
├── Is it user input?
│   └── Add to main.py handle_events
├── Is it data-related?
│   └── Add to data/*.py
└── Is it a combination?
    └── Start with data/logic, then UI
```

### Common Feature Types

| Type | Primary Files | Pattern |
|------|---------------|---------|
| New UI element | ui/*.py, config.py | Create in __init__, draw in render |
| New car behavior | race/car.py, config.py | Add state + update logic |
| New race mechanic | race/race_engine.py, race/car.py | Update simulation loop |
| New user control | main.py | Add to handle_events |
| New data display | ui/timing_screen.py | Add column or element |

---

## Integration Points Reference

### main.py F1Manager
```python
# In __init__: Create new components
# In handle_events: Add new controls
# In update: Add new update calls
# In render: Add new render calls
```

### race/race_engine.py RaceEngine
```python
# In __init__: Initialize new simulation state
# In update: Add new per-frame logic
# New accessor methods for UI to read state
```

### race/car.py Car
```python
# In __init__: Add new car properties
# In update: Update properties each frame
# New methods for specific behaviors
```

### ui/renderer.py TrackRenderer
```python
# In __init__: Cache new surfaces
# In render: Call new draw methods
# _draw_*: Add new drawing methods
```

### ui/timing_screen.py TimingScreen
```python
# In _draw_header: Add column headers
# In _draw_timing_rows: Add data display
```

---

## Planning Templates

### Simple UI Addition
```markdown
1. Add config constant if needed
2. Add surface cache in __init__
3. Add draw method
4. Call draw method from render
5. Test
```

### New Car State
```markdown
1. Add property in Car.__init__
2. Add update logic in Car.update()
3. Add accessor method if needed
4. Add display in UI if needed
5. Test
```

### New Game Control
```markdown
1. Add state variable in F1Manager.__init__
2. Add key handler in handle_events
3. Add logic in update if needed
4. Add visual feedback in render
5. Test
```

---

## Complexity Estimation

### Low Complexity (1-5 steps)
- Adding a config value
- Simple visual element
- Basic color/text change

### Medium Complexity (5-15 steps)
- New car state with display
- New UI component
- New user control with feedback

### High Complexity (15+ steps)
- New game mechanic
- Multi-file refactor
- New screen/mode

---

## Current State

### Active Plan
None

### Pending Implementation
None

### Recently Completed
None

---

## Session Notes

### Current Session
Not yet started.

### In Progress
None.
