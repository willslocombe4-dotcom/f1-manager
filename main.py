"""
F1 Manager - Phase 1: Live Race Visualization
Main game loop
"""
import pygame
import sys
import config
from race.race_engine import RaceEngine
from ui.renderer import TrackRenderer
from ui.timing_screen import TimingScreen
from ui.results_screen import ResultsScreen


class F1Manager:
    """Main game class"""

    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("F1 Manager - Live Race")

        # Create display
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        # Initialize game components
        self.race_engine = RaceEngine()
        self.track_renderer = TrackRenderer(self.screen)
        self.timing_screen = TimingScreen(self.screen)
        self.results_screen = ResultsScreen(self.screen)

        # Game state
        self.running = True
        self.paused = False

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:
                    if self.race_engine.is_race_finished():
                        # New race with new grid
                        self.race_engine = RaceEngine()
                        self.results_screen.reset_scroll()
                    elif not self.race_engine.race_started:
                        self.race_engine.start_race()
                    else:
                        self.paused = not self.paused

                elif event.key == pygame.K_r:
                    # Restart race
                    self.race_engine = RaceEngine()
                    self.results_screen.reset_scroll()

                # Pass scroll events to results screen if race is finished
                elif self.race_engine.is_race_finished():
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        self.results_screen.handle_scroll(event)

            # Handle mouse wheel scrolling on results screen
            elif event.type == pygame.MOUSEWHEEL:
                if self.race_engine.is_race_finished():
                    self.results_screen.handle_scroll(event)

    def update(self):
        """Update game state"""
        if self.race_engine.race_started and not self.paused and not self.race_engine.is_race_finished():
            self.race_engine.update()

    def render(self):
        """Render everything"""
        # Clear screen
        self.screen.fill(config.BG_COLOR)

        # Check if race is finished
        if self.race_engine.is_race_finished():
            # Show results screen
            self.results_screen.render(self.race_engine)
        else:
            # Show normal race view
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

        # Show FPS
        fps = int(self.clock.get_fps())
        font_small = pygame.font.Font(None, 20)
        fps_text = font_small.render(f"FPS: {fps}", True, config.TEXT_GRAY)
        self.screen.blit(fps_text, (config.SCREEN_WIDTH - 80, 10))

        # Update display
        pygame.display.flip()

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
