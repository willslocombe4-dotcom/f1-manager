# Bug Fixer Context

Last updated: 2024-12-21
STATUS: IDLE

## Fixed Bugs

### Track was oval instead of F1 circuit
- **Date:** 2024-12-21
- **Problem:** Track rendered as simple oval
- **Cause:** Renderer was drawing circles, not using waypoints
- **Fix:** Rewrote renderer.py to use track.waypoints for polygon drawing
- **File:** ui/renderer.py

### Cars moving too fast
- **Date:** 2024-12-21
- **Problem:** Cars completed laps too quickly
- **Cause:** BASE_SPEED was 2.0, too high
- **Fix:** Reduced BASE_SPEED to 0.25 in config.py
- **File:** config.py

### IndentationError in main.py
- **Date:** 2024-12-21
- **Problem:** Syntax error on line 1
- **Cause:** Hidden character at start of file
- **Fix:** Deleted and recreated main.py cleanly
- **File:** main.py

## Known Fragile Areas

### Track Waypoints
- Waypoints must form closed loop
- Last point connects to first
- Keep within 1000x900 track view area

### Progress System
- Must stay between 0.0 and 1.0
- Resets to 0 on lap completion
- `total_progress = lap + progress`

### Coordinate System
- Pygame Y-axis is inverted (0 at top)
- Track view is 0-1000 X
- Timing panel is 1000-1600 X

## Error Patterns

### "AttributeError: 'Car' object has no attribute 'X'"
- Check Car class in race/car.py
- Make sure property is initialized in __init__

### "IndexError: list index out of range"
- Usually waypoint access issue
- Check track.waypoints bounds

### Visual elements not appearing
- Check draw order (later draws on top)
- Check coordinates are in visible area
- Check color alpha values

## File-Specific Notes

### config.py
- All caps for constants
- Colors are RGB tuples

### race/car.py
- progress: 0.0-1.0 around track
- lap: integer lap count
- speed: base + variance - degradation

### race/track.py
- waypoints: list of (x, y) tuples
- get_position(progress): returns screen coords

### ui/renderer.py
- Draws in order: grass, track, kerbs, cars
- Uses track.waypoints for shapes

## Testing Commands

```bash
# Run the game
python main.py

# Controls
# SPACE - Start/Pause/New race
# R - Restart
# ESC - Quit
```
