"""
Track Selection Screen - Browse and select tracks for racing
"""
import pygame
import config
from race.track_loader import get_available_tracks, load_track_waypoints, load_track_with_decorations, get_default_waypoints


class TrackSelectionScreen:
    """Screen for browsing and selecting tracks"""
    
    def __init__(self, surface):
        self.surface = surface
        self.selection_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        # Fonts
        self.font_title = pygame.font.Font(None, 72)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_track = pygame.font.Font(None, 42)
        self.font_track_info = pygame.font.Font(None, 24)
        self.font_hint = pygame.font.Font(None, 24)
        
        # Colors
        self.color_bg = (15, 15, 15)
        self.color_title = (255, 255, 255)
        self.color_subtitle = (150, 150, 150)
        self.color_track = (200, 200, 200)
        self.color_track_hover = (255, 255, 255)

        self.color_accent = (220, 0, 0)  # F1 Red
        self.color_box_bg = (30, 30, 30)
        self.color_box_border = (60, 60, 60)
        
        # Track list
        self.tracks = []
        self.selected_index = 0
        self.track_rects = []  # For mouse interaction
        
        # Currently selected track (persisted selection)
        self.current_selection_name = "Default Circuit"
        
        # Pending waypoints and decorations for the current selection (loaded when track is selected)
        self._pending_waypoints = None
        self._pending_decorations = None
        
        # Colors for selected indicator
        self.color_selected_badge = (0, 180, 80)  # Green for "SELECTED" badge
        
        # Load tracks
        self._load_tracks()
        
    def _load_tracks(self):
        """Load available tracks from directory"""
        self.tracks = []
        
        # Add default track first
        self.tracks.append({
            'name': 'Default Circuit',
            'filepath': None,  # None means use default waypoints
            'num_waypoints': 65,
            'is_default': True,
        })
        
        # Add tracks from directory
        available = get_available_tracks()
        for track in available:
            track['is_default'] = False
            self.tracks.append(track)
        
        # Reset selection
        self.selected_index = 0
        
    def set_current_selection(self, track_name):
        """Set the currently selected track (for highlighting when screen opens)"""
        self.current_selection_name = track_name
        # Find and select the track with this name
        for i, track in enumerate(self.tracks):
            if track['name'] == track_name:
                self.selected_index = i
                break
    
    def handle_event(self, event):
        """
        Handle input events.
        
        Returns:
            tuple or None:
                - ("select", track_name, waypoints) when ESC is pressed (confirm and exit)
                - None if no action (stay on screen)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_track()  # Just select, don't return
            elif event.key == pygame.K_ESCAPE:
                # Return selection when exiting (waypoints, decorations)
                return ("select", self.current_selection_name, self._pending_waypoints, self._pending_decorations)
                
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_hover(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_mouse_click(event.pos)  # Just select, don't return
        
        return None
    
    def _move_selection(self, direction):
        """Move track selection up or down"""
        if not self.tracks:
            return
            
        new_index = self.selected_index + direction
        
        # Wrap around
        if new_index < 0:
            new_index = len(self.tracks) - 1
        elif new_index >= len(self.tracks):
            new_index = 0
            
        self.selected_index = new_index
    
    def _select_track(self):
        """Mark the currently highlighted track as selected (but don't exit screen)"""
        if not self.tracks:
            return
            
        track = self.tracks[self.selected_index]
        track_name = track['name']
        
        # Update current selection name
        self.current_selection_name = track_name
        
        # Load and store waypoints and decorations for when we exit
        if track.get('is_default') or track.get('filepath') is None:
            self._pending_waypoints = None  # None means use default
            self._pending_decorations = None
        else:
            waypoints, decorations = load_track_with_decorations(track['filepath'])
            if waypoints is None:
                # Fallback to default if loading fails
                self._pending_waypoints = None
                self._pending_decorations = None
            else:
                self._pending_waypoints = waypoints
                self._pending_decorations = decorations
    
    def _handle_mouse_hover(self, pos):
        """Update hover state based on mouse position"""
        for i, rect in enumerate(self.track_rects):
            if rect and rect.collidepoint(pos):
                self.selected_index = i
                break
    
    def _handle_mouse_click(self, pos):
        """Handle mouse click on track items - selects track but stays on screen"""
        for i, rect in enumerate(self.track_rects):
            if rect and rect.collidepoint(pos):
                self.selected_index = i
                self._select_track()  # Just select, don't return
                return
        return None
    
    def update(self):
        """Update screen (for animations if needed)"""
        pass
    
    def render(self):
        """Render the track selection screen"""
        # Clear with dark background
        self.selection_surface.fill(self.color_bg)
        
        # Draw decorative elements
        self._draw_background_decoration()
        
        # Draw title
        self._draw_title()
        
        # Draw track list
        self._draw_track_list()
        
        # Draw footer
        self._draw_footer()
        
        # Blit to main surface
        self.surface.blit(self.selection_surface, (0, 0))
    
    def _draw_background_decoration(self):
        """Draw decorative background elements"""
        # Subtle racing stripes on the sides
        stripe_color = (25, 25, 25)
        stripe_width = 80
        
        # Left stripes
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.selection_surface,
                stripe_color,
                (offset, 0),
                (offset + 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
        # Right stripes
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.selection_surface,
                stripe_color,
                (config.SCREEN_WIDTH - offset, 0),
                (config.SCREEN_WIDTH - offset - 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
        # Accent line under title area
        pygame.draw.line(
            self.selection_surface,
            self.color_accent,
            (config.SCREEN_WIDTH // 2 - 200, 160),
            (config.SCREEN_WIDTH // 2 + 200, 160),
            3
        )
    
    def _draw_title(self):
        """Draw the screen title"""
        center_x = config.SCREEN_WIDTH // 2
        
        # Main title
        title_text = self.font_title.render("SELECT TRACK", True, self.color_title)
        title_rect = title_text.get_rect(center=(center_x, 80))
        self.selection_surface.blit(title_text, title_rect)
        
        # Subtitle
        track_count = len(self.tracks)
        subtitle = f"{track_count} track{'s' if track_count != 1 else ''} available"
        subtitle_text = self.font_subtitle.render(subtitle, True, self.color_subtitle)
        subtitle_rect = subtitle_text.get_rect(center=(center_x, 130))
        self.selection_surface.blit(subtitle_text, subtitle_rect)
    
    def _draw_track_list(self):
        """Draw the list of available tracks"""
        center_x = config.SCREEN_WIDTH // 2
        start_y = 220
        item_height = 70
        item_width = 500
        
        # Clear track rects
        self.track_rects = []
        
        # Calculate visible area
        max_visible = 8
        visible_tracks = self.tracks[:max_visible]
        
        for i, track in enumerate(visible_tracks):
            y_pos = start_y + i * item_height
            is_hovered = (i == self.selected_index)  # Currently hovered/keyboard-selected
            is_default = track.get('is_default', False)
            is_current_selection = (track['name'] == self.current_selection_name)  # Persisted selection
            
            # Item rect
            item_rect = pygame.Rect(
                center_x - item_width // 2,
                y_pos,
                item_width,
                item_height - 10
            )
            self.track_rects.append(item_rect)
            
            # Draw background box
            bg_color = (40, 40, 40) if is_hovered else self.color_box_bg
            pygame.draw.rect(self.selection_surface, bg_color, item_rect, border_radius=8)
            
            # Draw border - green for current selection, red for hover, default otherwise
            if is_current_selection:
                border_color = self.color_selected_badge
            elif is_hovered:
                border_color = self.color_accent
            else:
                border_color = self.color_box_border
            pygame.draw.rect(self.selection_surface, border_color, item_rect, width=2, border_radius=8)
            
            # Draw hover indicator (arrow)
            if is_hovered:
                indicator_x = item_rect.left - 30
                indicator_text = self.font_track.render(">", True, self.color_accent)
                self.selection_surface.blit(indicator_text, (indicator_x, y_pos + 10))
            
            # Draw track name - green only if selected, white if hovered, gray otherwise
            if is_current_selection:
                name_color = self.color_selected_badge
            elif is_hovered:
                name_color = self.color_track_hover
            else:
                name_color = self.color_track
            name_text = self.font_track.render(track['name'], True, name_color)
            self.selection_surface.blit(name_text, (item_rect.left + 20, y_pos + 8))
            
            # Draw "SELECTED" badge if this is the current selection
            if is_current_selection:
                badge_text = self.font_track_info.render("SELECTED", True, self.color_selected_badge)
                badge_x = item_rect.right - badge_text.get_width() - 15
                self.selection_surface.blit(badge_text, (badge_x, y_pos + 15))
            
            # Draw track info
            info_parts = []
            if is_default:
                info_parts.append("Built-in")
            info_parts.append(f"{track.get('num_waypoints', '?')} waypoints")
            info_str = " | ".join(info_parts)
            info_text = self.font_track_info.render(info_str, True, self.color_subtitle)
            self.selection_surface.blit(info_text, (item_rect.left + 20, y_pos + 38))
        
        # Show "more tracks" indicator if needed
        if len(self.tracks) > max_visible:
            more_text = self.font_track_info.render(
                f"+ {len(self.tracks) - max_visible} more tracks...",
                True,
                self.color_subtitle
            )
            more_rect = more_text.get_rect(center=(center_x, start_y + max_visible * item_height + 10))
            self.selection_surface.blit(more_text, more_rect)
    
    def _draw_footer(self):
        """Draw footer with controls hint"""
        center_x = config.SCREEN_WIDTH // 2
        footer_y = config.SCREEN_HEIGHT - 50
        
        # Controls hint
        hint_text = self.font_hint.render(
            "Arrow Keys to navigate  |  Enter to select  |  ESC to confirm & go back",
            True,
            self.color_subtitle
        )
        hint_rect = hint_text.get_rect(center=(center_x, footer_y))
        self.selection_surface.blit(hint_text, hint_rect)
    
    def refresh_tracks(self):
        """Refresh the track list from disk"""
        self._load_tracks()
