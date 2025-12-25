"""
F1 Manager - Phase 1: Live Race Visualization
Main game loop with state machine
"""
import pygame
import sys
import config
from race.race_engine import RaceEngine
from race.track_loader import get_default_waypoints
from ui.renderer import TrackRenderer
from ui.timing_screen import TimingScreen
from ui.results_screen import ResultsScreen
from ui.main_menu import MainMenu
from ui.track_selection import TrackSelectionScreen
from ui.settings_screen import SettingsScreen
from settings.runtime_config import runtime_config
from settings.persistence import SettingsPersistence


class F1Manager:
    """Main game class with state machine"""

    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("F1 Manager - Live Race")

        # Create display
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        # Game state
        self.state = config.GAME_STATE_MENU
        self.running = True
        self.paused = False
        
        # Current track waypoints and decorations (None = default)
        self.current_waypoints = None
        self.current_decorations = None
        
        # Selected track from Track Selection
        self.selected_track_name = "Default Circuit"  # Track name for display
        self.selected_waypoints = None  # Waypoints for race (None = default)
        self.selected_decorations = None  # Decorations for race (None = default)

        # Initialize UI components (always available)
        self.main_menu = MainMenu(self.screen)
        self.main_menu.set_selected_track(self.selected_track_name)
        self.track_selection = TrackSelectionScreen(self.screen)
        self.settings_screen = SettingsScreen(self.screen)
        
        # Race components (initialized when race starts)
        self.race_engine = None
        self.track_renderer = None
        self.timing_screen = None
        self.results_screen = None
        
        # Load saved settings on startup
        SettingsPersistence.load(runtime_config)

    def _start_race(self, waypoints=None, decorations=None):
        """Initialize and start a race with optional custom waypoints and decorations"""
        self.current_waypoints = waypoints
        self.current_decorations = decorations
        self.race_engine = RaceEngine(waypoints=waypoints, decorations=decorations)
        self.track_renderer = TrackRenderer(self.screen)
        self.timing_screen = TimingScreen(self.screen)
        self.results_screen = ResultsScreen(self.screen)
        self.paused = False
        self.state = config.GAME_STATE_RACING

    def _return_to_menu(self):
        """Clean up race and return to main menu"""
        # Reset track renderer cache if it exists
        if self.track_renderer:
            self.track_renderer.reset_cache()
        
        # Clear race components
        self.race_engine = None
        self.track_renderer = None
        self.timing_screen = None
        self.results_screen = None
        
        # Reset menu state
        self.main_menu.selected_index = 0
        self.state = config.GAME_STATE_MENU

    def handle_events(self):
        """Handle user input based on current state"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Route events based on state
            if self.state == config.GAME_STATE_MENU:
                self._handle_menu_event(event)
            elif self.state == config.GAME_STATE_TRACK_SELECTION:
                self._handle_track_selection_event(event)
            elif self.state == config.GAME_STATE_SETTINGS:
                self._handle_settings_event(event)
            elif self.state == config.GAME_STATE_RACING:
                self._handle_racing_event(event)
            elif self.state == config.GAME_STATE_RESULTS:
                self._handle_results_event(event)

    def _handle_menu_event(self, event):
        """Handle events in main menu state"""
        action = self.main_menu.handle_event(event)
        
        if action == "quick_race":
            self._start_race(waypoints=self.selected_waypoints, decorations=self.selected_decorations)  # Use selected track or default
        elif action == "track_selection":
            self.track_selection.refresh_tracks()
            self.track_selection.set_current_selection(self.selected_track_name)
            self.state = config.GAME_STATE_TRACK_SELECTION
        elif action == "settings":
            self.state = config.GAME_STATE_SETTINGS
        elif action == "quit":
            self.running = False

    def _handle_track_selection_event(self, event):
        """Handle events in track selection state"""
        result = self.track_selection.handle_event(event)
        
        if isinstance(result, tuple) and result[0] == "select":
            # ESC was pressed - store selected track name, waypoints, and decorations, return to menu
            self.selected_track_name = result[1]
            self.selected_waypoints = result[2]
            self.selected_decorations = result[3] if len(result) > 3 else None
            self.main_menu.set_selected_track(self.selected_track_name)
            self.state = config.GAME_STATE_MENU

    def _handle_settings_event(self, event):
        """Handle events in settings state"""
        result = self.settings_screen.handle_event(event)
        
        if result == "back":
            # Save settings when leaving settings screen
            SettingsPersistence.save(runtime_config)
            self.state = config.GAME_STATE_MENU

    def _handle_racing_event(self, event):
        """Handle events during racing"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._return_to_menu()
                return

            elif event.key == pygame.K_SPACE:
                if self.race_engine.is_race_finished():
                    # Race finished - go to results
                    self.state = config.GAME_STATE_RESULTS
                elif not self.race_engine.race_started:
                    self.race_engine.start_race()
                else:
                    self.paused = not self.paused

            elif event.key == pygame.K_r:
                # Restart race with same track
                self._start_race(waypoints=self.current_waypoints, decorations=self.current_decorations)

            # Speed control keys (1-5)
            elif event.key == pygame.K_1:
                self.race_engine.set_simulation_speed(1)
            elif event.key == pygame.K_2:
                self.race_engine.set_simulation_speed(2)
            elif event.key == pygame.K_3:
                self.race_engine.set_simulation_speed(5)
            elif event.key == pygame.K_4:
                self.race_engine.set_simulation_speed(10)
            elif event.key == pygame.K_5:
                self.race_engine.set_simulation_speed(20)

        # Handle mouse clicks for speed buttons
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_speed_button_click(event.pos)

    def _handle_results_event(self, event):
        """Handle events on results screen"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._return_to_menu()
                return
            
            elif event.key == pygame.K_SPACE:
                # Return to menu
                self._return_to_menu()
                return
            
            elif event.key == pygame.K_r:
                # Restart race with same track
                self._start_race(waypoints=self.current_waypoints, decorations=self.current_decorations)
                return
            
            # Scroll events
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                self.results_screen.handle_scroll(event)

        # Handle mouse wheel scrolling
        elif event.type == pygame.MOUSEWHEEL:
            self.results_screen.handle_scroll(event)

    def _handle_speed_button_click(self, pos):
        """Check if a speed button was clicked"""
        x, y = pos
        options = config.SIMULATION_SPEED_OPTIONS
        button_width = 35
        button_height = 25
        margin = 5
        start_x = config.TRACK_VIEW_WIDTH - (len(options) * (button_width + margin)) - 10
        btn_y = 10
        
        if btn_y <= y <= btn_y + button_height:
            for i, speed in enumerate(options):
                btn_x = start_x + i * (button_width + margin)
                if btn_x <= x <= btn_x + button_width:
                    self.race_engine.set_simulation_speed(speed)
                    break

    def update(self):
        """Update game state based on current state"""
        if self.state == config.GAME_STATE_MENU:
            self.main_menu.update()
        elif self.state == config.GAME_STATE_TRACK_SELECTION:
            self.track_selection.update()
        elif self.state == config.GAME_STATE_SETTINGS:
            self.settings_screen.update()
        elif self.state == config.GAME_STATE_RACING:
            if self.race_engine and self.race_engine.race_started and not self.paused:
                if self.race_engine.is_race_finished():
                    # Auto-transition to results
                    self.state = config.GAME_STATE_RESULTS
                else:
                    self.race_engine.update()

    def render(self):
        """Render based on current state"""
        # Clear screen
        self.screen.fill(config.BG_COLOR)

        if self.state == config.GAME_STATE_MENU:
            self.main_menu.render()
            
        elif self.state == config.GAME_STATE_TRACK_SELECTION:
            self.track_selection.render()
            
        elif self.state == config.GAME_STATE_SETTINGS:
            self.settings_screen.render()
            
        elif self.state == config.GAME_STATE_RACING:
            self._render_race()
            
        elif self.state == config.GAME_STATE_RESULTS:
            self.results_screen.render(self.race_engine)

        # Show FPS (always)
        fps = int(self.clock.get_fps())
        font_small = pygame.font.Font(None, 20)
        fps_text = font_small.render(f"FPS: {fps}", True, config.TEXT_GRAY)
        self.screen.blit(fps_text, (config.SCREEN_WIDTH - 80, 10))

        # Update display
        pygame.display.flip()

    def _render_race(self):
        """Render the race view"""
        # Render track and cars
        self.track_renderer.render(self.race_engine)

        # Render timing screen
        self.timing_screen.render(self.race_engine)

        # Draw separator line
        pygame.draw.line(
            self.screen,
            config.TRACK_LINE_COLOR,
            (config.TRACK_VIEW_WIDTH, 0),
            (config.TRACK_VIEW_WIDTH, config.SCREEN_HEIGHT),
            2
        )

        # Show pause indicator
        if self.paused:
            font = pygame.font.Font(None, 48)
            pause_text = font.render("PAUSED", True, config.TEXT_COLOR)
            pause_rect = pause_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
            )
            # Draw semi-transparent background
            bg_rect = pause_rect.inflate(40, 20)
            overlay = pygame.Surface((bg_rect.width, bg_rect.height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, bg_rect)
            self.screen.blit(pause_text, pause_rect)

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(config.FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = F1Manager()
    game.run()


if __name__ == "__main__":
    main()
