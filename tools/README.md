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

---

## Track Generator (AI-Friendly)

**File:** `track_generator.py`
**Run:** `python tools/track_generator.py --help`

**This is the primary tool for AI agents to create tracks.** No image processing, no crashes - just pure math and real F1 track data.

### Features

- **Real F1 Tracks** - Pre-converted waypoints from actual circuits (Bahrain, Silverstone, Monaco, Monza, Spa)
- **Random Generation** - Procedural tracks using Catmull-Rom splines with chicanes and hairpins
- **Anti-Oval Algorithm** - Automatically rejects boring oval shapes
- **Python API** - Import directly into AI agent code
- **CLI Interface** - Command-line for quick generation

### Usage (AI Agents)

```python
from tools.track_generator import TrackGenerator

gen = TrackGenerator()

# Option 1: Use a real F1 circuit
waypoints = gen.get_real_track("bahrain")
gen.save("Bahrain GP", waypoints)

# Option 2: Generate random track
waypoints = gen.generate_random(complexity="medium", seed=42)
gen.save("Custom Circuit", waypoints)

# Option 3: List available tracks
print(gen.list_real_tracks())
```

### CLI Usage

```bash
# List available real tracks
python tools/track_generator.py --list

# Use a real F1 track
python tools/track_generator.py --real bahrain

# Generate random track
python tools/track_generator.py --random --name "Custom Circuit"

# Complex random track with seed
python tools/track_generator.py --random --complexity complex --seed 42

# Export as Python code too
python tools/track_generator.py --real silverstone --export-python
```

### Available Real Tracks

| ID | Name | Location |
|----|------|----------|
| `bahrain` | Bahrain International Circuit | Sakhir, Bahrain |
| `silverstone` | Silverstone Circuit | Silverstone, UK |
| `monaco` | Circuit de Monaco | Monte Carlo, Monaco |
| `monza` | Autodromo Nazionale Monza | Monza, Italy |
| `spa` | Circuit de Spa-Francorchamps | Spa, Belgium |

### Random Track Complexity

| Level | Control Points | Chicanes | Hairpins |
|-------|----------------|----------|----------|
| `simple` | 8 | 1 | 1 |
| `medium` | 12 | 2 | 2 |
| `complex` | 16 | 3 | 3 |

### Why This Tool?

The old `track_tracer.py` used image processing (OpenCV) which was unreliable - it crashed on certain image formats and produced inconsistent results.

This tool uses:
1. **Pre-converted real track data** from the TUMFTM racetrack-database
2. **Mathematical curve generation** using Catmull-Rom splines
3. **Anti-oval detection** to ensure interesting track shapes

No images. No crashes. Just reliable track generation.

---

## Track Decorator (Draw + Paint Mode)

**File:** `track_decorator.py`
**Run:** `python tools/track_decorator.py [track_file.json]`

**Create tracks from scratch and paint decorations** - two modes in one tool. Draw mode for placing waypoints, Decorate mode for painting kerbs and gravel.

### Features

- **Draw Mode** - Click to place waypoints, drag to move them, right-click to delete
- **Decorate Mode** - Click and drag to paint decorations directly on boundaries
- **Real-Time Preview** - See decorations as you drag, before releasing
- **Visual Boundaries** - Left boundary (blue) and right boundary (red) always visible
- **Start Line** - Set start/finish line at any segment
- **API Mode** - Import and use programmatically (no pygame window needed)
- **Undo Support** - Undo works for both waypoints and decorations

### Visual Mode Controls

