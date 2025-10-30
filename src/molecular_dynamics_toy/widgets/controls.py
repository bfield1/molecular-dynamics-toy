"""Controls widget for simulation parameters."""

import logging
import pygame
from typing import Tuple

from molecular_dynamics_toy.data import colors

logger = logging.getLogger(__name__)


class PlayPauseButton:
    """A button that toggles between play and pause states.
    
    Attributes:
        rect: Rectangle defining button position and size.
        playing: True if in play state, False if paused.
    """
    
    # Colors
    BG_COLOR = colors.CONTROL_BG_COLOR
    BG_HOVER_COLOR = colors.CONTROL_BG_HOVER_COLOR
    BORDER_COLOR = colors.CONTROL_BORDER_COLOR
    ICON_COLOR = colors.CONTROL_ICON_COLOR
    
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


class ResetButton:
    """A button that resets the simulation.
    
    Attributes:
        rect: Rectangle defining button position and size.
        hovered: Whether mouse is currently over this button.
    """
    
    # Colors
    BG_COLOR = colors.CONTROL_BG_COLOR
    BG_HOVER_COLOR = colors.CONTROL_BG_HOVER_COLOR
    BORDER_COLOR = colors.CONTROL_BORDER_COLOR
    ICON_COLOR = (200, 50, 50)  # Reddish for reset
    
    def __init__(self, rect: pygame.Rect):
        """Initialize the reset button.
        
        Args:
            rect: Rectangle defining position and size.
        """
        self.rect = rect
        self.hovered = False
        
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Check if position is inside button and handle click.
        
        Args:
            pos: Mouse position (x, y).
            
        Returns:
            True if button was clicked.
        """
        if self.rect.collidepoint(pos):
            logger.info("Reset button clicked")
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
        
        # Draw X icon (two diagonal lines)
        icon_rect = self.rect.inflate(-20, -20)  # Padding
        
        # Top-left to bottom-right
        pygame.draw.line(
            surface,
            self.ICON_COLOR,
            (icon_rect.left, icon_rect.top),
            (icon_rect.right, icon_rect.bottom),
            3
        )
        
        # Top-right to bottom-left
        pygame.draw.line(
            surface,
            self.ICON_COLOR,
            (icon_rect.right, icon_rect.top),
            (icon_rect.left, icon_rect.bottom),
            3
        )


class SpeedControl:
    """A control for adjusting simulation speed (steps per frame).
    
    Attributes:
        rect: Rectangle defining control position and size.
        speed: Number of MD steps per frame (minimum 1).
    """
    
    # Colors
    BG_COLOR = colors.CONTROL_BG_COLOR
    BG_HOVER_COLOR = colors.CONTROL_BG_HOVER_COLOR
    BORDER_COLOR = colors.CONTROL_BORDER_COLOR
    ICON_COLOR = colors.CONTROL_ICON_COLOR
    TEXT_COLOR = colors.TEXT_COLOR
    
    def __init__(self, rect: pygame.Rect, initial_speed: int = 1):
        """Initialize the speed control.
        
        Args:
            rect: Rectangle defining position and size.
            initial_speed: Initial speed value (steps per frame).
        """
        self.rect = rect
        self.speed = max(1, initial_speed)
        
        # Calculate sub-component rects
        button_width = rect.height  # Square buttons
        text_width = rect.width - 2 * button_width
        
        self.decrease_button_rect = pygame.Rect(
            rect.left, rect.top, button_width, rect.height
        )
        self.text_rect = pygame.Rect(
            rect.left + button_width, rect.top, text_width, rect.height
        )
        self.increase_button_rect = pygame.Rect(
            rect.right - button_width, rect.top, button_width, rect.height
        )
        
        self.decrease_hovered = False
        self.increase_hovered = False
        
        self.font = pygame.font.Font(None, 28)
        
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Check if position is inside control and handle click.
        
        Args:
            pos: Mouse position (x, y).
            
        Returns:
            True if control was clicked.
        """
        if self.decrease_button_rect.collidepoint(pos):
            self.speed = max(1, self.speed - 1)
            logger.info(f"Speed decreased to {self.speed}")
            return True
        elif self.increase_button_rect.collidepoint(pos):
            self.speed += 1
            logger.info(f"Speed increased to {self.speed}")
            return True
        return False
        
    def handle_hover(self, pos: Tuple[int, int]):
        """Update hover state based on mouse position.
        
        Args:
            pos: Mouse position (x, y).
        """
        self.decrease_hovered = self.decrease_button_rect.collidepoint(pos)
        self.increase_hovered = self.increase_button_rect.collidepoint(pos)
        
    def render(self, surface: pygame.Surface):
        """Render the control.
        
        Args:
            surface: Surface to render onto.
        """
        # Draw decrease button (rewind symbol: <<)
        bg_color = self.BG_HOVER_COLOR if self.decrease_hovered else self.BG_COLOR
        pygame.draw.rect(surface, bg_color, self.decrease_button_rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.decrease_button_rect, 2)
        
        # Draw double left triangles
        icon_rect = self.decrease_button_rect.inflate(-16, -16)
        mid_x = icon_rect.centerx
        # Left triangle
        left_triangle = [
            (mid_x - 8, icon_rect.top),
            (mid_x - 8, icon_rect.bottom),
            (icon_rect.left, icon_rect.centery)
        ]
        # Right triangle
        right_triangle = [
            (mid_x + 2, icon_rect.top),
            (mid_x + 2, icon_rect.bottom),
            (mid_x - 6, icon_rect.centery)
        ]
        pygame.draw.polygon(surface, self.ICON_COLOR, left_triangle)
        pygame.draw.polygon(surface, self.ICON_COLOR, right_triangle)
        
        # Draw text box with speed value
        pygame.draw.rect(surface, colors.WIDGET_BG_COLOR, self.text_rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.text_rect, 2)
        
        text_surface = self.font.render(str(self.speed), True, self.TEXT_COLOR)
        text_pos = text_surface.get_rect(center=self.text_rect.center)
        surface.blit(text_surface, text_pos)
        
        # Draw increase button (fast forward symbol: >>)
        bg_color = self.BG_HOVER_COLOR if self.increase_hovered else self.BG_COLOR
        pygame.draw.rect(surface, bg_color, self.increase_button_rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.increase_button_rect, 2)
        
        # Draw double right triangles
        icon_rect = self.increase_button_rect.inflate(-16, -16)
        mid_x = icon_rect.centerx
        # Left triangle
        left_triangle = [
            (mid_x - 2, icon_rect.top),
            (mid_x - 2, icon_rect.bottom),
            (mid_x + 6, icon_rect.centery)
        ]
        # Right triangle
        right_triangle = [
            (mid_x + 8, icon_rect.top),
            (mid_x + 8, icon_rect.bottom),
            (icon_rect.right, icon_rect.centery)
        ]
        pygame.draw.polygon(surface, self.ICON_COLOR, left_triangle)
        pygame.draw.polygon(surface, self.ICON_COLOR, right_triangle)

