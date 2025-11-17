"""Specialized menu widgets."""

import logging
import pygame
from typing import Optional, Callable
from molecular_dynamics_toy.widgets.base import Menu
from molecular_dynamics_toy.data import presets

logger = logging.getLogger(__name__)


class PresetsMenu(Menu):
    """Menu for loading preset atomic configurations.
    
    Automatically populates with presets from data.presets module.
    """
    
    def __init__(self, rect: pygame.Rect, load_callback: Optional[Callable[[str], None]] = None):
        """Initialize the presets menu.
        
        Args:
            rect: Rectangle defining menu position and size.
            load_callback: Function to call when preset is selected.
                           Takes preset_id as argument.
        """
        super().__init__(rect, title="Load Preset", auto_close_on_select=True)
        
        self.load_callback = load_callback
        
        # Populate with presets
        for preset_id in presets.get_preset_names():
            display_name = presets.get_preset_display_name(preset_id)
            self.add_item(display_name, lambda pid=preset_id: self._load_preset(pid))
            
    def _load_preset(self, preset_id: str):
        """Load a preset configuration.
        
        Args:
            preset_id: Preset identifier.
        """
        logger.info(f"Loading preset: {preset_id}")
        
        if self.load_callback:
            self.load_callback(preset_id)


class MainMenu(Menu):
    """Main application menu.
    
    Provides access to application-level functions like About, Info, and Exit.
    """
    
    def __init__(self, rect: pygame.Rect, exit_callback: Optional[Callable[[], None]] = None):
        """Initialize the main menu.
        
        Args:
            rect: Rectangle defining menu position and size.
            exit_callback: Function to call when Exit is selected.
        """
        super().__init__(rect, title="Menu", auto_close_on_select=False)
        
        self.exit_callback = exit_callback
        
        # Add menu items
        self.add_item("About", self._show_about)
        self.add_item("Third Party Information", self._show_third_party_info)
        self.add_item("Exit", self._exit_application)
        
    def _show_about(self):
        """Show about dialog (not yet implemented)."""
        logger.info("About clicked (not implemented)")
        
    def _show_third_party_info(self):
        """Show third party information (not yet implemented)."""
        logger.info("Third Party Info clicked (not implemented)")
        
    def _exit_application(self):
        """Exit the application."""
        logger.info("Exit requested from menu")
        if self.exit_callback:
            self.exit_callback()