"""
SettingsDisplayScreen - Display/video settings
Shows resolution info and display options with ability to change them.
"""
import pygame
import config


class SettingsDisplayScreen:
    """Settings screen for display configuration."""
    
    def __init__(self, surface, native_resolution):
        self.surface = surface
        self.screen_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.current_resolution = current_resolution
        self.available_resolutions = available_resolutions
        self.is_fullscreen = is_fullscreen
        
        # Selected resolution index
        self.selected_resolution_index = 0
        for i, res in enumerate(self.available_resolutions):
            if res == current_resolution:
                self.selected_resolution_index = i
                break
        
        # Fonts (cached)
        self.font_title = pygame.font.Font(None, 72)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_item = pygame.font.Font(None, 36)
        self.font_value = pygame.font.Font(None, 36)
        self.font_hint = pygame.font.Font(None, 24)
        self.font_button = pygame.font.Font(None, 28)
        
        # Colors
        self.color_bg = (15, 15, 15)
        self.color_title = (255, 255, 255)
        self.color_subtitle = (150, 150, 150)
        self.color_item = (200, 200, 200)
        self.color_value = (100, 200, 255)
        self.color_accent = (220, 0, 0)  # F1 Red
        self.color_box_bg = (30, 30, 30)
        self.color_box_border = (60, 60, 60)
        self.color_button = (50, 50, 50)
        self.color_button_hover = (70, 70, 70)
        
        # Menu items
        self.menu_items = [
            "resolution",
            "fullscreen",
            "apply",
            "back"
        ]
        self.selected_index = 0
        
        # Pending changes
        self.pending_resolution = self.current_resolution
        self.pending_fullscreen = self.is_fullscreen
        self.has_changes = False
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.menu_items) - 1, self.selected_index + 1)
            elif event.key == pygame.K_LEFT:
                self._handle_left()
            elif event.key == pygame.K_RIGHT:
                self._handle_right()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._handle_select()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check button clicks
                mouse_pos = event.pos
                # TODO: Add mouse click handling for buttons
        
        return None
    
    def _handle_left(self):
        """Handle left arrow key."""
        if self.menu_items[self.selected_index] == "resolution":
            # Cycle to previous resolution
            self.selected_resolution_index = (self.selected_resolution_index - 1) % len(self.available_resolutions)
            self.pending_resolution = self.available_resolutions[self.selected_resolution_index]
            self._check_changes()
        elif self.menu_items[self.selected_index] == "fullscreen":
            # Toggle fullscreen
            self.pending_fullscreen = not self.pending_fullscreen
            self._check_changes()
    
    def _handle_right(self):
        """Handle right arrow key."""
        if self.menu_items[self.selected_index] == "resolution":
            # Cycle to next resolution
            self.selected_resolution_index = (self.selected_resolution_index + 1) % len(self.available_resolutions)
            self.pending_resolution = self.available_resolutions[self.selected_resolution_index]
            self._check_changes()
        elif self.menu_items[self.selected_index] == "fullscreen":
            # Toggle fullscreen
            self.pending_fullscreen = not self.pending_fullscreen
            self._check_changes()
    
    def _handle_select(self):
        """Handle selection/enter key."""
        selected_item = self.menu_items[self.selected_index]
        
        if selected_item == "apply":
            if self.has_changes:
                # Return the new settings to apply
                return ("apply_display", self.pending_resolution, self.pending_fullscreen)
        elif selected_item == "back":
            return "back"
        elif selected_item == "fullscreen":
            # Toggle on select too
            self.pending_fullscreen = not self.pending_fullscreen
            self._check_changes()
        
        return None
    
    def _check_changes(self):
        """Check if there are pending changes."""
        self.has_changes = (
            self.pending_resolution != self.current_resolution or
            self.pending_fullscreen != self.is_fullscreen
        )
    
    def update(self):
        """Update screen."""
        pass
    
    def render(self):
        """Render the display settings screen."""
        # Clear with dark background
        self.screen_surface.fill(self.color_bg)
        
        # Draw decorative elements
        self._draw_background_decoration()
        
        # Draw title
        self._draw_title()
        
        # Draw menu items
        self._draw_menu_items()
        
        # Draw footer
        self._draw_footer()
        
        # Blit to main surface
        self.surface.blit(self.screen_surface, (0, 0))
    
    def _draw_background_decoration(self):
        """Draw decorative background elements."""
        stripe_color = (25, 25, 25)
        stripe_width = 80
        
        # Left stripes
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.screen_surface,
                stripe_color,
                (offset, 0),
                (offset + 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
        # Right stripes
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.screen_surface,
                stripe_color,
                (config.SCREEN_WIDTH - offset, 0),
                (config.SCREEN_WIDTH - offset - 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
        # Accent line under title
        pygame.draw.line(
            self.screen_surface,
            self.color_accent,
            (config.SCREEN_WIDTH // 2 - 200, 140),
            (config.SCREEN_WIDTH // 2 + 200, 140),
            3
        )
    
    def _draw_title(self):
        """Draw the screen title."""
        center_x = config.SCREEN_WIDTH // 2
        
        title_text = self.font_title.render("SETTINGS", True, self.color_title)
        title_rect = title_text.get_rect(center=(center_x, 80))
        self.screen_surface.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_subtitle.render("Display Options", True, self.color_subtitle)
        subtitle_rect = subtitle_text.get_rect(center=(center_x, 120))
        self.screen_surface.blit(subtitle_text, subtitle_rect)
    
    def _draw_menu_items(self):
        """Draw all menu items."""
        center_x = config.SCREEN_WIDTH // 2
        start_y = 200
        item_height = 70
        item_width = 600
        
        # Resolution selector
        y_pos = start_y
        is_selected = (self.selected_index == 0)
        self._draw_resolution_selector(center_x, y_pos, item_width, item_height - 10, is_selected)
        
        # Fullscreen toggle
        y_pos = start_y + item_height
        is_selected = (self.selected_index == 1)
        self._draw_fullscreen_toggle(center_x, y_pos, item_width, item_height - 10, is_selected)
        
        # Current info
        y_pos = start_y + item_height * 2
        self._draw_current_info(center_x, y_pos, item_width, item_height - 10)
        
        # Apply button
        y_pos = start_y + item_height * 3 + 20
        is_selected = (self.selected_index == 2)
        self._draw_apply_button(center_x, y_pos, is_selected)
        
        # Back button
        y_pos = start_y + item_height * 3 + 80
        is_selected = (self.selected_index == 3)
        self._draw_back_button(center_x, y_pos, is_selected)
    
    def _draw_resolution_selector(self, center_x, y_pos, width, height, is_selected):
        """Draw resolution selector."""
        rect = pygame.Rect(center_x - width // 2, y_pos, width, height)
        
        # Background
        bg_color = (40, 40, 40) if is_selected else self.color_box_bg
        pygame.draw.rect(self.screen_surface, bg_color, rect, border_radius=8)
        
        # Border
        border_color = self.color_accent if is_selected else self.color_box_border
        pygame.draw.rect(self.screen_surface, border_color, rect, width=2, border_radius=8)
        
        # Label
        label_text = self.font_item.render("Resolution", True, self.color_item)
        self.screen_surface.blit(label_text, (rect.left + 20, y_pos + 15))
        
        # Value with arrows
        res_text = f"< {self.pending_resolution[0]} x {self.pending_resolution[1]} >"
        value_text = self.font_value.render(res_text, True, self.color_value if is_selected else self.color_subtitle)
        value_x = rect.right - value_text.get_width() - 20
        self.screen_surface.blit(value_text, (value_x, y_pos + 15))
    
    def _draw_fullscreen_toggle(self, center_x, y_pos, width, height, is_selected):
        """Draw fullscreen toggle."""
        rect = pygame.Rect(center_x - width // 2, y_pos, width, height)
        
        # Background
        bg_color = (40, 40, 40) if is_selected else self.color_box_bg
        pygame.draw.rect(self.screen_surface, bg_color, rect, border_radius=8)
        
        # Border
        border_color = self.color_accent if is_selected else self.color_box_border
        pygame.draw.rect(self.screen_surface, border_color, rect, width=2, border_radius=8)
        
        # Label
        label_text = self.font_item.render("Display Mode", True, self.color_item)
        self.screen_surface.blit(label_text, (rect.left + 20, y_pos + 15))
        
        # Value
        mode_text = "Fullscreen" if self.pending_fullscreen else "Windowed"
        value_text = self.font_value.render(mode_text, True, self.color_value if is_selected else self.color_subtitle)
        value_x = rect.right - value_text.get_width() - 20
        self.screen_surface.blit(value_text, (value_x, y_pos + 15))
    
    def _draw_current_info(self, center_x, y_pos, width, height):
        """Draw current display info."""
        rect = pygame.Rect(center_x - width // 2, y_pos, width, height)
        
        # Background (darker)
        pygame.draw.rect(self.screen_surface, (20, 20, 20), rect, border_radius=8)
        pygame.draw.rect(self.screen_surface, (40, 40, 40), rect, width=1, border_radius=8)
        
        # Current resolution
        current_text = f"Current: {self.current_resolution[0]}x{self.current_resolution[1]} "
        current_text += f"({'Fullscreen' if self.is_fullscreen else 'Windowed'})"
        info_text = self.font_hint.render(current_text, True, self.color_subtitle)
        info_x = rect.centerx - info_text.get_width() // 2
        self.screen_surface.blit(info_text, (info_x, y_pos + 10))
        
        # UI Scale
        scale_text = f"UI Scale: {config.SCALE_FACTOR:.2f}x"
        scale_surface = self.font_hint.render(scale_text, True, self.color_subtitle)
        scale_x = rect.centerx - scale_surface.get_width() // 2
        self.screen_surface.blit(scale_surface, (scale_x, y_pos + 30))
    
    def _draw_apply_button(self, center_x, y_pos, is_selected):
        """Draw apply button."""
        button_width = 200
        button_height = 50
        
        rect = pygame.Rect(center_x - button_width // 2, y_pos, button_width, button_height)
        
        # Background - highlight if changes pending
        if self.has_changes:
            bg_color = (0, 100, 0) if is_selected else (0, 70, 0)
        else:
            bg_color = (40, 40, 40) if is_selected else self.color_box_bg
        
        pygame.draw.rect(self.screen_surface, bg_color, rect, border_radius=8)
        
        # Border
        border_color = self.color_accent if is_selected else self.color_box_border
        pygame.draw.rect(self.screen_surface, border_color, rect, width=2, border_radius=8)
        
        # Text
        text = "APPLY CHANGES" if self.has_changes else "APPLY"
        button_text = self.font_item.render(text, True, self.color_title if is_selected else self.color_item)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen_surface.blit(button_text, text_rect)
    
    def _draw_back_button(self, center_x, y_pos, is_selected):
        """Draw back button."""
        button_width = 200
        button_height = 50
        
        rect = pygame.Rect(center_x - button_width // 2, y_pos, button_width, button_height)
        
        # Background
        bg_color = (40, 40, 40) if is_selected else self.color_box_bg
        pygame.draw.rect(self.screen_surface, bg_color, rect, border_radius=8)
        
        # Border
        border_color = self.color_accent if is_selected else self.color_box_border
        pygame.draw.rect(self.screen_surface, border_color, rect, width=2, border_radius=8)
        
        # Text
        button_text = self.font_item.render("BACK", True, self.color_title if is_selected else self.color_item)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen_surface.blit(button_text, text_rect)
    
    def _draw_footer(self):
        """Draw footer with controls hint."""
        center_x = config.SCREEN_WIDTH // 2
        footer_y = config.SCREEN_HEIGHT - 50
        
        hint_text = self.font_hint.render(
            "Arrow Keys to navigate/change  |  ENTER to select  |  ESC to go back",
            True,
            self.color_subtitle
        )
        hint_rect = hint_text.get_rect(center=(center_x, footer_y))
        self.screen_surface.blit(hint_text, hint_rect)