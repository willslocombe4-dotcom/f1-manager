# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the game
python main.py

# Install dependencies
pip install pygame-ce
```

## Architecture

This is a Pygame-based F1 race simulation game with a split-screen layout: track view (1000px) on the left, live timing (600px) on the right.

### Core Components

**RaceEngine** (`race/race_engine.py`) - Central simulation controller
- Owns all Car instances and the Track
- Runs the update loop: moves cars, calculates positions, computes gaps
- Cars sorted by `get_total_progress()` (lap count + track progress) to determine race order

**Car** (`race/car.py`) - Individual car state and movement
- `progress` (0.0-1.0): position around track, resets on lap completion
- `speed`: base speed with random variance and tire degradation
- Movement: `progress += speed / track_length` per frame

**Track** (`race/track.py`) - Circuit defined by waypoint coordinates
- `waypoints`: list of (x, y) tuples forming the racing line
- `get_position(progress)`: converts 0-1 progress to screen coordinates
- `get_offset_position()`: handles side-by-side car positioning

### UI Components

**TrackRenderer** (`ui/renderer.py`) - Draws track polygon from waypoints, renders cars as colored circles with position numbers

**TimingScreen** (`ui/timing_screen.py`) - F1 broadcast-style timing tower showing position, driver, team, gap, tire compound

**ResultsScreen** (`ui/results_screen.py`) - End-of-race results overlay with final standings

### Data Flow

1. `main.py` creates F1Manager which initializes RaceEngine
2. Each frame: `race_engine.update()` moves all cars and recalculates positions
3. Renderers read car positions from RaceEngine and draw to screen
4. Race ends when leader's lap exceeds `total_laps`

### Configuration

All game constants in `config.py`:
- `BASE_SPEED`: car movement rate (0.25 = realistic pace)
- `SPEED_VARIANCE`: randomness between cars (0.3)
- Screen dimensions, colors, tire compounds

### Adding New Tracks

Modify `Track._generate_waypoints()` in `race/track.py`. Add (x, y) tuples that form a closed loop within the 1000x900 track view area.

### Adding New Teams/Drivers

Edit `TEAMS_DATA` in `data/teams.py`. Each team needs: name, color (RGB), list of driver dicts with number/name/short code.
