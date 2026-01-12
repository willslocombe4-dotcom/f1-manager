"""
F1 Track Editor - Visual waypoint editor for creating F1 circuits

Controls:
- Left Click: Place new waypoint or select existing waypoint
- Drag: Move selected waypoint
- Right Click / Delete: Remove selected waypoint
- Space: Toggle preview car animation
- S: Save track to file
- L: Load track from file
- C: Clear all waypoints
- E: Export waypoints to file
- I: Load background image
- V: Toggle image visibility
- +/-: Adjust image opacity
- Esc: Exit editor

The racing line is drawn as you build the track.
Preview car shows how vehicles will move around your circuit.
You can load a background image (PNG, JPG) to trace over real F1 tracks.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import math
import json
from datetime import datetime
from tkinter import filedialog
import tkinter as tk

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60

# Track view area (matching game's track view)
TRACK_VIEW_WIDTH = 1000
TRACK_VIEW_HEIGHT = 900

# UI Panel
PANEL_WIDTH = 200
PANEL_X = TRACK_VIEW_WIDTH

# Colors
BG_COLOR = (15, 15, 15)
TRACK_BG_COLOR = (20, 20, 20)
PANEL_BG_COLOR = (25, 25, 25)
TRACK_LINE_COLOR = (80, 120, 255)
WAYPOINT_COLOR = (100, 255, 100)
WAYPOINT_SELECTED_COLOR = (255, 200, 50)
WAYPOINT_HOVER_COLOR = (255, 255, 100)
PREVIEW_CAR_COLOR = (255, 50, 50)
GRID_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
TEXT_DIM_COLOR = (150, 150, 150)

# Sizes
WAYPOINT_RADIUS = 8
WAYPOINT_HOVER_RADIUS = 12
PREVIEW_CAR_SIZE = 12
TRACK_LINE_WIDTH = 3
GRID_SIZE = 50

class TrackEditor:
    """Visual editor for creating F1 track waypoints"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("F1 Track Editor")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)

        # Track data
        self.waypoints = []
        self.selected_waypoint = None
        self.hover_waypoint = None
        self.dragging = False

        # Preview car
        self.preview_enabled = False
        self.preview_progress = 0.0
        self.preview_speed = 0.003  # Progress per frame

        # UI state
        self.message = "Click to place waypoints"
        self.message_timer = 0

        # File handling
        self.current_file = None

        # Background image
        self.bg_image = None
        self.bg_image_path = None
        self.bg_image_visible = True
        self.bg_image_opacity = 128  # 0-255, default 50%

        # Racing line cache
        self.racing_line_surface = None
        self.racing_line_dirty = True

    def run(self):
        """Main editor loop"""
        running = True

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self.handle_keypress(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event.button, event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(event.button)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)

            # Update
            self.update()

            # Draw
            self.draw()

            # Cap framerate
            self.clock.tick(FPS)

        pygame.quit()

    def handle_keypress(self, key):
        """Handle keyboard input"""
        if key == pygame.K_ESCAPE:
            return False  # Exit
        elif key == pygame.K_SPACE:
            self.preview_enabled = not self.preview_enabled
            self.show_message(f"Preview: {'ON' if self.preview_enabled else 'OFF'}")
        elif key == pygame.K_s:
            self.save_track()
        elif key == pygame.K_l:
            self.load_track()
        elif key == pygame.K_c:
            self.clear_waypoints()
        elif key == pygame.K_e:
            self.export_waypoints()
        elif key == pygame.K_i:
            self.load_background_image()
        elif key == pygame.K_v:
            self.toggle_image_visibility()
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.adjust_image_opacity(10)
        elif key == pygame.K_MINUS:
            self.adjust_image_opacity(-10)
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            self.delete_selected_waypoint()

        return True

    def handle_mouse_down(self, button, pos):
        """Handle mouse button press"""
        x, y = pos

        # Only interact with track view area
        if x >= TRACK_VIEW_WIDTH:
            return

        if button == 1:  # Left click
            # Check if clicking existing waypoint
            clicked_idx = self.get_waypoint_at_pos(pos)

            if clicked_idx is not None:
                # Select and start dragging
                self.selected_waypoint = clicked_idx
                self.dragging = True
            else:
                # Place new waypoint
                self.waypoints.append((x, y))
                self.selected_waypoint = len(self.waypoints) - 1
                self.racing_line_dirty = True
                self.show_message(f"Waypoint {len(self.waypoints)} placed")

        elif button == 3:  # Right click
            # Delete waypoint at cursor
            clicked_idx = self.get_waypoint_at_pos(pos)
            if clicked_idx is not None:
                self.waypoints.pop(clicked_idx)
                self.selected_waypoint = None
                self.racing_line_dirty = True
                self.show_message(f"Waypoint deleted ({len(self.waypoints)} remaining)")

    def handle_mouse_up(self, button):
        """Handle mouse button release"""
        if button == 1:
            self.dragging = False

    def handle_mouse_motion(self, pos):
        """Handle mouse movement"""
        x, y = pos

        # Update hover state
        if x < TRACK_VIEW_WIDTH:
            self.hover_waypoint = self.get_waypoint_at_pos(pos)
        else:
            self.hover_waypoint = None

        # Handle dragging
        if self.dragging and self.selected_waypoint is not None:
            # Clamp to track view area
            x = max(0, min(x, TRACK_VIEW_WIDTH - 1))
            y = max(0, min(y, TRACK_VIEW_HEIGHT - 1))
            self.waypoints[self.selected_waypoint] = (x, y)
            self.racing_line_dirty = True

    def get_waypoint_at_pos(self, pos):
        """Get index of waypoint at mouse position, or None"""
        x, y = pos

        for i, (wx, wy) in enumerate(self.waypoints):
            dist = math.sqrt((x - wx) ** 2 + (y - wy) ** 2)
            if dist <= WAYPOINT_HOVER_RADIUS:
                return i

        return None

    def delete_selected_waypoint(self):
        """Delete the currently selected waypoint"""
        if self.selected_waypoint is not None and len(self.waypoints) > 0:
            self.waypoints.pop(self.selected_waypoint)
            self.selected_waypoint = None
            self.racing_line_dirty = True
            self.show_message(f"Waypoint deleted ({len(self.waypoints)} remaining)")

    def clear_waypoints(self):
        """Clear all waypoints"""
        self.waypoints = []
        self.selected_waypoint = None
        self.preview_progress = 0.0
        self.racing_line_dirty = True
        self.show_message("All waypoints cleared")

    def save_track(self):
        """Save track to JSON file"""
        if len(self.waypoints) < 3:
            self.show_message("Need at least 3 waypoints to save")
            return

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"track_{timestamp}.json"
        filepath = os.path.join("tools", "tracks", filename)

        # Create tracks directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save data
        data = {
            "waypoints": self.waypoints,
            "created": timestamp,
            "num_waypoints": len(self.waypoints),
            "background_image": self.bg_image_path,
            "background_opacity": self.bg_image_opacity
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            self.current_file = filename
            self.show_message(f"Saved: {filename}")
        except Exception as e:
            self.show_message(f"Save failed: {str(e)}")

    def load_track(self):
        """Load most recent track from tracks directory"""
        tracks_dir = os.path.join("tools", "tracks")

        if not os.path.exists(tracks_dir):
            self.show_message("No tracks directory found")
            return

        # Get all JSON files
        files = [f for f in os.listdir(tracks_dir) if f.endswith('.json')]

        if not files:
            self.show_message("No saved tracks found")
            return

        # Load most recent
        files.sort(reverse=True)
        filepath = os.path.join(tracks_dir, files[0])

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            self.waypoints = [tuple(wp) for wp in data['waypoints']]
            self.selected_waypoint = None
            self.preview_progress = 0.0
            self.current_file = files[0]
            self.racing_line_dirty = True

            # Load background image if present
            if 'background_image' in data and data['background_image']:
                self.bg_image_path = data['background_image']
                self.load_image_from_path(self.bg_image_path)

            if 'background_opacity' in data:
                self.bg_image_opacity = data['background_opacity']

            self.show_message(f"Loaded: {files[0]} ({len(self.waypoints)} points)")
        except Exception as e:
            self.show_message(f"Load failed: {str(e)}")

    def export_waypoints(self):
        """Export waypoints in Python format to file"""
        if len(self.waypoints) < 3:
            self.show_message("Need at least 3 waypoints to export")
            return

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"track_{timestamp}_export.py"
        filepath = os.path.join("tools", "tracks", filename)

        # Create tracks directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Build the Python code content
        content_lines = []
        content_lines.append("# F1 Track Waypoints Export")
        content_lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content_lines.append(f"# Total waypoints: {len(self.waypoints)}")
        content_lines.append("#")
        content_lines.append("# Copy the waypoints list below into race/track.py")
        content_lines.append("")
        content_lines.append("waypoints = [")

        # Format in rows of 5 for readability
        for i in range(0, len(self.waypoints), 5):
            row = self.waypoints[i:i+5]
            formatted = ", ".join([f"{wp}" for wp in row])
            content_lines.append(f"    {formatted},")

        content_lines.append("]")
        content_lines.append("")

        # Write to file
        try:
            with open(filepath, 'w') as f:
                f.write('\n'.join(content_lines))
            self.show_message(f"Exported to: {filename}")
        except Exception as e:
            self.show_message(f"Export failed: {str(e)}")


    def load_background_image(self):
        """Load a background image for tracing"""
        # Create tkinter root window (hidden)
        root = tk.Tk()
        root.withdraw()

        # Open file dialog
        filepath = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )

        root.destroy()

        if filepath:
            self.load_image_from_path(filepath)

    def load_image_from_path(self, filepath):
        """Load and scale an image from the given path"""
        try:
            # Load image
            original_image = pygame.image.load(filepath)

            # Scale to fit track view area (1000x900)
            scaled_image = pygame.transform.scale(original_image, (TRACK_VIEW_WIDTH, TRACK_VIEW_HEIGHT))

            # Convert to surface with alpha for opacity control
            self.bg_image = scaled_image.convert_alpha()
            self.bg_image_path = filepath

            filename = os.path.basename(filepath)
            self.show_message(f"Image loaded: {filename}")
        except Exception as e:
            self.show_message(f"Image load failed: {str(e)}")
            self.bg_image = None
            self.bg_image_path = None

    def toggle_image_visibility(self):
        """Toggle background image visibility"""
        if self.bg_image is None:
            self.show_message("No background image loaded")
            return

        self.bg_image_visible = not self.bg_image_visible
        self.show_message(f"Image: {'VISIBLE' if self.bg_image_visible else 'HIDDEN'}")

    def adjust_image_opacity(self, delta):
        """Adjust background image opacity"""
        if self.bg_image is None:
            self.show_message("No background image loaded")
            return

        self.bg_image_opacity = max(0, min(255, self.bg_image_opacity + delta))
        self.show_message(f"Image opacity: {int(self.bg_image_opacity / 255 * 100)}%")

    def show_message(self, text):
        """Display a temporary message"""
        self.message = text
        self.message_timer = 180  # 3 seconds at 60 FPS

    def update(self):
        """Update editor state"""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1

        # Update preview car
        if self.preview_enabled and len(self.waypoints) >= 3:
            self.preview_progress += self.preview_speed
            if self.preview_progress >= 1.0:
                self.preview_progress = 0.0

    def get_position_on_track(self, progress):
        """Get x, y position at given progress (0.0 to 1.0) along track"""
        if len(self.waypoints) < 2:
            return None

        track_length = len(self.waypoints)
        index = int(progress * track_length) % track_length
        next_index = (index + 1) % track_length

        # Interpolate between waypoints
        t = (progress * track_length) % 1.0
        x1, y1 = self.waypoints[index]
        x2, y2 = self.waypoints[next_index]

        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t

        return (x, y)

    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(BG_COLOR)

        # Draw track view background
        pygame.draw.rect(self.screen, TRACK_BG_COLOR, (0, 0, TRACK_VIEW_WIDTH, TRACK_VIEW_HEIGHT))

        # Draw grid
        self.draw_grid()

        # Draw background image (behind everything else)
        if self.bg_image and self.bg_image_visible:
            self.draw_background_image()

        # Draw racing line
        self.draw_racing_line()

        # Draw waypoints
        self.draw_waypoints()

        # Draw preview car
        if self.preview_enabled:
            self.draw_preview_car()

        # Draw UI panel
        self.draw_ui_panel()

        # Update display
        pygame.display.flip()

    def draw_grid(self):
        """Draw background grid"""
        for x in range(0, TRACK_VIEW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, TRACK_VIEW_HEIGHT), 1)
        for y in range(0, TRACK_VIEW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (TRACK_VIEW_WIDTH, y), 1)

    def draw_background_image(self):
        """Draw background image with current opacity"""
        # Create a copy with adjusted opacity
        image_copy = self.bg_image.copy()
        image_copy.set_alpha(self.bg_image_opacity)
        self.screen.blit(image_copy, (0, 0))

    def draw_racing_line(self):
        """Draw the racing line connecting waypoints"""
        if len(self.waypoints) < 2:
            return

        # Recreate surface if dirty or missing
        if self.racing_line_dirty or self.racing_line_surface is None:
            self.racing_line_surface = pygame.Surface((TRACK_VIEW_WIDTH, TRACK_VIEW_HEIGHT), pygame.SRCALPHA)
            
            # Draw line segments
            for i in range(len(self.waypoints)):
                next_i = (i + 1) % len(self.waypoints)
                pygame.draw.line(
                    self.racing_line_surface,
                    TRACK_LINE_COLOR,
                    self.waypoints[i],
                    self.waypoints[next_i],
                    TRACK_LINE_WIDTH
                )

            # Draw filled polygon if we have enough points
            if len(self.waypoints) >= 3:
                # Draw semi-transparent track surface
                pygame.draw.polygon(self.racing_line_surface, (*TRACK_LINE_COLOR, 30), self.waypoints)
            
            self.racing_line_dirty = False

        # Blit cached surface
        if self.racing_line_surface:
            self.screen.blit(self.racing_line_surface, (0, 0))

    def draw_waypoints(self):
        """Draw waypoint markers"""
        for i, (x, y) in enumerate(self.waypoints):
            # Determine color
            if i == self.selected_waypoint:
                color = WAYPOINT_SELECTED_COLOR
                radius = WAYPOINT_RADIUS + 2
            elif i == self.hover_waypoint:
                color = WAYPOINT_HOVER_COLOR
                radius = WAYPOINT_RADIUS + 1
            else:
                color = WAYPOINT_COLOR
                radius = WAYPOINT_RADIUS

            # Draw waypoint
            pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), radius, 2)

            # Draw number for selected/hover
            if i == self.selected_waypoint or i == self.hover_waypoint:
                text = self.font_small.render(str(i), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x, y - 20))
                self.screen.blit(text, text_rect)

    def draw_preview_car(self):
        """Draw animated preview car"""
        if len(self.waypoints) < 3:
            return

        pos = self.get_position_on_track(self.preview_progress)
        if pos:
            x, y = pos
            pygame.draw.circle(self.screen, PREVIEW_CAR_COLOR, (int(x), int(y)), PREVIEW_CAR_SIZE)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), PREVIEW_CAR_SIZE, 2)

    def draw_ui_panel(self):
        """Draw UI panel with controls and info"""
        # Background
        pygame.draw.rect(self.screen, PANEL_BG_COLOR, (PANEL_X, 0, PANEL_WIDTH, SCREEN_HEIGHT))

        y = 20

        # Title
        title = self.font_large.render("Track Editor", True, TEXT_COLOR)
        self.screen.blit(title, (PANEL_X + 10, y))
        y += 50

        # Stats
        stats = [
            f"Waypoints: {len(self.waypoints)}",
            f"Preview: {'ON' if self.preview_enabled else 'OFF'}",
            f"Selected: {self.selected_waypoint if self.selected_waypoint is not None else '-'}",
        ]

        for stat in stats:
            text = self.font_small.render(stat, True, TEXT_DIM_COLOR)
            self.screen.blit(text, (PANEL_X + 10, y))
            y += 25

        # Background image status
        if self.bg_image:
            bg_filename = os.path.basename(self.bg_image_path) if self.bg_image_path else "Unknown"
            if len(bg_filename) > 18:
                bg_filename = bg_filename[:15] + "..."
            bg_stats = [
                f"Image: {bg_filename}",
                f"Visible: {'Yes' if self.bg_image_visible else 'No'}",
                f"Opacity: {int(self.bg_image_opacity / 255 * 100)}%",
            ]
            for stat in bg_stats:
                text = self.font_small.render(stat, True, TEXT_DIM_COLOR)
                self.screen.blit(text, (PANEL_X + 10, y))
                y += 25

        y += 20

        # Controls
        pygame.draw.line(self.screen, GRID_COLOR, (PANEL_X + 10, y), (PANEL_X + PANEL_WIDTH - 10, y), 1)
        y += 15

        controls_title = self.font_medium.render("Controls", True, TEXT_COLOR)
        self.screen.blit(controls_title, (PANEL_X + 10, y))
        y += 30

        controls = [
            ("Click", "Place point"),
            ("Drag", "Move point"),
            ("Right Click", "Delete point"),
            ("Delete", "Remove selected"),
            ("Space", "Toggle preview"),
            ("S", "Save track"),
            ("L", "Load track"),
            ("C", "Clear all"),
            ("E", "Export code"),
            ("I", "Load image"),
            ("V", "Toggle image"),
            ("+/-", "Image opacity"),
            ("Esc", "Exit"),
        ]

        for key, action in controls:
            key_text = self.font_small.render(key, True, WAYPOINT_SELECTED_COLOR)
            action_text = self.font_small.render(action, True, TEXT_DIM_COLOR)
            self.screen.blit(key_text, (PANEL_X + 10, y))
            self.screen.blit(action_text, (PANEL_X + 70, y))
            y += 22

        # Message at bottom
        if self.message_timer > 0:
            y = SCREEN_HEIGHT - 100
            pygame.draw.rect(self.screen, (40, 40, 40), (PANEL_X, y, PANEL_WIDTH, 80))

            # Wrap message if too long
            words = self.message.split()
            lines = []
            current_line = []

            for word in words:
                current_line.append(word)
                test_text = ' '.join(current_line)
                if self.font_small.size(test_text)[0] > PANEL_WIDTH - 20:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:
                lines.append(' '.join(current_line))

            msg_y = y + 10
            for line in lines:
                msg_text = self.font_small.render(line, True, TEXT_COLOR)
                self.screen.blit(msg_text, (PANEL_X + 10, msg_y))
                msg_y += 22

def main():
    """Entry point for track editor"""
    editor = TrackEditor()
    editor.run()

if __name__ == "__main__":
    main()
