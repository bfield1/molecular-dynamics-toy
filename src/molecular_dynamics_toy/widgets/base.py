"""Base widget classes for common UI elements."""

import logging
import pygame
from typing import Tuple, Callable, Optional, List
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


class MenuItem(TextButton):
    """A menu item button.
    
    Just a specialized TextButton with menu-appropriate styling.
    """
    
    # Menu item specific colors
    BG_COLOR = colors.MENU_ITEM_BG_COLOR
    BG_HOVER_COLOR = colors.MENU_ITEM_BG_HOVER_COLOR
    BORDER_COLOR = colors.MENU_ITEM_BORDER_COLOR
    TEXT_COLOR = colors.TEXT_COLOR
    
    def __init__(self, rect: pygame.Rect, text: str, 
                 callback: Optional[Callable[[], None]] = None):
        """Initialize menu item.
        
        Args:
            rect: Rectangle defining position and size.
            text: Text to display.
            callback: Function to call when clicked.
        """
        super().__init__(rect, text, callback=callback, font_size=22)


class CloseButton(Button):
    """A close button with an X icon."""
    
    ICON_COLOR = colors.ICON_RESET_COLOR
    
    def __init__(self, rect: pygame.Rect):
        """Initialize close button.
        
        Args:
            rect: Rectangle defining position and size.
        """
        super().__init__(rect)
        
    def render_content(self, surface: pygame.Surface):
        """Render X icon.
        
        Args:
            surface: Surface to render onto.
        """
        icon_rect = self.rect.inflate(-12, -12)
        
        # Draw X (two diagonal lines)
        pygame.draw.line(
            surface,
            self.ICON_COLOR,
            (icon_rect.left, icon_rect.top),
            (icon_rect.right, icon_rect.bottom),
            3
        )
        pygame.draw.line(
            surface,
            self.ICON_COLOR,
            (icon_rect.right, icon_rect.top),
            (icon_rect.left, icon_rect.bottom),
            3
        )


