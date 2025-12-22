# Feature Planner Context

Last updated: 2025-12-21
STATUS: IDLE

## Current Architecture

### Core Files
- `main.py` - Game loop, F1Manager class
- `config.py` - Constants (BASE_SPEED=0.25, screen sizes, colors)
- `race/race_engine.py` - RaceEngine owns cars and track
- `race/car.py` - Car with progress (0-1), speed, tires
- `race/track.py` - Track with waypoints list
- `ui/renderer.py` - TrackRenderer draws track polygon + cars
- `ui/timing_screen.py` - TimingScreen shows live timing
- `ui/results_screen.py` - ResultsScreen shows final standings
- `data/teams.py` - TEAMS_DATA with colors and drivers

### Key Patterns
- Progress-based movement: `progress += speed / track_length`
- Cars sorted by `get_total_progress()` for race order
- Track position via `get_position(progress)` converts 0-1 to screen coords
- 60 FPS game loop in main.py

## Features Being Planned

*None currently*

## Features Ready for Coding

*None currently*

## Completed Plans

- Enhanced Track Visuals (2025-12-21)
  - Planning confidence: HIGH (92%)
  - Implementation confidence: HIGH (95%)
  - All visual elements successfully implemented
  - Static surface caching working as planned
  - No issues during implementation

- Phase 1: Basic Race Visualization (implemented)
  - Track with waypoints
  - Car movement
  - Timing screen
  - Results screen

## Technical Decisions

- Using pygame-ce for Python 3.14 compatibility
- Waypoint-based tracks (list of x,y tuples)
- Progress 0-1 for lap position
- Split-screen layout: 1000px track + 600px timing

## Architecture Notes

### Adding New Screens
- Create new file in `ui/`
- Add to main.py imports
- Integrate in render() method

### Adding Car Properties
- Add to Car class in `race/car.py`
- Update timing_screen.py if displaying
- May need config.py constants

### Adding Game Modes
- Consider state machine in F1Manager class
- Current states: pre-race, racing, paused, finished

## Pending Questions

*None*
