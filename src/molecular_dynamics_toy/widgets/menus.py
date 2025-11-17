"""Specialized menu widgets."""

import logging
import sys
import os.path
from typing import Optional, Callable
import webbrowser

import pygame

from molecular_dynamics_toy.widgets.base import Menu, TextBox
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


ABOUT_TEXT = """Molecular Dynamics Toy

A simple molecular dynamics simulation demo built with Python, Pygame, and ASE.

Features:
- Interactive atom placement
- Real-time MD simulation using MatterSim
- Multiple preset structures
- Adjustable simulation parameters

Version: 0.1.0
Author: Bernard Field
Copyright 2025 Bernard Field

Check for updates and see the source code on the website:
github.com/bfield1/molecular-dynamics-toy
"""


class MainMenu(Menu):
    """Main application menu.
    
    Provides access to application-level functions like About, Info, and Exit.
    """
    
    def __init__(self, rect: pygame.Rect, exit_callback: Optional[Callable[[], None]] = None,
                 force_show_third_party: Optional[bool] = False):
        """Initialize the main menu.
        
        Args:
            rect: Rectangle defining menu position and size.
            exit_callback: Function to call when Exit is selected.
            force_show_third_party: Shows the "Third Party Information" button,
                even in a package or development build.
                Note that it will likely not work if used in a package build,
                and may check outside the intended directory.
        """
        super().__init__(rect, title="Menu", auto_close_on_select=False)
        
        self.exit_callback = exit_callback

        about_rect = pygame.Rect(0, 0, 400, 500)
        self.about_textbox = TextBox(about_rect, title="About", text=ABOUT_TEXT)
        
        # Add menu items
        self.add_item("About", self._show_about)
        self.add_item("Website", self._open_website)
        if getattr(sys, "frozen", False) or force_show_third_party:
            # Only link to 3rd party info if using the bundled version of the app.
            self.add_item("Third Party Information", self._show_third_party_info)
        self.add_item("Exit", self._exit_application)
        
    def _show_about(self):
        """Show about dialog."""
        logger.info("Showing About dialog")
        self.about_textbox.open()
    
    def _open_website(self):
        """Open GitHub home-page"""
        URL = r"https://github.com/bfield1/molecular-dynamics-toy"
        logger.info(f"Opening {URL}")
        webbrowser.open(URL)
        
    def _show_third_party_info(self):
        """Show third party information in default web browser."""
        try:
            # Get the path to ThirdPartyNotices.html
            # When bundled with PyInstaller, files are in sys._MEIPASS
            if hasattr(sys, '_MEIPASS'):
                html_path = os.path.join(sys._MEIPASS, 'ThirdPartyNotices.html')
            else:
                # Development mode - look in project root or similar
                html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                        'ThirdPartyNotices.html')
            
            if os.path.exists(html_path):
                # Open in default web browser
                webbrowser.open('file://' + os.path.abspath(html_path))
                logger.info(f"Opened third party notices: {html_path}")
            else:
                logger.error(f"Third party notices file not found: {html_path}")
                
        except Exception as e:
            logger.error(f"Failed to open third party notices: {e}")
        
    def _exit_application(self):
        """Exit the application."""
        logger.info("Exit requested from menu")
        if self.exit_callback:
            self.exit_callback()