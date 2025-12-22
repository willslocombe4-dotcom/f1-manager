# F1 Manager Development Tools

This directory contains standalone development tools for the F1 Manager game.

## Track Editor

**File:** `track_editor.py`
**Run:** `python tools/track_editor.py`

Visual waypoint editor for creating F1 circuits.

### Features

- **Interactive Waypoint Placement** - Click to add waypoints, drag to reposition
- **Visual Racing Line** - See the track shape as you build it
- **Preview Animation** - Animated car shows how vehicles will move around the track
- **Save/Load System** - Save tracks as JSON files in `tools/tracks/`
- **Code Export** - Generate Python code ready to paste into `race/track.py`
- **Grid Overlay** - 50px grid for precise waypoint alignment
- **1000x900 Canvas** - Matches the game's track view dimensions

### Controls

| Key/Action | Function |
|------------|----------|
| Left Click | Place new waypoint or select existing |
| Drag | Move selected waypoint |
| Right Click | Delete waypoint under cursor |
| Delete/Backspace | Remove selected waypoint |
| Space | Toggle preview car animation |
| S | Save track to JSON file |
| L | Load most recent track |
| C | Clear all waypoints |
| E | Export waypoints to console (Python format) |
| Esc | Exit editor |

### Workflow

1. **Run the editor**: `python tools/track_editor.py`
2. **Click to place waypoints** around your desired circuit shape
3. **Drag waypoints** to fine-tune the racing line
4. **Press Space** to preview how a car will move around the track
5. **Press S** to save your track as a JSON file
6. **Press E** to export Python code to the console
7. **Copy the exported code** into `race/track.py` in the `_generate_waypoints()` method

### Tips

- Use 60-80 waypoints for smooth, realistic tracks
- Waypoints form a closed loop (last connects to first)
- The grid helps align straight sections
- Preview car animation helps identify problem areas
- Save frequently while designing complex circuits
- Right-click for quick waypoint deletion while building

### File Format

Saved tracks use JSON format:

```json
{
  "waypoints": [
    [100, 200],
    [150, 180],
    ...
  ],
  "created": "20251221_143022",
  "num_waypoints": 73
}
```

Exported code uses Python tuple format for direct use in `race/track.py`:

```python
waypoints = [
    (100, 200), (150, 180), (200, 160), (250, 145), (300, 135),
    (350, 130), (400, 128), (450, 130), (500, 138), (550, 150),
    ...
]
```

## Future Tools

See `.claude/context/tool-builder-context.md` for planned development tools:
- Team Editor
- Config Tweaker
- Debug Overlay
- Race Replay System
