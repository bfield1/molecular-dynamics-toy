"""Controls widget for simulation parameters."""

import logging
import pygame
from typing import Tuple

logger = logging.getLogger(__name__)


class PlayPauseButton:
    """A button that toggles between play and pause states.
    
    Attributes:
        rect: Rectangle defining button position and size.
        playing: True if in play state, False if paused.
    """
    
    # Colors
    BG_COLOR = (240, 240, 240)
    BG_HOVER_COLOR = (220, 220, 220)
    BORDER_COLOR = (180, 180, 180)
    ICON_COLOR = (50, 50, 50)
    
    def __init__(self, rect: pygame.Rect):
        """Initialize the play/pause button.
        
        Args:
            rect: Rectangle defining position and size.
        """
        self.rect = rect
        self.playing = False
        self.hovered = False
        
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Check if position is inside button and handle click.
        
        Args:
            pos: Mouse position (x, y).
            
        Returns:
            True if button was clicked.
        """
        if self.rect.collidepoint(pos):
            self.playing = not self.playing
            logger.info(f"Simulation {'playing' if self.playing else 'paused'}")
            return True
        return False
        
    def handle_hover(self, pos: Tuple[int, int]):
        """Update hover state based on mouse position.
        
        Args:
            pos: Mouse position (x, y).
        """
        self.hovered = self.rect.collidepoint(pos)
        
    def render(self, surface: pygame.Surface):
        """Render the button.
        
        Args:
            surface: Surface to render onto.
        """
        # Draw background
        bg_color = self.BG_HOVER_COLOR if self.hovered else self.BG_COLOR
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.rect, 2)
        
        # Draw icon (play triangle or pause bars)
        icon_rect = self.rect.inflate(-20, -20)  # Padding
        
        if self.playing:
            # Draw pause icon (two vertical bars)
            bar_width = icon_rect.width // 3
            bar_height = icon_rect.height
            left_bar = pygame.Rect(
                icon_rect.left,
                icon_rect.top,
                bar_width,
                bar_height
            )
            right_bar = pygame.Rect(
                icon_rect.right - bar_width,
                icon_rect.top,
                bar_width,
                bar_height
            )
            pygame.draw.rect(surface, self.ICON_COLOR, left_bar)
            pygame.draw.rect(surface, self.ICON_COLOR, right_bar)
        else:
            # Draw play icon (triangle pointing right)
            triangle_points = [
                (icon_rect.left, icon_rect.top),
                (icon_rect.left, icon_rect.bottom),
                (icon_rect.right, icon_rect.centery)
            ]
            pygame.draw.polygon(surface, self.ICON_COLOR, triangle_points)


class ControlsWidget:
    """Widget for simulation controls (play/pause, speed, temperature).
    
    Attributes:
        rect: Rectangle defining widget position and size.
        playing: True if simulation is playing, False if paused.
    """
    
    BG_COLOR = (255, 255, 255)
    
    def __init__(self, rect: pygame.Rect):
        """Initialize the controls widget.
        
        Args:
            rect: Rectangle defining widget position and size.
        """
        self.rect = rect
        self.play_pause_button = None
        
        self._create_controls()
        logger.info("ControlsWidget initialized")
        
    def _create_controls(self):
        """Create control elements."""
        margin = 20
        button_size = 60
        
        # Create play/pause button
        button_rect = pygame.Rect(
            self.rect.left + margin,
            self.rect.top + margin,
            button_size,
            button_size
        )
        self.play_pause_button = PlayPauseButton(button_rect)
        
    @property
    def playing(self) -> bool:
        """Get current play/pause state."""
        return self.play_pause_button.playing if self.play_pause_button else False
        
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events.
        
        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.play_pause_button:
                    self.play_pause_button.handle_click(event.pos)
                    
        elif event.type == pygame.MOUSEMOTION:
            if self.play_pause_button:
                self.play_pause_button.handle_hover(event.pos)
                
    def update(self):
        """Update widget state (called each frame)."""
        pass
        
    def render(self, surface: pygame.Surface):
        """Render the widget.
        
        Args:
            surface: Surface to render onto.
        """
        # Draw background
        pygame.draw.rect(surface, self.BG_COLOR, self.rect)
        
        # Draw controls
        if self.play_pause_button:
            self.play_pause_button.render(surface)
            
    def set_rect(self, rect: pygame.Rect):
        """Update widget position and size, recalculating control positions.
        
        Args:
            rect: New rectangle defining widget position and size.
        """
        self.rect = rect
        self._create_controls()
        logger.debug(f"ControlsWidget resized to {rect}")