"""
BaseSettingsScreen - Base class for all settings screens
Provides common rendering and navigation patterns.
"""
import pygame
import config


class SettingItem:
    """Represents a single setting that can be adjusted."""
    
    def __init__(self, name, key, value, min_val=None, max_val=None, 
                 step=None, format_func=None, options=None):
        """
        Initialize a setting item.
        
        Args:
            name: Display name
            key: Key for storing/retrieving value
            value: Current value
            min_val: Minimum value (for numeric settings)
            max_val: Maximum value (for numeric settings)
            step: Step size for adjustments
            format_func: Function to format value for display
            options: List of options (for selection settings)
        """
        self.name = name
        self.key = key
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.step = step if step is not None else 1
        self.format_func = format_func or str
        self.options = options
        self.rect = pygame.Rect(0, 0, 0, 0)
    
    def get_display_value(self):
        """Get formatted display value."""
        return self.format_func(self.value)
    
    def adjust(self, direction):
        """
        Adjust value by direction (-1 or +1).
        
        Returns:
            New value after adjustment
        """
        if self.options:
            # Cycle through options
            idx = self.options.index(self.value) if self.value in self.options else 0
            idx = (idx + direction) % len(self.options)
            self.value = self.options[idx]
        else:
            # Numeric adjustment
            new_val = self.value + (self.step * direction)
            if self.min_val is not None:
                new_val = max(self.min_val, new_val)
            if self.max_val is not None:
                new_val = min(self.max_val, new_val)
            self.value = new_val
        return self.value


