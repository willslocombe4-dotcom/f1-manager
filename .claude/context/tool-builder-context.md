# Tool Builder Context

Last updated: 2025-12-21

## Built Tools

### Track Editor (tools/track_editor.py)
Visual waypoint editor for creating F1 circuits with background image tracing support.

**Features:**
- Click to place waypoints, drag to move them
- Preview racing line and car animation
- Load background images (PNG, JPG) to trace real tracks
- Toggle image visibility and adjust opacity
- Save/load tracks with image references
- Export waypoints as Python code to file (tools/tracks/track_TIMESTAMP_export.py)

**Controls:**
- Click: Place waypoint
- Drag: Move waypoint
- Right Click/Delete: Remove waypoint
- Space: Toggle preview car
- S: Save track
- L: Load track
- C: Clear all
- E: Export code
- I: Load background image
- V: Toggle image visibility
- +/-: Adjust image opacity
- Esc: Exit

**Track JSON Format:**
```json
{
  "waypoints": [[x, y], ...],
  "created": "timestamp",
  "num_waypoints": 60,
  "background_image": "path/to/image.png",
  "background_opacity": 128
}
```

## Tools In Progress

*None*

## Tool Ideas Backlog

### High Priority
*None*

### Medium Priority
- **Team Editor** - Edit teams and drivers
  - Change team names/colors
  - Add/remove drivers
  - Preview timing screen look

- **Config Tweaker** - Adjust game settings
  - Speed sliders
  - Visual previews
  - Export config values

### Low Priority
- **Debug Overlay** - Development helper
  - Show car stats in real-time
  - Visualize waypoints and progress
  - FPS and performance data

- **Race Replay System** - Record and playback
  - Save race data to file
  - Playback with pause/speed controls
  - Compare different races

## Technical Patterns

### Standalone Tool Setup
```python
import sys
sys.path.insert(0, '..')  # Import from parent
import config
from race.track import Track
```

### Pygame Tool Window
```python
pygame.init()
screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption("Tool Name")
```

### Export Waypoints Format
```python
# Output format for track.py
waypoints = [
    (100, 200),
    (150, 180),
    # ... more points
]
```

### File Dialog Pattern
```python
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename(
    title="Select File",
    filetypes=[("Image files", "*.png *.jpg")]
)
root.destroy()
```

### Color Picker Pattern
```python
# RGB sliders or click-to-pick from palette
```

## File Locations

- Tools go in: `tools/`
- Each tool is standalone .py file
- Tools can import from parent with sys.path trick

## Game Data Formats

### Track Waypoints
```python
# List of (x, y) tuples, 0-1000 x, 0-900 y
# Forms closed loop (last connects to first)
# ~60-80 points for smooth track
```

### Track JSON Files
```python
{
    "waypoints": [(x, y), ...],
    "created": "timestamp",
    "num_waypoints": int,
    "background_image": "optional/path/to/image.png",
    "background_opacity": 0-255
}
```

### Team Data
```python
{
    "name": "Team Name",
    "color": (R, G, B),
    "drivers": [
        {"number": 1, "name": "Full Name", "short": "ABC"}
    ]
}
```

### Config Values
```python
BASE_SPEED = 0.25
SPEED_VARIANCE = 0.3
# etc
```

## Notes

### Background Image Integration
- Use tkinter.filedialog for file picking (works well with pygame)
- Remember to call `root.withdraw()` and `root.destroy()` to hide tkinter window
- Scale images to track view dimensions (1000x900) for consistent tracing
- Store image path (not pixel data) in JSON for persistence
- Use pygame surface alpha for opacity control: `image.set_alpha(0-255)`
- Draw order matters: grid -> background image -> track line -> waypoints -> preview car

### Pygame + Tkinter Integration
- Tkinter dialogs work fine alongside pygame windows
- Always create and destroy tk root for each dialog use
- Don't keep tkinter event loop running with pygame
### Waypoint Export Files
- Export creates .py files with ready-to-use Python code
- Saved to tools/tracks/ with timestamp: track_YYYYMMDD_HHMMSS_export.py
- Contains commented header with generation time and waypoint count
- Waypoints formatted in rows of 5 tuples for readability
- Can be directly copied into race/track.py
