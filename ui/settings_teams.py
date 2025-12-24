"""
SettingsTeamsScreen - Placeholder for team settings (Phase 3)
"""
import pygame
import config


class SettingsTeamsScreen:
    """Placeholder settings screen for team configuration."""
    
    def __init__(self, surface):
        self.surface = surface
        self.screen_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        # Fonts (cached)
        self.font_title = pygame.font.Font(None, 72)
        self.font_message = pygame.font.Font(None, 36)
        self.font_hint = pygame.font.Font(None, 24)
        
        # Colors
        self.color_bg = (15, 15, 15)
        self.color_title = (255, 255, 255)
        self.color_subtitle = (150, 150, 150)
        self.color_accent = (220, 0, 0)
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return "back"
        return None
    
    def update(self):
        """Update screen."""
        pass
    
    def render(self):
        """Render the placeholder screen."""
        self.screen_surface.fill(self.color_bg)
        
        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2
        
        # Title
        title = self.font_title.render("TEAM SETTINGS", True, self.color_title)
        title_rect = title.get_rect(center=(center_x, center_y - 60))
        self.screen_surface.blit(title, title_rect)
        
        # Coming soon message
        message = self.font_message.render("Coming in Phase 3", True, self.color_subtitle)
        message_rect = message.get_rect(center=(center_x, center_y + 10))
        self.screen_surface.blit(message, message_rect)
        
        # Hint
        hint = self.font_hint.render("Press ESC or Enter to go back", True, self.color_subtitle)
        hint_rect = hint.get_rect(center=(center_x, config.SCREEN_HEIGHT - 50))
        self.screen_surface.blit(hint, hint_rect)
        
        self.surface.blit(self.screen_surface, (0, 0))