| Input | Action |
|-------|--------|
| **D** | Switch to Draw mode (place/move waypoints) |
| **P** | Switch to Decorate mode (paint kerbs/gravel) |
| **K** | Select Kerb tool (decorate mode) |
| **G** | Select Gravel tool (decorate mode) |
| **E** | Select Eraser tool (decorate mode) |
| **L** | Select Left boundary (blue) |
| **R** | Select Right boundary (red) |
| **T** | Set start line at hover segment |
| **Left-click** | Place waypoint (draw) / Paint (decorate) |
| **Right-click** | Delete waypoint (draw) / Erase (decorate) |
| **Z** | Undo last action |
| **C** | Clear waypoints (draw) / Clear decorations (decorate) |
| **S** | Save track |
| **O** | Open/load track file |
| **N** | Toggle segment numbers |
| **A** | Auto-suggest decorations |
| **+/-** or **Scroll** | Zoom |
| **Arrow keys** | Pan |
| **Esc** | Exit |

### Workflow (Creating a Track from Scratch)

1. **Run the tool**: `python tools/track_decorator.py`
2. **Press D** for Draw mode
3. **Click to place waypoints** forming your circuit shape
4. **Drag waypoints** to fine-tune positions
5. **Press P** for Decorate mode
6. **Select tool** (K for kerb, G for gravel)
7. **Select boundary** (L for left, R for right)
8. **Paint decorations** by clicking and dragging
9. **Press T** over a segment to set start line
10. **Press S** to save

### API Usage (for AI Agents)

```python
from tools.track_decorator import TrackDecorator
import math

# Create new track from scratch
decorator = TrackDecorator()
decorator.create_new_track("My Circuit")

# Add waypoints (e.g., an oval)
for i in range(20):
    angle = (i / 20) * 2 * math.pi
    x = 500 + 300 * math.cos(angle)
    y = 450 + 200 * math.sin(angle)
    decorator.add_waypoint(x, y)

# Or load existing track
# decorator = TrackDecorator("existing_track.json")

# Analyze segments to understand the track
analysis = decorator.analyze_segments()
# Returns: {15: {'angle_deg': 42.5, 'turn_direction': 'left', ...}, ...}

# Place decorations explicitly
decorator.add_kerb(boundary="right", start=15, end=18)
decorator.add_gravel(boundary="left", start=13, end=20)
decorator.set_start_line(segment=0)
decorator.set_racing_line(enabled=True)

# Modify waypoints
decorator.move_waypoint(5, x=600, y=500)
decorator.remove_waypoint(10)

# Validate before saving
errors = decorator.validate()  # Returns [] if valid

# Save
decorator.save("my_track.json")
```

### Full API Reference

| Method | Description |
|--------|-------------|
| `create_new_track(name)` | Start a new empty track |
| `add_waypoint(x, y, index=None)` | Add waypoint (returns index) |
| `remove_waypoint(index)` | Remove waypoint by index |
| `move_waypoint(index, x, y)` | Move waypoint to new position |
| `clear_waypoints()` | Remove all waypoints |
| `get_waypoints()` | Get list of (x, y) tuples |
| `add_kerb(boundary, start, end)` | Add kerb decoration |
| `add_gravel(boundary, start, end)` | Add gravel trap |
| `set_start_line(segment)` | Set start/finish line position |
| `remove_start_line()` | Remove start line |
| `set_racing_line(enabled)` | Enable/disable racing line |
| `clear_decorations()` | Remove all decorations |
| `analyze_segments()` | Get turn info for each segment |
| `suggest_decorations()` | Get AI-suggested decorations |
| `validate()` | Check for errors |
| `undo()` | Undo last change |
| `save(filepath)` | Save to JSON file |

### JSON Format

Tracks with decorations use this format:

```json
{
  "name": "Decorated Circuit",
  "waypoints": [[100, 200], [150, 180], ...],
  "decorations": {
    "kerbs": [
      {"boundary": "left", "start": 15, "end": 18},
      {"boundary": "right", "start": 42, "end": 46}
    ],
    "gravel": [
      {"boundary": "right", "start": 13, "end": 20},
      {"boundary": "left", "start": 40, "end": 48}
    ],
    "start_line": {"segment": 0},
    "racing_line": true
  },
  "created": "20251225_120000",
  "num_waypoints": 65
}
```

