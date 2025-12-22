# F1 Manager - Phase 1: Live Race Visualization

A real-time F1 race simulation with live timing, built with Python and pygame-ce.

## Features

- **20 Cars Racing**: All 10 F1 teams with 2 drivers each
- **F1-Style Circuit**: Circular track with racing line visualization
- **Live Timing Screen**: Real-time position, gaps, tire info, and lap data
- **Smooth Animations**: 60 FPS with smooth car movement
- **Authentic F1 Colors**: Accurate team colors for all 10 teams
- **Race Simulation**: Dynamic race positions based on car performance

## Installation

Make sure you have pygame-ce installed:

```bash
pip install pygame-ce
```

## Running the Game

```bash
cd "D:/game dev/f1_manager"
python main.py
```

## Controls

- **SPACE**: Start the race (or pause/unpause during race)
- **R**: Restart the race
- **ESC**: Quit the game

## Project Structure

```
f1_manager/
├── main.py              # Main game loop
├── config.py            # Game configuration
├── assets/
│   └── colors.py        # F1 team colors
├── race/
│   ├── track.py         # Track layout and waypoints
│   ├── car.py           # Individual car logic
│   └── race_engine.py   # Race simulation engine
├── ui/
│   ├── timing_screen.py # Live timing display
│   └── renderer.py      # Track and car rendering
└── data/
    └── teams.py         # F1 teams and drivers data
```

## Technical Details

- **Screen Resolution**: 1600x900 (1000px track + 600px timing)
- **Frame Rate**: 60 FPS
- **Track Type**: Circular circuit with waypoint-based movement
- **Car Count**: 20 cars (10 teams × 2 drivers)
- **Race Length**: 20 laps (sprint race)

## F1 Teams Included

1. Red Bull Racing (Verstappen, Perez)
2. Ferrari (Leclerc, Sainz)
3. Mercedes (Hamilton, Russell)
4. McLaren (Norris, Piastri)
5. Aston Martin (Alonso, Stroll)
6. Alpine (Gasly, Ocon)
7. Williams (Albon, Sargeant)
8. Alfa Romeo (Bottas, Zhou)
9. Haas (Hulkenberg, Magnussen)
10. AlphaTauri (Tsunoda, Ricciardo)

## What's Next (Future Phases)

- Strategy management (pit stops, tire changes)
- Weather conditions
- Different track layouts
- Team management features
- Season championship mode

---

Built with Python 3 and pygame-ce
