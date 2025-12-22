# F1 Tool Builder Context

**Last Updated:** Not yet used

---

## Tool Statistics

| Metric | Value |
|--------|-------|
| Tools Built | 1 (pre-existing) |
| Lines of Code | ~650 (track_editor) |

---

## Existing Tools

### Track Editor
**File:** `tools/track_editor.py`
**Lines:** ~650
**Status:** Complete and working

**Features:**
- Visual waypoint placement
- Drag to reposition
- Preview car animation
- Background image tracing
- Save/Load JSON
- Export Python code

**Controls:**
| Key | Action |
|-----|--------|
| Click | Place/select waypoint |
| Drag | Move waypoint |
| Right click | Delete waypoint |
| Space | Toggle preview |
| S | Save track |
| L | Load track |
| C | Clear all |
| E | Export code |
| I | Load background |
| V | Toggle image |
| +/- | Image opacity |
| Esc | Exit |

**Export Location:** `tools/tracks/`

---

## Tool Ideas Backlog

| Tool | Purpose | Priority | Complexity |
|------|---------|----------|------------|
| Team Editor | Edit teams/drivers/colors | Medium | Medium |
| Config Tweaker | Adjust game settings | Low | Low |
| Debug Overlay | Runtime car data | Low | Medium |
| Race Replay | Record/playback | Low | High |

---

## Common Patterns

### Tool Initialization
```python
import pygame
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Title")
clock = pygame.time.Clock()
```

### Main Loop
```python
while running:
    for event in pygame.event.get():
        # Handle events
    update()
    draw()
    clock.tick(FPS)
pygame.quit()
```

### Save to JSON
```python
import json
data = {"key": value}
with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)
```

### Export Python Code
```python
lines = ["# Header", f"data = {data}"]
with open(filepath, 'w') as f:
    f.write('\n'.join(lines))
```

---

## Integration Notes

### Track Editor → Track Importer
1. User creates track in editor
2. Editor exports to `tools/tracks/*_export.py`
3. @f1-track-importer reads export
4. Importer updates `race/track.py`

### Future Tool Integrations
- Team Editor → `data/teams.py`
- Config Tweaker → `config.py`

---

## Session Notes

### Current Session
Not yet started.

### Ideas/Notes
(To be populated during tool building)
