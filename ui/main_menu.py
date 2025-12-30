"""
Main Menu - F1 Manager game main menu with navigation
"""
import pygame
import config


class MenuItem:
    """Represents a clickable menu item"""
    
    def __init__(self, text, action, enabled=True, subtitle=None):
        self.text = text
        self.action = action
        self.enabled = enabled
        self.subtitle = subtitle  # Optional subtitle (e.g., "Coming Soon")
        self.rect = pygame.Rect(0, 0, 0, 0)  # Set during rendering
        self.hovered = False


class MainMenu:
    """Main menu screen with navigation options"""
    
    def __init__(self, surface):
        self.surface = surface
        self.menu_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        # Fonts
        self.font_title = pygame.font.Font(None, 96)
        self.font_subtitle = pygame.font.Font(None, 36)
        self.font_menu = pygame.font.Font(None, 48)
        self.font_menu_small = pygame.font.Font(None, 28)
        self.font_hint = pygame.font.Font(None, 24)
        
        # Colors
        self.color_title = (255, 255, 255)
        self.color_menu = (200, 200, 200)
        self.color_menu_hover = (255, 255, 255)
        self.color_menu_disabled = (100, 100, 100)
        self.color_subtitle = (150, 150, 150)
        self.color_accent = (220, 0, 0)  # F1 Red
        self.color_bg = (15, 15, 15)
        
        # Menu items
        self.menu_items = [
            MenuItem("QUICK RACE", "quick_race"),
            MenuItem("CAREER MODE", "career_mode", enabled=False, subtitle="Coming Soon"),
            MenuItem("TRACK SELECTION", "track_selection"),
            MenuItem("CONFIG", "config"),  # Renamed from SETTINGS
            MenuItem("SETTINGS", "settings", subtitle="Display options"),  # New display settings
            MenuItem("QUIT", "quit"),
        ]
        
        self.selected_index = 0
        
        # Selected track name (shown under Quick Race)
        self.selected_track_name = "Default Circuit"
        
        # Animation
        self.title_offset = 0
        self.animation_time = 0
        
    def handle_event(self, event):
        """
        Handle input events.
        
        Returns:
            str or None: Action to perform, or None if no action
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._activate_selected()
            elif event.key == pygame.K_ESCAPE:
                return "quit"
                
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_hover(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_mouse_click(event.pos)
        
        return None
    
    def _move_selection(self, direction):
        """Move menu selection up or down"""
        new_index = self.selected_index + direction
        
        # Wrap around
        if new_index < 0:
            new_index = len(self.menu_items) - 1
        elif new_index >= len(self.menu_items):
            new_index = 0
            
        self.selected_index = new_index
    
    def _activate_selected(self):
        """Activate the currently selected menu item"""
        item = self.menu_items[self.selected_index]
        if item.enabled:
            return item.action
        return None
    
    def _handle_mouse_hover(self, pos):
        """Update hover state based on mouse position"""
        for i, item in enumerate(self.menu_items):
            if item.rect and item.rect.collidepoint(pos):
                self.selected_index = i
                item.hovered = True
            else:
                item.hovered = False
    
    def _handle_mouse_click(self, pos):
        """Handle mouse click on menu items"""
        for item in self.menu_items:
            if item.rect and item.rect.collidepoint(pos) and item.enabled:
                return item.action
        return None
    
    def set_selected_track(self, track_name):
        """Set the currently selected track name for display"""
        self.selected_track_name = track_name
        # Update the Quick Race menu item subtitle
        for item in self.menu_items:
            if item.action == "quick_race":
                item.subtitle = track_name
                break
    
    def update(self):
        """Update menu animations"""
        self.animation_time += 1
        # Subtle floating animation for title
        self.title_offset = 3 * pygame.math.Vector2(0, 1).rotate(self.animation_time * 2).y
    
    def render(self):
        """Render the main menu"""
        # Clear with dark background
        self.menu_surface.fill(self.color_bg)
        
        # Draw decorative elements
        self._draw_background_decoration()
        
        # Draw title
        self._draw_title()
        
        # Draw menu items
        self._draw_menu_items()
        
        # Draw footer
        self._draw_footer()
        
        # Blit to main surface
        self.surface.blit(self.menu_surface, (0, 0))
    
    def _draw_background_decoration(self):
        """Draw decorative background elements"""
        # Subtle racing stripes on the sides
        stripe_color = (25, 25, 25)
        stripe_width = 80
        
        # Left stripes
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.menu_surface,
                stripe_color,
                (offset, 0),
                (offset + 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
        # Right stripes
        for i in range(3):
            offset = i * 30
            pygame.draw.line(
                self.menu_surface,
                stripe_color,
                (config.SCREEN_WIDTH - offset, 0),
                (config.SCREEN_WIDTH - offset - 200, config.SCREEN_HEIGHT),
                stripe_width
            )
        
        # Accent line under title area
        pygame.draw.line(
            self.menu_surface,
            self.color_accent,
            (config.SCREEN_WIDTH // 2 - 200, 200),
            (config.SCREEN_WIDTH // 2 + 200, 200),
            3
        )
    
    def _draw_title(self):
        """Draw the game title"""
        center_x = config.SCREEN_WIDTH // 2
        
        # Main title
        title_text = self.font_title.render("F1 MANAGER", True, self.color_title)
        title_rect = title_text.get_rect(center=(center_x, 120 + self.title_offset))
        self.menu_surface.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_subtitle.render("2025 SEASON", True, self.color_subtitle)
        subtitle_rect = subtitle_text.get_rect(center=(center_x, 170))
        self.menu_surface.blit(subtitle_text, subtitle_rect)
    
    def _draw_menu_items(self):
        """Draw all menu items"""
        center_x = config.SCREEN_WIDTH // 2
        start_y = 300
        item_spacing = 80
        
        for i, item in enumerate(self.menu_items):
            y_pos = start_y + i * item_spacing
            is_selected = (i == self.selected_index)
            
            # Determine colors
            if not item.enabled:
                text_color = self.color_menu_disabled
            elif is_selected:
                text_color = self.color_menu_hover
            else:
                text_color = self.color_menu
            
            # Draw selection indicator
            if is_selected and item.enabled:
                # Draw bracket indicators
                indicator_offset = 180
                indicator_text = self.font_menu.render(">", True, self.color_accent)
                self.menu_surface.blit(
                    indicator_text,
                    (center_x - indicator_offset, y_pos - 5)
                )
                indicator_text = self.font_menu.render("<", True, self.color_accent)
                self.menu_surface.blit(
                    indicator_text,
                    (center_x + indicator_offset - 20, y_pos - 5)
                )
                
                # Draw subtle highlight box
                box_width = 350
                box_height = 50
                box_rect = pygame.Rect(
                    center_x - box_width // 2,
                    y_pos - 10,
                    box_width,
                    box_height
                )
                pygame.draw.rect(
                    self.menu_surface,
                    (30, 30, 30),
                    box_rect,
                    border_radius=5
                )
                pygame.draw.rect(
                    self.menu_surface,
                    self.color_accent if item.enabled else (60, 60, 60),
                    box_rect,
                    width=2,
                    border_radius=5
                )
            
            # Draw menu text
            menu_text = self.font_menu.render(item.text, True, text_color)
            menu_rect = menu_text.get_rect(center=(center_x, y_pos + 10))
            self.menu_surface.blit(menu_text, menu_rect)
            
            # Store rect for mouse interaction
            item.rect = pygame.Rect(
                center_x - 175,
                y_pos - 10,
                350,
                50
            )
            
            # Draw subtitle if present
            if item.subtitle:
                subtitle_text = self.font_menu_small.render(
                    item.subtitle, True, self.color_subtitle
                )
                subtitle_rect = subtitle_text.get_rect(center=(center_x, y_pos + 40))
                self.menu_surface.blit(subtitle_text, subtitle_rect)
    
    def _draw_footer(self):
        """Draw footer with controls hint"""
        center_x = config.SCREEN_WIDTH // 2
        footer_y = config.SCREEN_HEIGHT - 50
        
        # Controls hint
        hint_text = self.font_hint.render(
            "Use Arrow Keys or Mouse to navigate  |  Enter to select  |  ESC to quit",
            True,
            self.color_subtitle
        )
        hint_rect = hint_text.get_rect(center=(center_x, footer_y))
        self.menu_surface.blit(hint_text, hint_rect)
        
        # Version info
        version_text = self.font_hint.render(
            "v0.1.0 - Phase 1",
            True,
            (80, 80, 80)
        )
        self.menu_surface.blit(version_text, (20, config.SCREEN_HEIGHT - 30))