class TemperatureSlider:
    """A slider control for adjusting simulation temperature.
    
    Attributes:
        rect: Rectangle defining control position and size.
        temperature: Temperature in Kelvin.
        min_temp: Minimum temperature.
        max_temp: Maximum temperature.
        dragging: Whether slider is currently being dragged.
    """
    
    # Colors
    BG_COLOR = colors.CONTROL_BG_COLOR
    TRACK_COLOR = (180, 180, 180)
    SLIDER_COLOR = (100, 100, 100)
    SLIDER_HOVER_COLOR = (70, 70, 70)
    TEXT_COLOR = colors.TEXT_COLOR
    
    def __init__(self, rect: pygame.Rect, initial_temp: float = 300.0, 
                 min_temp: float = 0.0, max_temp: float = 1000.0):
        """Initialize the temperature slider.
        
        Args:
            rect: Rectangle defining position and size.
            initial_temp: Initial temperature in Kelvin.
            min_temp: Minimum temperature in Kelvin.
            max_temp: Maximum temperature in Kelvin.
        """
        self.rect = rect
        self.temperature = initial_temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.dragging = False
        self.hovered = False
        
        # Layout
        self.label_height = 25
        self.slider_height = 20
        self.slider_width = 15
        
        self.font = pygame.font.Font(None, 22)
        
    def _get_track_rect(self) -> pygame.Rect:
        """Get the rectangle for the slider track."""
        margin = 10
        return pygame.Rect(
            self.rect.left + margin,
            self.rect.top + self.label_height + 10,
            self.rect.width - 2 * margin,
            self.slider_height
        )
        
    def _get_slider_rect(self) -> pygame.Rect:
        """Get the rectangle for the slider handle."""
        track_rect = self._get_track_rect()
        
        # Calculate slider position based on temperature
        normalized = (self.temperature - self.min_temp) / (self.max_temp - self.min_temp)
        normalized = max(0.0, min(1.0, normalized))  # Clamp to [0, 1]
        
        slider_x = track_rect.left + normalized * (track_rect.width - self.slider_width)
        slider_y = track_rect.centery - self.slider_height // 2
        
        return pygame.Rect(slider_x, slider_y, self.slider_width, self.slider_height)
        
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Check if position is inside slider and start dragging.
        
        Args:
            pos: Mouse position (x, y).
            
        Returns:
            True if slider was clicked.
        """
        slider_rect = self._get_slider_rect()
        if slider_rect.collidepoint(pos):
            self.dragging = True
            return True
        
        # Also allow clicking on track to jump to position
        track_rect = self._get_track_rect()
        if track_rect.collidepoint(pos):
            self._update_from_position(pos[0])
            self.dragging = True
            return True
            
        return False
        
    def handle_release(self):
        """Handle mouse button release."""
        self.dragging = False
        
    def handle_drag(self, pos: Tuple[int, int]):
        """Handle mouse drag to update slider position.
        
        Args:
            pos: Mouse position (x, y).
        """
        if self.dragging:
            self._update_from_position(pos[0])
            
    def _update_from_position(self, x: int):
        """Update temperature based on x position.
        
        Args:
            x: X coordinate on screen.
        """
        track_rect = self._get_track_rect()
        
        # Convert x position to normalized value [0, 1]
        normalized = (x - track_rect.left) / track_rect.width
        normalized = max(0.0, min(1.0, normalized))
        
        # Convert to temperature
        old_temp = self.temperature
        self.temperature = self.min_temp + normalized * (self.max_temp - self.min_temp)
        
        if abs(self.temperature - old_temp) > 0.5:  # Log only significant changes
            logger.debug(f"Temperature set to {self.temperature:.1f} K")
            
    def handle_hover(self, pos: Tuple[int, int]):
        """Update hover state based on mouse position.
        
        Args:
            pos: Mouse position (x, y).
        """
        slider_rect = self._get_slider_rect()
        self.hovered = slider_rect.collidepoint(pos)
        
    def render(self, surface: pygame.Surface):
        """Render the slider.
        
        Args:
            surface: Surface to render onto.
        """
        # Draw label
        label_text = f"Temperature: {self.temperature:.0f} K"
        label_surface = self.font.render(label_text, True, self.TEXT_COLOR)
        label_rect = label_surface.get_rect(
            left=self.rect.left + 10,
            top=self.rect.top + 5
        )
        surface.blit(label_surface, label_rect)
        
        # Draw track
        track_rect = self._get_track_rect()
        pygame.draw.rect(surface, self.TRACK_COLOR, track_rect)
        pygame.draw.rect(surface, colors.BORDER_COLOR, track_rect, 1)
        
        # Draw slider handle
        slider_rect = self._get_slider_rect()
        slider_color = self.SLIDER_HOVER_COLOR if (self.hovered or self.dragging) else self.SLIDER_COLOR
        pygame.draw.rect(surface, slider_color, slider_rect)
        pygame.draw.rect(surface, colors.BORDER_COLOR, slider_rect, 2)


class ControlsWidget:
    """Widget for simulation controls (play/pause, speed, temperature).
    
    Attributes:
        rect: Rectangle defining widget position and size.
        playing: True if simulation is playing, False if paused.
        reset_requested: True if reset button was clicked this frame.
        speed: Number of MD steps per frame.
        temperature: Target temperature in Kelvin.
    """
    
    BG_COLOR = colors.WIDGET_BG_COLOR
    
    def __init__(self, rect: pygame.Rect):
        """Initialize the controls widget.
        
        Args:
            rect: Rectangle defining widget position and size.
        """
        self.rect = rect
        self.play_pause_button = None
        self.reset_button = None
        self.speed_control = None
        self.temperature_slider = None
        self.reset_requested = False
        
        self._create_controls()
        logger.info("ControlsWidget initialized")
        
    def _create_controls(self):
        """Create control elements."""
        # Preserve state if recreating
        old_playing = self.play_pause_button.playing if self.play_pause_button else False
        old_speed = self.speed_control.speed if self.speed_control else 1
        old_temp = self.temperature_slider.temperature if self.temperature_slider else 300.0
        
        margin = 20
        button_size = 60
        spacing = 10
        
        # Create play/pause button
        play_button_rect = pygame.Rect(
            self.rect.left + margin,
            self.rect.top + margin,
            button_size,
            button_size
        )
        self.play_pause_button = PlayPauseButton(play_button_rect)
        self.play_pause_button.playing = old_playing
        
        # Create reset button
        reset_button_rect = pygame.Rect(
            self.rect.left + margin + button_size + spacing,
            self.rect.top + margin,
            button_size,
            button_size
        )
        self.reset_button = ResetButton(reset_button_rect)
        
        # Create speed control
        speed_control_width = 200
        speed_control_rect = pygame.Rect(
            self.rect.left + margin + 2 * (button_size + spacing),
            self.rect.top + margin,
            speed_control_width,
            button_size
        )
        self.speed_control = SpeedControl(speed_control_rect, initial_speed=old_speed)
        
        # Create temperature slider
        slider_top = self.rect.top + margin + button_size + spacing
        slider_rect = pygame.Rect(
            self.rect.left + margin,
            slider_top,
            self.rect.width - 2 * margin,
            60
        )
        self.temperature_slider = TemperatureSlider(slider_rect, initial_temp=old_temp)
        
    @property
    def playing(self) -> bool:
        """Get current play/pause state."""
        return self.play_pause_button.playing if self.play_pause_button else False
        
    @property
    def speed(self) -> int:
        """Get current speed (steps per frame)."""
        return self.speed_control.speed if self.speed_control else 1
        
    @property
    def temperature(self) -> float:
        """Get current temperature in Kelvin."""
        return self.temperature_slider.temperature if self.temperature_slider else 300.0
        
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events.
        
        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.play_pause_button:
                    self.play_pause_button.handle_click(event.pos)
                if self.reset_button:
                    if self.reset_button.handle_click(event.pos):
                        self.reset_requested = True
                if self.speed_control:
                    self.speed_control.handle_click(event.pos)
                if self.temperature_slider:
                    self.temperature_slider.handle_click(event.pos)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                if self.temperature_slider:
                    self.temperature_slider.handle_release()
                    
        elif event.type == pygame.MOUSEMOTION:
            if self.play_pause_button:
                self.play_pause_button.handle_hover(event.pos)
            if self.reset_button:
                self.reset_button.handle_hover(event.pos)
            if self.speed_control:
                self.speed_control.handle_hover(event.pos)
            if self.temperature_slider:
                self.temperature_slider.handle_hover(event.pos)
                self.temperature_slider.handle_drag(event.pos)
                
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
        if self.reset_button:
            self.reset_button.render(surface)
        if self.speed_control:
            self.speed_control.render(surface)
        if self.temperature_slider:
            self.temperature_slider.render(surface)
            
    def set_rect(self, rect: pygame.Rect):
        """Update widget position and size, recalculating control positions.
        
        Args:
            rect: New rectangle defining widget position and size.
        """
        self.rect = rect
        self._create_controls()
        logger.debug(f"ControlsWidget resized to {rect}")