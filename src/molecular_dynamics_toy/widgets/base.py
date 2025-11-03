"""Base widget classes for common UI elements."""

import logging
import pygame
from typing import Tuple, Callable, Optional
from molecular_dynamics_toy.data import colors

logger = logging.getLogger(__name__)


class Button:
    """A base class for clickable buttons with hover effects.
    
    Provides common functionality for rectangular buttons with background,
    border, and hover states. Subclasses can override rendering methods
    to customize appearance.
    
    Attributes:
        rect: Rectangle defining button position and size.
        hovered: Whether mouse is currently over the button.
        enabled: Whether button can be clicked.
        callback: Optional function to call when button is clicked.
    """
    
    # Default colors (can be overridden by subclasses)
    BG_COLOR = colors.CONTROL_BG_COLOR
    BG_HOVER_COLOR = colors.CONTROL_BG_HOVER_COLOR
    BG_DISABLED_COLOR = colors.BUTTON_BG_DISABLED_COLOR
    BORDER_COLOR = colors.CONTROL_BORDER_COLOR
    BORDER_DISABLED_COLOR = colors.BUTTON_BORDER_DISABLED_COLOR
    
    def __init__(self, rect: pygame.Rect, callback: Optional[Callable[[], None]] = None,
                 enabled: bool = True):
        """Initialize the button.
        
        Args:
            rect: Rectangle defining position and size.
            callback: Optional function to call when clicked.
            enabled: Whether button starts enabled.
        """
        self.rect = rect
        self.hovered = False
        self.enabled = enabled
        self.callback = callback
        
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Check if position is inside button and handle click.
        
        Args:
            pos: Mouse position (x, y).
            
        Returns:
            True if button was clicked.
        """
        if not self.enabled:
            return False
            
        if self.rect.collidepoint(pos):
            self.on_click()
            if self.callback:
                self.callback()
            return True
        return False
        
    def handle_hover(self, pos: Tuple[int, int]):
        """Update hover state based on mouse position.
        
        Args:
            pos: Mouse position (x, y).
        """
        self.hovered = self.rect.collidepoint(pos) and self.enabled
        
    def on_click(self):
        """Handle click event. Override in subclasses for custom behavior."""
        pass
        
    def render(self, surface: pygame.Surface):
        """Render the button.
        
        Args:
            surface: Surface to render onto.
        """
        # Determine colors based on state
        if not self.enabled:
            bg_color = self.BG_DISABLED_COLOR
            border_color = self.BORDER_DISABLED_COLOR
        elif self.hovered:
            bg_color = self.BG_HOVER_COLOR
            border_color = self.BORDER_COLOR
        else:
            bg_color = self.BG_COLOR
            border_color = self.BORDER_COLOR
        
        # Draw background
        pygame.draw.rect(surface, bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Draw content (override in subclasses)
        self.render_content(surface)
        
    def render_content(self, surface: pygame.Surface):
        """Render button content (icon, text, etc.). Override in subclasses.
        
        Args:
            surface: Surface to render onto.
        """
        pass


class ToggleButton(Button):
    """A button that toggles between two states when clicked.
    
    Automatically swaps colors based on toggle state. Subclasses can define
    separate colors for selected/unselected states.
    
    Attributes:
        selected: Whether button is currently selected/toggled on.
    """
    
    # Colors for unselected state (inherited from Button)
    BG_COLOR = colors.CONTROL_BG_COLOR
    BG_HOVER_COLOR = colors.CONTROL_BG_HOVER_COLOR
    BORDER_COLOR = colors.CONTROL_BORDER_COLOR
    
    # Colors for selected state
    BG_SELECTED_COLOR = colors.ELEMENT_BG_SELECTED_COLOR
    BG_SELECTED_HOVER_COLOR = colors.ELEMENT_BG_SELECTED_HOVER_COLOR
    BORDER_SELECTED_COLOR = colors.ELEMENT_BORDER_SELECTED_COLOR
    
    def __init__(self, rect: pygame.Rect, callback: Optional[Callable[[], None]] = None,
                 enabled: bool = True, selected: bool = False):
        """Initialize the toggle button.
        
        Args:
            rect: Rectangle defining position and size.
            callback: Optional function to call when clicked.
            enabled: Whether button starts enabled.
            selected: Whether button starts selected.
        """
        super().__init__(rect, callback, enabled)
        self.selected = selected
        
    def on_click(self):
        """Toggle selected state when clicked."""
        self.selected = not self.selected
        
    def render(self, surface: pygame.Surface):
        """Render the button with state-dependent colors.
        
        Args:
            surface: Surface to render onto.
        """
        # Determine colors based on state
        if not self.enabled:
            bg_color = self.BG_DISABLED_COLOR
            border_color = self.BORDER_DISABLED_COLOR
        elif self.selected and self.hovered:
            bg_color = self.BG_SELECTED_HOVER_COLOR
            border_color = self.BORDER_SELECTED_COLOR
        elif self.selected:
            bg_color = self.BG_SELECTED_COLOR
            border_color = self.BORDER_SELECTED_COLOR
        elif self.hovered:
            bg_color = self.BG_HOVER_COLOR
            border_color = self.BORDER_COLOR
        else:
            bg_color = self.BG_COLOR
            border_color = self.BORDER_COLOR
        
        # Draw background
        pygame.draw.rect(surface, bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Draw content (override in subclasses)
        self.render_content(surface)


class TextButton(Button):
    """A button that displays text.
    
    Attributes:
        text: Text to display on the button.
    """
    
    TEXT_COLOR = colors.TEXT_COLOR
    TEXT_HOVER_COLOR = colors.TEXT_COLOR
    TEXT_DISABLED_COLOR = colors.TEXT_DISABLED_COLOR
    
    def __init__(self, rect: pygame.Rect, text: str, 
                 callback: Optional[Callable[[], None]] = None,
                 enabled: bool = True, font_size: int = 20):
        """Initialize the text button.
        
        Args:
            rect: Rectangle defining position and size.
            text: Text to display.
            callback: Optional function to call when clicked.
            enabled: Whether button starts enabled.
            font_size: Font size for the text.
        """
        super().__init__(rect, callback, enabled)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        
    def render_content(self, surface: pygame.Surface):
        """Render the text content.
        
        Args:
            surface: Surface to render onto.
        """
        # Choose text color based on state
        if not self.enabled:
            text_color = self.TEXT_DISABLED_COLOR
        elif self.hovered:
            text_color = self.TEXT_HOVER_COLOR
        else:
            text_color = self.TEXT_COLOR
            
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)