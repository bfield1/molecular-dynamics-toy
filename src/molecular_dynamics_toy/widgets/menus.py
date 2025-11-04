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