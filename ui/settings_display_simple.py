"""
SettingsDisplayScreen - Display/video settings
Shows resolution info and display options.
"""
import pygame
import config
from settings.runtime_config import runtime_config
from settings.persistence import SettingsPersistence


class SettingsDisplayScreen:
    """Settings screen for display configuration."""
    
    def __init__(self, surface, native_resolution):
        self.surface = surface
        self.screen_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.native_resolution = native_resolution
        
        # Fonts (cached)
        self.font_title = pygame.font.Font(None, 72)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_item = pygame.font.Font(None, 36)
        self.font_value = pygame.font.Font(None, 36)
        self.font_hint = pygame.font.Font(None, 24)
        
        # Colors
        self.color_bg = (15, 15, 15)
        self.color_title = (255, 255, 255)
        self.color_subtitle = (150, 150, 150)
        self.color_item = (200, 200, 200)
        self.color_value = (100, 200, 255)
        self.color_accent = (220, 0, 0)  # F1 Red
        self.color_box_bg = (30, 30, 30)
        self.color_box_border = (60, 60, 60)
        
        # Get current resolution index
        current_res = (runtime_config.display_width, runtime_config.display_height)
        self.resolution_index = 1  # Default to 1600x900
        for i, res in enumerate(config.SUPPORTED_RESOLUTIONS):
            if res == current_res:
                self.resolution_index = i
                break
        
        # Interactive items
        self.items = [
            {
                "name": "Resolution", 
                "type": "selector",
                "options": config.SUPPORTED_RESOLUTIONS,
                "current": self.resolution_index
            },
            {
                "name": "Display Mode", 
                "type": "toggle",
                "value": runtime_config.fullscreen
            },
            {
                "name": "UI Scale", 
                "type": "display",
                "value": f"{config.SCALE_FACTOR:.2f}x (auto)"
            },
        ]
        
        self.selected_index = 0  # Start on first item
        self.has_changes = False
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.has_changes:
                    self._save_settings()
                return "back"
            elif event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.items) + 1, self.selected_index + 1)  # +1 for Apply, +1 for Back
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                if self.selected_index < len(self.items):
                    self._handle_item_change(self.selected_index, event.key == pygame.K_RIGHT)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_index == len(self.items):  # Apply button
                    self._apply_settings()
                    return "restart_required"
                elif self.selected_index == len(self.items) + 1:  # Back button
                    if self.has_changes:
                        self._save_settings()
                    return "back"
                else:
                    # Toggle for boolean items
                    item = self.items[self.selected_index]
                    if item["type"] == "toggle":
                        self._handle_item_change(self.selected_index, True)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check button clicks
                if hasattr(self, 'apply_rect') and self.apply_rect.collidepoint(event.pos):
                    self._apply_settings()
                    return "restart_required"
                elif hasattr(self, 'back_rect') and self.back_rect.collidepoint(event.pos):
                    if self.has_changes:
                        self._save_settings()
                    return "back"
        
        return None
    
    def update(self):
        """Update screen."""
        pass
    
    def _handle_item_change(self, index, increase):
        """Handle changing an item's value."""
        if index >= len(self.items):
            return
            
        item = self.items[index]
        
        if item["type"] == "selector":
            # Resolution selector
            if increase:
                item["current"] = min(item["current"] + 1, len(item["options"]) - 1)
            else:
                item["current"] = max(item["current"] - 1, 0)
            self.has_changes = True
            
        elif item["type"] == "toggle":
            # Fullscreen toggle
            item["value"] = not item["value"]
            self.has_changes = True
    
    def _save_settings(self):
        """Save current settings to runtime config."""
        # Update resolution
        res_item = self.items[0]
        selected_res = res_item["options"][res_item["current"]]
        runtime_config.display_width = selected_res[0]
        runtime_config.display_height = selected_res[1]
        
        # Update fullscreen
        fullscreen_item = self.items[1]
        runtime_config.fullscreen = fullscreen_item["value"]
        
        # Save to disk
        SettingsPersistence.save(runtime_config)
        self.has_changes = False
    
    def _apply_settings(self):
        """Apply display settings (requires restart)."""
        self._save_settings()
        # Note: Actual display mode change requires game restart
    
    def render(self):
        """Render the display settings screen."""
        # Clear with dark background
        self.screen_surface.fill(self.color_bg)
        
        # Draw decorative elements
        self._draw_background_decoration()
        
        # Draw title
        self._draw_title()
        
        # Draw display info
        self._draw_items()
        
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
    
    def _draw_items(self):
        """Draw all display info items."""
        center_x = config.SCREEN_WIDTH // 2
        start_y = 200
        item_height = 70
        item_width = 600
        
        for i, item in enumerate(self.items):
            y_pos = start_y + i * item_height
            is_selected = (i == self.selected_index)
            
            # Item rect
            item_rect = pygame.Rect(
                center_x - item_width // 2,
                y_pos,
                item_width,
                item_height - 10
            )
            
            # Draw background
            bg_color = (40, 40, 40) if is_selected else self.color_box_bg
            pygame.draw.rect(self.screen_surface, bg_color, item_rect, border_radius=8)
            
            # Draw border
            border_color = self.color_accent if is_selected else self.color_box_border
            pygame.draw.rect(self.screen_surface, border_color, item_rect, width=2, border_radius=8)
            
            # Draw item name
            name_text = self.font_item.render(item["name"], True, self.color_item)
            self.screen_surface.blit(name_text, (item_rect.left + 20, y_pos + 15))
            
            # Draw value based on type
            if item["type"] == "selector":
                # Draw arrows and current value
                current_option = item["options"][item["current"]]
                value_text = f"< {current_option[0]} x {current_option[1]} >"
                value_surface = self.font_value.render(value_text, True, self.color_value)
                value_x = item_rect.right - value_surface.get_width() - 20
                self.screen_surface.blit(value_surface, (value_x, y_pos + 15))
                
            elif item["type"] == "toggle":
                # Draw toggle state
                value_text = "ON" if item["value"] else "OFF"
                color = self.color_value if item["value"] else self.color_subtitle
                value_surface = self.font_value.render(value_text, True, color)
                value_x = item_rect.right - value_surface.get_width() - 20
                self.screen_surface.blit(value_surface, (value_x, y_pos + 15))
                
            elif item["type"] == "display":
                # Draw read-only value
                value_surface = self.font_value.render(item["value"], True, self.color_subtitle)
                value_x = item_rect.right - value_surface.get_width() - 20
                self.screen_surface.blit(value_surface, (value_x, y_pos + 15))
        
        # Draw Apply button (if changes made)
        button_y = start_y + len(self.items) * item_height + 30
        
        if self.has_changes:
            is_apply_selected = (self.selected_index == len(self.items))
            
            self.apply_rect = pygame.Rect(
                center_x - 210,
                button_y,
                200,
                50
            )
            
            bg_color = (0, 100, 0) if is_apply_selected else (0, 60, 0)
            pygame.draw.rect(self.screen_surface, bg_color, self.apply_rect, border_radius=8)
            
            border_color = (0, 255, 0) if is_apply_selected else (0, 150, 0)
            pygame.draw.rect(self.screen_surface, border_color, self.apply_rect, width=2, border_radius=8)
            
            apply_text = self.font_item.render("APPLY", True, self.color_title)
            apply_text_rect = apply_text.get_rect(center=self.apply_rect.center)
            self.screen_surface.blit(apply_text, apply_text_rect)
            
            # Back button position when Apply is shown
            back_x = center_x + 10
        else:
            # Back button centered when no Apply button
            back_x = center_x - 100
        
        # Draw back button
        is_back_selected = (self.selected_index == len(self.items) + (1 if self.has_changes else 0))
        
        self.back_rect = pygame.Rect(
            back_x,
            button_y,
            200,
            50
        )
        
        bg_color = (40, 40, 40) if is_back_selected else self.color_box_bg
        pygame.draw.rect(self.screen_surface, bg_color, self.back_rect, border_radius=8)
        
        border_color = self.color_accent if is_back_selected else self.color_box_border
        pygame.draw.rect(self.screen_surface, border_color, self.back_rect, width=2, border_radius=8)
        
        back_text = self.font_item.render("BACK", True, self.color_title if is_back_selected else self.color_item)
        back_text_rect = back_text.get_rect(center=self.back_rect.center)
        self.screen_surface.blit(back_text, back_text_rect)
    
    def _draw_footer(self):
        """Draw footer with controls hint."""
        center_x = config.SCREEN_WIDTH // 2
        footer_y = config.SCREEN_HEIGHT - 50
        
        hint_text = self.font_hint.render(
            "Arrow Keys to navigate/change  |  ENTER to apply  |  ESC to go back",
            True,
            self.color_subtitle
        )
        hint_rect = hint_text.get_rect(center=(center_x, footer_y))
        self.screen_surface.blit(hint_text, hint_rect)
        
        if self.has_changes:
            warning_text = self.font_hint.render(
                "Changes require game restart",
                True,
                (255, 200, 0)  # Yellow warning
            )
            warning_rect = warning_text.get_rect(center=(center_x, footer_y - 25))
            self.screen_surface.blit(warning_text, warning_rect)