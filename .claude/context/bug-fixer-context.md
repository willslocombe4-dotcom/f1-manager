# Bug Fixer Context

Last updated: 2025-12-22
STATUS: IDLE

## Fixed Bugs

### Grass appearing on track surface (polygon fill issue)
- **Date:** 2025-12-22
- **Problem:** Grass (green) was appearing on top of the black track surface in several places, particularly at sharp corners
- **Root Cause:** The track surface was drawn as a SINGLE complex polygon by concatenating `outer_points + inner_points[::-1]`. At sharp corners (specifically indices 51-54), the inner boundary had self-intersections where boundary segments crossed over each other. Pygame's polygon fill algorithm uses the even-odd rule, which leaves gaps unfilled when the polygon self-intersects.
- **Fix:** Changed from drawing a single complex polygon to drawing individual quadrilateral segments. For each segment between waypoints, a quad is drawn using `[outer[i], outer[i+1], inner[i+1], inner[i]]`. This avoids self-intersection issues entirely and guarantees complete track coverage.
- **File:** ui/renderer.py:80-98 (LAYER 3: Track surface)
- **Related:** Previous gravel fix was not the cause; this was a separate issue with the track polygon itself

### Gravel traps overlapping track surface
- **Date:** 2025-12-22
- **Problem:** Gravel/sand runoff areas were appearing ON TOP of the track surface
- **Cause:** `_draw_gravel_trap()` created a polygon using only the extended gravel outer points. This formed an arc shape that, when filled as a polygon, could bleed across the track surface because it wasn't bounded by the track edge.
- **Fix:** Changed gravel trap to be a proper band/strip shape. Now collects both outer points (gravel outer edge) and inner points (track outer edge), then creates a closed polygon: `gravel_outer_points + gravel_inner_points[::-1]`. This ensures gravel only fills the area BETWEEN the track edge and the gravel outer boundary.
- **File:** ui/renderer.py:108-145

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

### Track Boundary Polygon Rendering (CRITICAL)
- NEVER draw track as a single complex polygon using `outer_points + inner_points[::-1]`
- Sharp corners cause boundary self-intersections which create gaps in polygon fill
- ALWAYS draw track as individual segment quads: `[outer[i], outer[i+1], inner[i+1], inner[i]]`
- Same issue can affect gravel traps at sharp corners

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