class Menu:
    """Base class for popup menus.
    
    Provides a popup menu with a list of items and optional close button.
    Handles layout, rendering, and event handling for menu items.
    
    Attributes:
        rect: Rectangle defining menu position and size.
        items: List of menu items.
        visible: Whether menu is currently visible.
        close_on_outside_click: Whether to close when clicking outside menu.
        show_close_button: Whether to show the close button.
        auto_close_on_select: Whether to close menu when item is clicked.
    """
    
    # Menu styling
    BG_COLOR = colors.MENU_BG_COLOR
    BORDER_COLOR = colors.MENU_BORDER_COLOR
    TITLE_COLOR = colors.TEXT_COLOR
    
    def __init__(self, rect: pygame.Rect, title: str = "Menu",
                 show_close_button: bool = True,
                 close_on_outside_click: bool = True,
                 auto_close_on_select: bool = True):
        """Initialize the menu.
        
        Args:
            rect: Rectangle defining menu position and size.
            title: Title text to display at top of menu.
            show_close_button: Whether to show close button.
            close_on_outside_click: Whether clicking outside closes menu.
            auto_close_on_select: Whether clicking menu item closes menu.
        """
        self.rect = rect
        self.title = title
        self.visible = False
        self.show_close_button = show_close_button
        self.close_on_outside_click = close_on_outside_click
        self.auto_close_on_select = auto_close_on_select
        
        # Layout parameters
        self.title_height = 40
        self.item_height = 35
        self.item_spacing = 5
        self.margin = 15
        
        # Close button
        self.close_button = None
        if self.show_close_button:
            close_size = 30
            self.close_button = CloseButton(
                pygame.Rect(
                    rect.right - close_size - 10,
                    rect.top + 10,
                    close_size,
                    close_size
                )
            )
        
        self.items: List[MenuItem] = []
        self.title_font = pygame.font.Font(None, 28)
        
    def open(self):
        """Open the menu."""
        self.visible = True
        logger.info(f"Menu '{self.title}' opened")
        
    def close(self):
        """Close the menu."""
        self.visible = False
        logger.info(f"Menu '{self.title}' closed")
        
    def toggle(self):
        """Toggle menu visibility."""
        if self.visible:
            self.close()
        else:
            self.open()
    
    def set_position(self, x: int, y: int):
        """Set menu position and update all sub-components.
        
        Args:
            x: New x coordinate for top-left corner.
            y: New y coordinate for top-left corner.
        """
        # Calculate offset
        dx = x - self.rect.left
        dy = y - self.rect.top
        
        # Move main rect
        self.rect.topleft = (x, y)
        
        # Move close button
        if self.close_button:
            self.close_button.rect.move_ip(dx, dy)
            
        # Move all menu items
        for item in self.items:
            item.rect.move_ip(dx, dy)
            
    def center(self, width: int, height: int):
        """Center menu in a window of given dimensions.
        
        Args:
            width: Window width.
            height: Window height.
        """
        new_x = (width - self.rect.width) // 2
        new_y = (height - self.rect.height) // 2
        self.set_position(new_x, new_y)

    def add_item(self, text: str, callback: Optional[Callable[[], None]] = None):
        """Add a menu item.
        
        Args:
            text: Item text.
            callback: Function to call when item is clicked.
        """
        # Calculate position for new item
        items_top = self.rect.top + self.title_height + self.margin
        item_y = items_top + len(self.items) * (self.item_height + self.item_spacing)
        
        item_rect = pygame.Rect(
            self.rect.left + self.margin,
            item_y,
            self.rect.width - 2 * self.margin,
            self.item_height
        )
        
        # Optionally wrap callback to auto-close menu after action
        if self.auto_close_on_select and callback:
            original_callback = callback
            def wrapped_callback():
                original_callback()
                self.close()
            final_callback = wrapped_callback
        else:
            final_callback = callback
        
        item = MenuItem(item_rect, text, callback=final_callback)
        self.items.append(item)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame events.
        
        Args:
            event: Pygame event to process.
            
        Returns:
            True if event was handled by menu (prevents propagation).
        """
        if not self.visible:
            return False
            
        # Menu is visible - consume all mouse events to prevent interaction with widgets behind it
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check close button
                if self.close_button and self.close_button.handle_click(event.pos):
                    self.close()
                    return True
                    
                # Check menu items
                for item in self.items:
                    if item.handle_click(event.pos):
                        return True
                        
                # Check if click is inside menu area
                if self.rect.collidepoint(event.pos):
                    # Click inside menu but not on any item - consume event
                    return True
                elif self.close_on_outside_click:
                    # Click outside menu - close it
                    self.close()
                    return True
                    
        elif event.type == pygame.MOUSEMOTION:
            # Update hover states only for menu elements
            if self.close_button:
                self.close_button.handle_hover(event.pos)
            for item in self.items:
                item.handle_hover(event.pos)
                
        # Consume all mouse events when menu is visible
        #return True
        return False
        
    def render(self, surface: pygame.Surface):
        """Render the menu.
        
        Args:
            surface: Surface to render onto.
        """
        if not self.visible:
            return
            
        # Draw semi-transparent overlay behind menu
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(100)
        overlay.fill(colors.MENU_OVERLAY_COLOR)
        surface.blit(overlay, (0, 0))
        
        # Draw menu background
        pygame.draw.rect(surface, self.BG_COLOR, self.rect)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.rect, 3)
        
        # Draw title
        title_surface = self.title_font.render(self.title, True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(
            centerx=self.rect.centerx,
            top=self.rect.top + 10
        )
        surface.blit(title_surface, title_rect)
        
        # Draw separator line under title
        separator_y = self.rect.top + self.title_height
        pygame.draw.line(
            surface,
            self.BORDER_COLOR,
            (self.rect.left + 10, separator_y),
            (self.rect.right - 10, separator_y),
            2
        )
        
        # Draw close button
        if self.close_button:
            self.close_button.render(surface)
        
        # Draw menu items
        for item in self.items:
            item.render(surface)