### Backward Compatibility

- Tracks without decorations still work - no auto-rendering in game
- The `decorations` field is optional in JSON files
- Existing tracks don't need to be modified

---

## Track Studio (Unified Tool) ⭐ RECOMMENDED

**File:** `track_studio.py`
**Run:** `python tools/track_studio.py`

**Visual track creation tool.** Create F1 circuits by generating from templates or drawing from scratch, then paint decorations manually.

### Features

- **Generate Mode** - Create tracks from templates (Monaco, Silverstone, Monza, Spa, Suzuka, Bahrain)
- **Draw Mode** - Place waypoints manually with click and drag
- **Decorate Mode** - Paint kerbs, gravel, and grass on track boundaries

### Controls

| Key | Action |
|-----|--------|
| **1** | Switch to Generate mode |
| **2** | Switch to Draw mode |
| **3** | Switch to Decorate mode |
| **B** | Browse templates (Generate mode) |
| **Enter** | Apply template (Generate mode) |
| **V** | Generate variation (Generate mode) |
| **K** | Kerb tool (Decorate mode) |
| **G** | Gravel tool (Decorate mode) |
| **F** | Grass tool (Decorate mode) |
| **E** | Eraser tool (Decorate mode) |
| **L** | Left boundary |
| **R** | Right boundary |
| **T** | Set start line |
| **S** | Save |
| **O** | Open track |
| **Z** | Undo |
| **C** | Clear |
| **N** | Toggle segment numbers |
| **Esc** | Exit |

### Workflow

1. **Run the tool**: `python tools/track_studio.py`
2. **Generate or Draw**: Use mode 1 to pick a template, or mode 2 to draw from scratch
3. **Decorate**: Switch to mode 3 and paint kerbs/gravel/grass manually
4. **Save**: Press S to save your track

### Available Templates

| ID | Name | Description |
|----|------|-------------|
| `monaco` | Monaco | Tight and twisty street circuit |
| `silverstone` | Silverstone | Fast and flowing British circuit |
| `monza` | Monza | Long straights with chicanes |
| `spa` | Spa-Francorchamps | Flowing with elevation changes |
| `suzuka` | Suzuka | Figure-8 inspired layout |
| `bahrain` | Bahrain | Classic F1 layout with technical sections |

---

## AI Template Generator

**File:** `generate_templates.py`
**Run:** `python tools/generate_templates.py [count]`

**Generates random track templates** using mathematical curves. Creates variety of track shapes that can be loaded and decorated in Track Studio.

### Usage

```bash
# Generate 10 random templates (default)
python tools/generate_templates.py

# Generate 20 templates
python tools/generate_templates.py 20
```

### Generation Methods

The generator randomly picks from these algorithms:

| Method | Description |
|--------|-------------|
| `oval` | Ellipse with random wobble |
| `bezier` | Catmull-Rom spline through random control points |
| `polygon` | Random polygon with rounded corners |
| `figure8` | Lemniscate of Bernoulli (figure-8 shape) |
| `random_walk` | Random walk that loops back |

### Output

Templates are saved to `tools/templates/` as JSON files:

```json
{
  "name": "Thunder Circuit",
  "waypoints": [[x, y], ...],
  "method": "bezier",
  "generated": "20251225_120000",
  "num_waypoints": 65,
  "decorations": {
    "kerbs": [],
    "gravel": [],
    "grass": [],
    "start_line": null,
    "racing_line": false
  }
}
```

### Workflow

1. **Generate templates**: `python tools/generate_templates.py 20`
2. **Open Track Studio**: `python tools/track_studio.py`
3. **Press O** to open a template from `tools/templates/`
4. **Decorate** with kerbs, gravel, and grass
5. **Save** your decorated track

---

## Future Tools

See `.claude/context/tool-builder-context.md` for planned development tools:
- Team Editor
- Config Tweaker
- Debug Overlay
- Race Replay System
