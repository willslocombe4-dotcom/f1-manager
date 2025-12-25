# F1 Toolmaker Context

**Last Updated:** 2025-12-25

---

## Tools Built

| Date | Tool | Lines | Status |
|------|------|-------|--------|
| Pre-existing | track_editor.py | ~657 | Complete |
| 2025-12-25 | track_decorator.py | ~1773 | Complete (Paint Mode) |
| 2025-12-25 | track_studio.py | ~1650 | Complete (Unified Tool) |

---

## Tool Patterns

### Standard Structure
```python
class ToolName:
    def __init__(self):
        pygame.init()
        # Setup window, fonts, state
    
    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()
    
    def _save(self):
        # Save to JSON
    
    def _export(self):
        # Export to game format
```

### Paint Mode Pattern (track_decorator.py)
```python
class PaintState:
    IDLE = "idle"
    PAINTING = "painting"
    ERASING = "erasing"

# Mouse handling for paint mode
def _handle_mouse_down(self, event):
    if event.button == 1:  # Left click - start painting
        self.paint_state = PaintState.PAINTING
        self.stroke_start_segment = self._get_segment_at_pos(event.pos)
    elif event.button == 3:  # Right click - start erasing
        self.paint_state = PaintState.ERASING

def _handle_mouse_motion(self, event):
    if self.paint_state == PaintState.PAINTING:
        self.stroke_end_segment = self._get_segment_at_pos(event.pos)
        # Preview updates automatically in draw

def _handle_mouse_up(self, event):
    if self.paint_state == PaintState.PAINTING:
        self._commit_stroke()  # Add to decorations
    self.paint_state = PaintState.IDLE
```

### Common Constants
```python
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60
BG_COLOR = (15, 15, 15)
TEXT_COLOR = (255, 255, 255)
```

---

## Learnings

### Pygame Tool Patterns
<!-- UI patterns, event handling, drawing that work well -->
- [2025-12-24] **Pattern:** Cache all fonts in __init__, never in draw loop | **Use:** Every tool
- [2025-12-24] **Pattern:** Use sys.path.insert to import from parent | **Use:** All tools in tools/ folder
- [2025-12-25] **Pattern:** Paint mode with state machine (IDLE/PAINTING/ERASING) | **Use:** Any tool where user drags to create
- [2025-12-25] **Pattern:** Real-time preview by drawing stroke before commit | **Use:** Paint/draw tools
- [2025-12-25] **Pattern:** Snap cursor to nearest valid point with MAX_SNAP_DISTANCE | **Use:** Precision placement tools

### Export Format Issues
<!-- Formats that didn't work, fixes -->

### Template Improvements
<!-- Better ways to structure tools -->
- [2025-12-24] **Improvement:** Add controls help text in _draw_controls() | **Use:** Makes tools self-documenting
- [2025-12-25] **Improvement:** Dual-mode tools (Visual + API) with _HEADLESS_MODE flag | **Use:** Tools that AI agents also use

### User Experience Wins
<!-- Controls/UI that users liked -->
- [2025-12-25] **Win:** Paint mode is more intuitive than click-select-confirm | **Use:** Decoration/drawing tools
- [2025-12-25] **Win:** Color-coded boundaries (blue=left, red=right) with thickness change when selected | **Use:** Any tool with multiple selection targets
- [2025-12-25] **Win:** Tool/mode indicator prominently displayed in panel header | **Use:** Multi-mode tools
- [2025-12-25] **Win:** Unified tools (generate+draw+decorate) reduce context switching | **Use:** Complex creation workflows
- [2025-12-25] **Win:** Template preview with dashed lines before applying | **Use:** Template-based generation
- [2025-12-25] **Win:** One-liner API methods like generate_decorated_track() for AI agents | **Use:** AI-friendly tools

---

## Track Studio Notes

### Merging Strategy
When merging multiple tools into one:
1. Keep all API methods from both tools
2. Add mode switching (1/2/3 keys)
3. Mode-specific controls only active in that mode
4. Common actions (save/load/undo) work in all modes
5. Template system from generator + paint system from decorator

### Template System
Templates are normalized (0-1) control points that get:
1. Scaled to canvas
2. Optionally varied (random ±8%)
3. Optionally mirrored/rotated
4. Smoothed with Catmull-Rom spline
5. Scaled to fit with margins

### API Design for AI
- `list_templates()` - discovery
- `generate_from_template()` - basic generation
- `generate_decorated_track()` - one-liner for complete track
- `auto_decorate()` - smart decoration based on analysis
- All methods return useful data or modify state predictably
