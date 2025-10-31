"""Main GUI application for interactive molecular dynamics."""

import logging
import pygame
from typing import Optional
import sys

from molecular_dynamics_toy.widgets.picker import PeriodicTableWidget
from molecular_dynamics_toy.widgets.controls import ControlsWidget
from molecular_dynamics_toy.widgets.simulation import SimulationWidget
from molecular_dynamics_toy.data import colors
from molecular_dynamics_toy.calculators import get_calculator

logger = logging.getLogger(__name__)


class MDApplication:
    """Main application window for interactive molecular dynamics.
    
    Manages the pygame window, event loop, and coordinates between different
    UI widgets (simulation renderer, periodic table, controls).
    
    Attributes:
        screen: Pygame display surface.
        clock: Pygame clock for controlling frame rate.
        running: Flag indicating if application is running.
        fps: Target frames per second.
        show_fps: Whether to display FPS counter.
    """
    
    # Window dimensions
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    
    # Widget layout (position and size rectangles)
    SIMULATION_RECT = pygame.Rect(50, 50, 700, 700)
    PERIODIC_TABLE_RECT = pygame.Rect(800, 50, 550, 400)
    CONTROLS_RECT = pygame.Rect(800, 500, 550, 250)
    
    # Colors
    BG_COLOR = colors.BG_COLOR
    WIDGET_BG_COLOR = colors.WIDGET_BG_COLOR
    BORDER_COLOR = colors.BORDER_COLOR
    TEXT_COLOR = colors.TEXT_COLOR
    
    def __init__(self, fps: int = 30, calculator: str = "mattersim", show_fps: bool = True):
        """Initialize the application.
        
        Args:
            fps: Target frames per second.
            calculator: Calculator name ('mattersim', 'mock').
        """
        pygame.init()
        
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Interactive Molecular Dynamics")
        
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False
        self.show_fps = show_fps
        
        # Font for debug/placeholder text
        self.font = pygame.font.Font(None, 24)
        self.fps_font = pygame.font.Font(None, 20)
        
        # Widgets (to be implemented)
        self.simulation_widget = SimulationWidget(self.SIMULATION_RECT, calculator=get_calculator(calculator))
        self.periodic_table_widget = PeriodicTableWidget(self.PERIODIC_TABLE_RECT)
        self.controls_widget = ControlsWidget(self.CONTROLS_RECT)
        
        self._update_layout()

        logger.info(f"MDApplication initialized: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT} @ {fps} FPS")
        
    def handle_events(self):
        """Process pygame events.
        
        Distributes events to appropriate widgets and handles global events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                logger.info("Quit event received")
                
            elif event.type == pygame.VIDEORESIZE:
                self.WINDOW_WIDTH = event.w
                self.WINDOW_HEIGHT = event.h
                self._update_layout()
                logger.debug(f"Window resized to {event.w}x{event.h}")
                    
            # Pass events to widgets when they exist
            if self.simulation_widget:
                self.simulation_widget.handle_event(event)
            if self.periodic_table_widget:
                self.periodic_table_widget.handle_event(event)
            if self.controls_widget:
                self.controls_widget.handle_event(event)
                    
    def update(self):
        """Update application state.
        
        Called once per frame to update all widgets.
        """
        # Pass selected element to simulation widget
        if self.simulation_widget and self.periodic_table_widget:
            self.simulation_widget.selected_element = self.periodic_table_widget.selected_element
            
        # Handle reset
        if self.controls_widget and self.controls_widget.reset_requested and self.simulation_widget:
            self.simulation_widget.reset()
            self.controls_widget.reset_requested = False  # Clear flag after consuming
            
        # Update simulation parameters
        if self.simulation_widget and self.controls_widget:
            self.simulation_widget.engine.temperature = self.controls_widget.temperature
            self.simulation_widget.engine.timestep = self.controls_widget.timestep
            
        # Update simulation with play state and speed
        if self.simulation_widget and self.controls_widget:
            self.simulation_widget.update(
                self.controls_widget.playing,
                self.controls_widget.steps_per_frame
            )
        
    def render(self):
        """Render the application.
        
        Draws background and all widgets to the screen.
        """
        # Fill background
        self.screen.fill(self.BG_COLOR)
        
        # Render widgets when they exist
        if self.simulation_widget:
            self.simulation_widget.render(self.screen)
        if self.periodic_table_widget:
            self.periodic_table_widget.render(self.screen)
        if self.controls_widget:
            self.controls_widget.render(self.screen)

        # Draw FPS counter
        if self.show_fps:
            self._render_fps()
        
        pygame.display.flip()
    
    def _render_fps(self):
        """Render FPS counter in top-left corner."""
        fps_value = self.clock.get_fps()
        fps_text = f"FPS: {fps_value:.1f}"
        fps_surface = self.fps_font.render(fps_text, True, self.TEXT_COLOR)
        
        # Draw semi-transparent background
        padding = 5
        bg_rect = fps_surface.get_rect(topleft=(10, 10)).inflate(padding * 2, padding * 2)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(180)
        bg_surface.fill((255, 255, 255))
        self.screen.blit(bg_surface, bg_rect)
        
        # Draw text
        self.screen.blit(fps_surface, (10 + padding, 10 + padding))

    def _draw_widget_placeholder(self, rect: pygame.Rect, title: str, subtitle: str):
        """Draw a placeholder box for a widget.
        
        Args:
            rect: Rectangle defining widget position and size.
            title: Widget title text.
            subtitle: Widget description text.
        """
        # Draw background
        pygame.draw.rect(self.screen, self.WIDGET_BG_COLOR, rect)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, rect, 2)
        
        # Draw title
        title_surface = self.font.render(title, True, self.TEXT_COLOR)
        title_rect = title_surface.get_rect(centerx=rect.centerx, top=rect.top + 20)
        self.screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_font = pygame.font.Font(None, 18)
        subtitle_surface = subtitle_font.render(subtitle, True, (120, 120, 120))
        subtitle_rect = subtitle_surface.get_rect(centerx=rect.centerx, top=title_rect.bottom + 10)
        self.screen.blit(subtitle_surface, subtitle_rect)
        
    def run(self):
        """Run the main application loop."""
        self.running = True
        logger.info("Starting main loop")
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
            
        logger.info("Main loop ended")
        self.quit()
        
    def quit(self):
        """Clean up and quit the application."""
        pygame.quit()
        logger.info("Application quit")
    
    def _update_layout(self):
        """Recalculate widget positions based on current window size."""
        # Simple responsive layout - adjust as needed
        margin = 50
        sim_size = min(self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT - 2*margin)
        
        self.SIMULATION_RECT = pygame.Rect(margin, margin, sim_size, sim_size)
        self.PERIODIC_TABLE_RECT = pygame.Rect(
            sim_size + 2*margin, margin, 
            self.WINDOW_WIDTH - sim_size - 3*margin, self.WINDOW_HEIGHT/2
        )
        self.CONTROLS_RECT = pygame.Rect(
            sim_size + 2*margin, self.WINDOW_HEIGHT/2 + 2*margin,
            self.WINDOW_WIDTH - sim_size - 3*margin, self.WINDOW_HEIGHT/2 - 3*margin
        )

        # Update widget rects if they exist
        if self.periodic_table_widget:
            self.periodic_table_widget.set_rect(self.PERIODIC_TABLE_RECT)
        if self.simulation_widget:
            self.simulation_widget.set_rect(self.SIMULATION_RECT)
        if self.controls_widget:
            self.controls_widget.set_rect(self.CONTROLS_RECT)


def main():
    """Entry point for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app = MDApplication(fps=30)
    app.run()
    sys.exit()


if __name__ == "__main__":
    main()