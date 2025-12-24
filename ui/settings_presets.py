"""
SettingsPresetsScreen - Load/save presets UI
"""
import pygame
import config
from settings.runtime_config import runtime_config
from settings.presets import PresetManager, BUILTIN_PRESETS


class SettingsPresetsScreen:
    """Settings screen for loading and saving presets."""
    
    def __init__(self, surface):
        self.surface = surface
        self.screen_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        # Fonts (cached)
        self.font_title = pygame.font.Font(None, 72)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_preset = pygame.font.Font(None, 36)
        self.font_preset_desc = pygame.font.Font(None, 24)
        self.font_hint = pygame.font.Font(None, 24)
        self.font_input = pygame.font.Font(None, 32)
        
        # Colors
        self.color_bg = (15, 15, 15)
        self.color_title = (255, 255, 255)
        self.color_subtitle = (150, 150, 150)
        self.color_preset = (200, 200, 200)
        self.color_preset_selected = (255, 255, 255)
        self.color_accent = (220, 0, 0)  # F1 Red
        self.color_box_bg = (30, 30, 30)
        self.color_box_border = (60, 60, 60)
        self.color_builtin = (100, 200, 255)  # Blue for built-in
        self.color_custom = (100, 255, 100)   # Green for custom
        
        # Preset manager
        self.preset_manager = PresetManager()
        
        # State
        self.selected_index = 0
        self.preset_rects = []
        
        # Save mode state
        self.save_mode = False
        self.save_name = ""
        self.save_description = ""
        self.save_field = 0  # 0 = name, 1 = description
        
        # Status message
        self.status_message = ""
        self.status_timer = 0
    
    def _get_all_items(self):
        """Get all preset items plus action items."""
        items = []
        
        # Built-in presets
        for preset in BUILTIN_PRESETS:
            items.append({
                "type": "preset",
                "preset": preset,
                "is_builtin": True,
            })
        
        # Custom presets
        for preset in self.preset_manager.get_custom_presets():
            items.append({
                "type": "preset",
                "preset": preset,
                "is_builtin": False,
            })
        
        # Save current as preset
        items.append({
            "type": "action",
            "name": "SAVE CURRENT AS PRESET",
            "action": "save",
        })
        
        # Back
        items.append({
            "type": "action",
            "name": "BACK",
            "action": "back",
        })
        
        return items
    
    def handle_event(self, event):
        """Handle input events."""
        # Handle save mode input
        if self.save_mode:
            return self._handle_save_mode_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_UP:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._activate_selected()
            elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                self._delete_selected()
            elif event.key == pygame.K_u:
                self._update_selected()
        
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self._handle_mouse_click(event.pos)
        
        return None
    
    def _handle_save_mode_event(self, event):
        """Handle events in save mode."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.save_mode = False
                self.save_name = ""
                self.save_description = ""
                return None
            elif event.key == pygame.K_TAB:
                self.save_field = (self.save_field + 1) % 2
            elif event.key == pygame.K_RETURN:
                if self.save_field == 0 and self.save_name:
                    self.save_field = 1
                elif self.save_field == 1:
                    self._save_preset()
            elif event.key == pygame.K_BACKSPACE:
                if self.save_field == 0:
                    self.save_name = self.save_name[:-1]
                else:
                    self.save_description = self.save_description[:-1]
            else:
                # Add character
                char = event.unicode
                if char and char.isprintable():
                    if self.save_field == 0 and len(self.save_name) < 20:
                        self.save_name += char
                    elif self.save_field == 1 and len(self.save_description) < 40:
                        self.save_description += char
        
        return None
    
    def _save_preset(self):
        """Save the current settings as a preset."""
        if not self.save_name:
            self.status_message = "Please enter a name"
            self.status_timer = 120
            return
        
        self.preset_manager.save_custom_preset(
            self.save_name,
            self.save_description or "Custom preset",
            runtime_config.to_dict()
        )
        
        self.save_mode = False
        self.save_name = ""
        self.save_description = ""
        self.status_message = "Preset saved!"
        self.status_timer = 120
    
    def _move_selection(self, direction):
        """Move selection up or down."""
        items = self._get_all_items()
        self.selected_index = (self.selected_index + direction) % len(items)
    
    def _activate_selected(self):
        """Activate the selected item."""
        items = self._get_all_items()
        if self.selected_index >= len(items):
            return None
        
        item = items[self.selected_index]
        
        if item["type"] == "preset":
            # Load preset
            preset = item["preset"]
            runtime_config.from_dict(preset["settings"])
            self.status_message = f"Loaded: {preset['name']}"
            self.status_timer = 120
            return None
        
        elif item["type"] == "action":
            if item["action"] == "save":
                self.save_mode = True
                self.save_field = 0
                return None
            elif item["action"] == "back":
                return "back"
        
        return None
    
    def _delete_selected(self):
        """Delete the selected custom preset."""
        items = self._get_all_items()
        if self.selected_index >= len(items):
            return
        
        item = items[self.selected_index]
        
        if item["type"] == "preset" and not item["is_builtin"]:
            preset = item["preset"]
            self.preset_manager.delete_custom_preset(preset["name"])
            self.status_message = f"Deleted: {preset['name']}"
            self.status_timer = 120
            # Adjust selection if needed
            if self.selected_index >= len(self._get_all_items()):
                self.selected_index = max(0, len(self._get_all_items()) - 1)
    
    def _update_selected(self):
        """Update the selected custom preset with current settings."""
        items = self._get_all_items()
        if self.selected_index >= len(items):
            return
        
        item = items[self.selected_index]
        
        # Can only update custom presets
        if item["type"] == "preset" and not item["is_builtin"]:
            preset = item["preset"]
            # Update with current runtime_config values
            self.preset_manager.save_custom_preset(
                preset["name"],
                preset.get("description", "Custom preset"),
                runtime_config.to_dict()
            )
            self.status_message = f"Updated: {preset['name']}"
            self.status_timer = 120
    
    def _handle_mouse_hover(self, pos):
        """Update selection based on mouse position."""
        for i, rect in enumerate(self.preset_rects):
            if rect and rect.collidepoint(pos):
                self.selected_index = i
                return
    
    def _handle_mouse_click(self, pos):
        """Handle mouse click."""
        for i, rect in enumerate(self.preset_rects):
            if rect and rect.collidepoint(pos):
                self.selected_index = i
                return self._activate_selected()
        return None
    
    def update(self):
        """Update screen."""
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer <= 0:
                self.status_message = ""
    
    def render(self):
        """Render the presets screen."""
        # Clear with dark background
        self.screen_surface.fill(self.color_bg)
        
        # Draw decorative elements
        self._draw_background_decoration()
        
        # Draw title
        self._draw_title()
        
        if self.save_mode:
            self._draw_save_dialog()
        else:
            # Draw preset list
            self._draw_presets()
        
        # Draw status message
        if self.status_message:
            self._draw_status()
        
        # Draw footer
        self._draw_footer()
        
        # Blit to main surface
        self.surface.blit(self.screen_surface, (0, 0))
    
    def _draw_background_decoration(self):
        """Draw decorative background elements."""
        stripe_color = (25, 25, 25)
        stripe_width = 80
        
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.screen_surface,
                stripe_color,
                (offset, 0),
                (offset + 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.screen_surface,
                stripe_color,
                (config.SCREEN_WIDTH - offset, 0),
                (config.SCREEN_WIDTH - offset - 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
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
        
        title_text = self.font_title.render("PRESETS", True, self.color_title)
        title_rect = title_text.get_rect(center=(center_x, 80))
        self.screen_surface.blit(title_text, title_rect)
    
    def _draw_presets(self):
        """Draw all preset items."""
        center_x = config.SCREEN_WIDTH // 2
        start_y = 180
        item_height = 70
        item_width = 550
        
        items = self._get_all_items()
        self.preset_rects = []
        
        for i, item in enumerate(items):
            y_pos = start_y + i * item_height
            is_selected = (i == self.selected_index)
            
            # Item rect
            item_rect = pygame.Rect(
                center_x - item_width // 2,
                y_pos,
                item_width,
                item_height - 10
            )
            self.preset_rects.append(item_rect)
            
            # Draw background
            bg_color = (40, 40, 40) if is_selected else self.color_box_bg
            pygame.draw.rect(self.screen_surface, bg_color, item_rect, border_radius=8)
            
            # Draw border
            border_color = self.color_accent if is_selected else self.color_box_border
            pygame.draw.rect(self.screen_surface, border_color, item_rect, width=2, border_radius=8)
            
            # Draw selection indicator
            if is_selected:
                indicator_text = self.font_preset.render(">", True, self.color_accent)
                self.screen_surface.blit(indicator_text, (item_rect.left - 25, y_pos + 12))
            
            if item["type"] == "preset":
                preset = item["preset"]
                is_builtin = item["is_builtin"]
                
                # Draw preset name
                name_color = self.color_preset_selected if is_selected else self.color_preset
                name_text = self.font_preset.render(preset["name"], True, name_color)
                self.screen_surface.blit(name_text, (item_rect.left + 20, y_pos + 8))
                
                # Draw type badge
                badge_color = self.color_builtin if is_builtin else self.color_custom
                badge_text = "BUILT-IN" if is_builtin else "CUSTOM"
                badge = self.font_preset_desc.render(badge_text, True, badge_color)
                self.screen_surface.blit(badge, (item_rect.right - badge.get_width() - 15, y_pos + 12))
                
                # Draw description
                desc_text = self.font_preset_desc.render(preset.get("description", ""), True, self.color_subtitle)
                self.screen_surface.blit(desc_text, (item_rect.left + 20, y_pos + 38))
            
            else:
                # Action item
                name_color = self.color_preset_selected if is_selected else self.color_preset
                name_text = self.font_preset.render(item["name"], True, name_color)
                name_rect = name_text.get_rect(center=item_rect.center)
                self.screen_surface.blit(name_text, name_rect)
    
    def _draw_save_dialog(self):
        """Draw the save preset dialog."""
        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2
        
        # Dialog box
        dialog_width = 500
        dialog_height = 250
        dialog_rect = pygame.Rect(
            center_x - dialog_width // 2,
            center_y - dialog_height // 2,
            dialog_width,
            dialog_height
        )
        
        pygame.draw.rect(self.screen_surface, self.color_box_bg, dialog_rect, border_radius=10)
        pygame.draw.rect(self.screen_surface, self.color_accent, dialog_rect, width=2, border_radius=10)
        
        # Title
        title = self.font_subtitle.render("SAVE PRESET", True, self.color_title)
        title_rect = title.get_rect(center=(center_x, dialog_rect.top + 30))
        self.screen_surface.blit(title, title_rect)
        
        # Name field
        name_label = self.font_preset_desc.render("Name:", True, self.color_subtitle)
        self.screen_surface.blit(name_label, (dialog_rect.left + 30, dialog_rect.top + 70))
        
        name_box = pygame.Rect(dialog_rect.left + 30, dialog_rect.top + 95, dialog_width - 60, 35)
        box_color = self.color_accent if self.save_field == 0 else self.color_box_border
        pygame.draw.rect(self.screen_surface, (20, 20, 20), name_box)
        pygame.draw.rect(self.screen_surface, box_color, name_box, width=2)
        
        name_text = self.font_input.render(self.save_name + ("|" if self.save_field == 0 else ""), True, self.color_title)
        self.screen_surface.blit(name_text, (name_box.left + 10, name_box.top + 5))
        
        # Description field
        desc_label = self.font_preset_desc.render("Description:", True, self.color_subtitle)
        self.screen_surface.blit(desc_label, (dialog_rect.left + 30, dialog_rect.top + 140))
        
        desc_box = pygame.Rect(dialog_rect.left + 30, dialog_rect.top + 165, dialog_width - 60, 35)
        box_color = self.color_accent if self.save_field == 1 else self.color_box_border
        pygame.draw.rect(self.screen_surface, (20, 20, 20), desc_box)
        pygame.draw.rect(self.screen_surface, box_color, desc_box, width=2)
        
        desc_text = self.font_input.render(self.save_description + ("|" if self.save_field == 1 else ""), True, self.color_title)
        self.screen_surface.blit(desc_text, (desc_box.left + 10, desc_box.top + 5))
        
        # Instructions
        hint = self.font_preset_desc.render("Tab to switch fields | Enter to save | ESC to cancel", True, self.color_subtitle)
        hint_rect = hint.get_rect(center=(center_x, dialog_rect.bottom - 20))
        self.screen_surface.blit(hint, hint_rect)
    
    def _draw_status(self):
        """Draw status message."""
        center_x = config.SCREEN_WIDTH // 2
        
        status_text = self.font_subtitle.render(self.status_message, True, self.color_custom)
        status_rect = status_text.get_rect(center=(center_x, config.SCREEN_HEIGHT - 100))
        self.screen_surface.blit(status_text, status_rect)
    
    def _draw_footer(self):
        """Draw footer with controls hint."""
        center_x = config.SCREEN_WIDTH // 2
        footer_y = config.SCREEN_HEIGHT - 50
        
        hint = "Enter to load  |  U to update  |  Delete to remove  |  ESC to go back"
        hint_text = self.font_hint.render(hint, True, self.color_subtitle)
        hint_rect = hint_text.get_rect(center=(center_x, footer_y))
        self.screen_surface.blit(hint_text, hint_rect)
