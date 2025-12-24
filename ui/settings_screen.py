"""
SettingsScreen - Main settings menu with category navigation
"""
import pygame
import config
from settings.runtime_config import runtime_config
from settings.persistence import SettingsPersistence


class SettingsCategory:
    """Represents a settings category/submenu."""
    
    def __init__(self, name, action, subtitle=None, enabled=True):
        self.name = name
        self.action = action
        self.subtitle = subtitle
        self.enabled = enabled
        self.rect = pygame.Rect(0, 0, 0, 0)


class SettingsScreen:
    """Main settings screen with category navigation."""
    
    def __init__(self, surface):
        self.surface = surface
        self.screen_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        # Fonts (cached)
        self.font_title = pygame.font.Font(None, 72)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_category = pygame.font.Font(None, 42)
        self.font_category_sub = pygame.font.Font(None, 24)
        self.font_hint = pygame.font.Font(None, 24)
        
        # Colors
        self.color_bg = (15, 15, 15)
        self.color_title = (255, 255, 255)
        self.color_subtitle = (150, 150, 150)
        self.color_category = (200, 200, 200)
        self.color_category_selected = (255, 255, 255)
        self.color_category_disabled = (100, 100, 100)
        self.color_accent = (220, 0, 0)  # F1 Red
        self.color_box_bg = (30, 30, 30)
        self.color_box_border = (60, 60, 60)
        
        # Categories
        self.categories = [
            SettingsCategory("PRESETS", "presets", "Load/save configurations"),
            SettingsCategory("RACE", "race", "Laps, simulation speed"),
            SettingsCategory("TIRES", "tires", "Degradation, cliff settings"),
            SettingsCategory("FUEL", "fuel", "Burn rate, weight penalty"),
            SettingsCategory("PIT STOPS", "pitstops", "Times, variance"),
            SettingsCategory("PERFORMANCE", "performance", "Tier modifiers, synergy"),
            SettingsCategory("TEAMS", "teams", "Coming in Phase 3", enabled=False),
            SettingsCategory("DRIVERS", "drivers", "Coming in Phase 3", enabled=False),
            SettingsCategory("BACK", "back", "Return to main menu"),
        ]
        
        self.selected_index = 0
        
        # Subscreen instances (lazy loaded)
        self._subscreens = {}
        
        # Current active subscreen
        self.active_subscreen = None
    
    def _get_subscreen(self, action):
        """Get or create a subscreen instance."""
        if action not in self._subscreens:
            if action == "presets":
                from ui.settings_presets import SettingsPresetsScreen
                self._subscreens[action] = SettingsPresetsScreen(self.surface)
            elif action == "race":
                from ui.settings_race import SettingsRaceScreen
                self._subscreens[action] = SettingsRaceScreen(self.surface)
            elif action == "tires":
                from ui.settings_tires import SettingsTiresScreen
                self._subscreens[action] = SettingsTiresScreen(self.surface)
            elif action == "fuel":
                from ui.settings_fuel import SettingsFuelScreen
                self._subscreens[action] = SettingsFuelScreen(self.surface)
            elif action == "pitstops":
                from ui.settings_pitstops import SettingsPitstopsScreen
                self._subscreens[action] = SettingsPitstopsScreen(self.surface)
            elif action == "performance":
                from ui.settings_performance import SettingsPerformanceScreen
                self._subscreens[action] = SettingsPerformanceScreen(self.surface)
            elif action == "teams":
                from ui.settings_teams import SettingsTeamsScreen
                self._subscreens[action] = SettingsTeamsScreen(self.surface)
            elif action == "drivers":
                from ui.settings_drivers import SettingsDriversScreen
                self._subscreens[action] = SettingsDriversScreen(self.surface)
        return self._subscreens.get(action)
    
    def _clear_settings_subscreens(self):
        """Clear cached subscreens so they reload fresh values from runtime_config."""
        # Keep presets screen, clear all others
        presets_screen = self._subscreens.get("presets")
        self._subscreens.clear()
        if presets_screen:
            self._subscreens["presets"] = presets_screen
    
    def handle_event(self, event):
        """
        Handle input events.
        
        Returns:
            str or None: "back" to return to main menu, None otherwise
        """
        # If subscreen is active, delegate to it
        if self.active_subscreen:
            result = self.active_subscreen.handle_event(event)
            if result == "back":
                # If returning from presets screen, clear cached subscreens
                # so they reload fresh values from runtime_config
                if self.active_subscreen == self._subscreens.get("presets"):
                    self._clear_settings_subscreens()
                self.active_subscreen = None
            return None
        
        # Handle main menu events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_UP:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._activate_selected()
        
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self._handle_mouse_click(event.pos)
        
        return None
    
    def _move_selection(self, direction):
        """Move selection up or down."""
        new_index = self.selected_index + direction
        if new_index < 0:
            new_index = len(self.categories) - 1
        elif new_index >= len(self.categories):
            new_index = 0
        self.selected_index = new_index
    
    def _activate_selected(self):
        """Activate the selected category."""
        category = self.categories[self.selected_index]
        if not category.enabled:
            return None
        
        if category.action == "back":
            return "back"
        
        # Open subscreen
        subscreen = self._get_subscreen(category.action)
        if subscreen:
            self.active_subscreen = subscreen
        
        return None
    
    def _handle_mouse_hover(self, pos):
        """Update selection based on mouse position."""
        for i, category in enumerate(self.categories):
            if category.rect and category.rect.collidepoint(pos):
                self.selected_index = i
                return
    
    def _handle_mouse_click(self, pos):
        """Handle mouse click."""
        for i, category in enumerate(self.categories):
            if category.rect and category.rect.collidepoint(pos):
                self.selected_index = i
                return self._activate_selected()
        return None
    
    def update(self):
        """Update screen."""
        if self.active_subscreen:
            self.active_subscreen.update()
    
    def render(self):
        """Render the settings screen."""
        # If subscreen is active, render it instead
        if self.active_subscreen:
            self.active_subscreen.render()
            return
        
        # Clear with dark background
        self.screen_surface.fill(self.color_bg)
        
        # Draw decorative elements
        self._draw_background_decoration()
        
        # Draw title
        self._draw_title()
        
        # Draw categories
        self._draw_categories()
        
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
    
    def _draw_categories(self):
        """Draw all category items."""
        center_x = config.SCREEN_WIDTH // 2
        start_y = 180
        item_height = 70
        item_width = 500
        
        for i, category in enumerate(self.categories):
            y_pos = start_y + i * item_height
            is_selected = (i == self.selected_index)
            
            # Item rect
            item_rect = pygame.Rect(
                center_x - item_width // 2,
                y_pos,
                item_width,
                item_height - 10
            )
            category.rect = item_rect
            
            # Determine colors
            if not category.enabled:
                text_color = self.color_category_disabled
                border_color = self.color_box_border
            elif is_selected:
                text_color = self.color_category_selected
                border_color = self.color_accent
            else:
                text_color = self.color_category
                border_color = self.color_box_border
            
            # Draw background
            bg_color = (40, 40, 40) if is_selected and category.enabled else self.color_box_bg
            pygame.draw.rect(self.screen_surface, bg_color, item_rect, border_radius=8)
            
            # Draw border
            pygame.draw.rect(self.screen_surface, border_color, item_rect, width=2, border_radius=8)
            
            # Draw selection indicator
            if is_selected and category.enabled:
                indicator_text = self.font_category.render(">", True, self.color_accent)
                self.screen_surface.blit(indicator_text, (item_rect.left - 30, y_pos + 8))
            
            # Draw category name
            name_text = self.font_category.render(category.name, True, text_color)
            self.screen_surface.blit(name_text, (item_rect.left + 20, y_pos + 8))
            
            # Draw subtitle
            if category.subtitle:
                sub_color = self.color_subtitle if category.enabled else self.color_category_disabled
                sub_text = self.font_category_sub.render(category.subtitle, True, sub_color)
                self.screen_surface.blit(sub_text, (item_rect.left + 20, y_pos + 38))
    
    def _draw_footer(self):
        """Draw footer with controls hint."""
        center_x = config.SCREEN_WIDTH // 2
        footer_y = config.SCREEN_HEIGHT - 50
        
        hint_text = self.font_hint.render(
            "Arrow Keys to navigate  |  Enter to select  |  ESC to go back",
            True,
            self.color_subtitle
        )
        hint_rect = hint_text.get_rect(center=(center_x, footer_y))
        self.screen_surface.blit(hint_text, hint_rect)