class BaseSettingsScreen:
    """Base class for settings screens with common UI patterns."""
    
    def __init__(self, surface, title="SETTINGS"):
        self.surface = surface
        self.screen_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.title = title
        
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
        self.color_item_selected = (255, 255, 255)
        self.color_value = (100, 200, 255)
        self.color_accent = (220, 0, 0)  # F1 Red
        self.color_box_bg = (30, 30, 30)
        self.color_box_border = (60, 60, 60)
        
        # Settings items
        self.items = []
        self.selected_index = 0
        
        # Back item (always last)
        self.back_item = SettingItem("BACK", "back", None)
    
    def _init_items(self):
        """Override in subclass to initialize setting items."""
        pass
    
    def handle_event(self, event):
        """
        Handle input events.
        
        Returns:
            str or None: "back" to return to previous screen, None otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_UP:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
            elif event.key == pygame.K_LEFT:
                self._adjust_selected(-1)
            elif event.key == pygame.K_RIGHT:
                self._adjust_selected(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._activate_selected()
        
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_mouse_click(event.pos)
        
        return None
    
    def _move_selection(self, direction):
        """Move selection up or down."""
        total_items = len(self.items) + 1  # +1 for back item
        self.selected_index = (self.selected_index + direction) % total_items
    
    def _adjust_selected(self, direction):
        """Adjust the selected setting value."""
        if self.selected_index < len(self.items):
            item = self.items[self.selected_index]
            item.adjust(direction)
            self._on_value_changed(item)
    
    def _on_value_changed(self, item):
        """Override in subclass to handle value changes."""
        pass
    
    def _activate_selected(self):
        """Activate the selected item (for back button)."""
        if self.selected_index >= len(self.items):
            return "back"
        return None
    
    def _handle_mouse_hover(self, pos):
        """Update selection based on mouse position."""
        for i, item in enumerate(self.items):
            if item.rect and item.rect.collidepoint(pos):
                self.selected_index = i
                return
        if self.back_item.rect and self.back_item.rect.collidepoint(pos):
            self.selected_index = len(self.items)
    
    def _handle_mouse_click(self, pos):
        """Handle mouse click."""
        # Check back button
        if self.back_item.rect and self.back_item.rect.collidepoint(pos):
            return "back"
        
        # Check setting items for left/right click areas
        for i, item in enumerate(self.items):
            if item.rect and item.rect.collidepoint(pos):
                self.selected_index = i
                # Determine if click is on left or right side
                mid_x = item.rect.centerx
                if pos[0] < mid_x:
                    self._adjust_selected(-1)
                else:
                    self._adjust_selected(1)
                return None
        
        return None
    
    def update(self):
        """Update screen (for animations if needed)."""
        pass
    
    def render(self):
        """Render the settings screen."""
        # Clear with dark background
        self.screen_surface.fill(self.color_bg)
        
        # Draw decorative elements
        self._draw_background_decoration()
        
        # Draw title
        self._draw_title()
        
        # Draw settings items
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
        
        title_text = self.font_title.render(self.title, True, self.color_title)
        title_rect = title_text.get_rect(center=(center_x, 80))
        self.screen_surface.blit(title_text, title_rect)
    
    def _draw_items(self):
        """Draw all setting items."""
        center_x = config.SCREEN_WIDTH // 2
        start_y = 200
        item_height = 60
        item_width = 600
        
        # Draw setting items
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
            item.rect = item_rect
            
            # Draw background
            bg_color = (40, 40, 40) if is_selected else self.color_box_bg
            pygame.draw.rect(self.screen_surface, bg_color, item_rect, border_radius=5)
            
            # Draw border
            border_color = self.color_accent if is_selected else self.color_box_border
            pygame.draw.rect(self.screen_surface, border_color, item_rect, width=2, border_radius=5)
            
            # Draw selection indicator
            if is_selected:
                indicator_text = self.font_item.render(">", True, self.color_accent)
                self.screen_surface.blit(indicator_text, (item_rect.left - 25, y_pos + 10))
            
            # Draw item name
            name_color = self.color_item_selected if is_selected else self.color_item
            name_text = self.font_item.render(item.name, True, name_color)
            self.screen_surface.blit(name_text, (item_rect.left + 20, y_pos + 12))
            
            # Draw value with arrows
            if item.value is not None:
                value_str = item.get_display_value()
                value_text = self.font_value.render(value_str, True, self.color_value)
                value_x = item_rect.right - value_text.get_width() - 50
                self.screen_surface.blit(value_text, (value_x, y_pos + 12))
                
                # Draw adjustment arrows
                if is_selected:
                    left_arrow = self.font_value.render("<", True, self.color_accent)
                    right_arrow = self.font_value.render(">", True, self.color_accent)
                    self.screen_surface.blit(left_arrow, (value_x - 25, y_pos + 12))
                    self.screen_surface.blit(right_arrow, (item_rect.right - 30, y_pos + 12))
        
        # Draw back button
        back_y = start_y + len(self.items) * item_height + 20
        is_back_selected = (self.selected_index >= len(self.items))
        
        back_rect = pygame.Rect(
            center_x - 100,
            back_y,
            200,
            50
        )
        self.back_item.rect = back_rect
        
        bg_color = (40, 40, 40) if is_back_selected else self.color_box_bg
        pygame.draw.rect(self.screen_surface, bg_color, back_rect, border_radius=5)
        
        border_color = self.color_accent if is_back_selected else self.color_box_border
        pygame.draw.rect(self.screen_surface, border_color, back_rect, width=2, border_radius=5)
        
        back_color = self.color_item_selected if is_back_selected else self.color_item
        back_text = self.font_item.render("BACK", True, back_color)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen_surface.blit(back_text, back_text_rect)
    
    def _draw_footer(self):
        """Draw footer with controls hint."""
        center_x = config.SCREEN_WIDTH // 2
        footer_y = config.SCREEN_HEIGHT - 50
        
        hint_text = self.font_hint.render(
            "Arrow Keys to navigate  |  Left/Right to adjust  |  ESC to go back",
            True,
            self.color_subtitle
        )
        hint_rect = hint_text.get_rect(center=(center_x, footer_y))
        self.screen_surface.blit(hint_text, hint_rect)
