"""Simulation widget for rendering and controlling MD simulation."""

import logging
import pygame
import numpy as np
from typing import Optional

from ase import Atoms

from molecular_dynamics_toy.engine import MDEngine
from molecular_dynamics_toy.data import colors
from molecular_dynamics_toy.data.atom_properties import ATOM_COLORS, ATOM_VDW_RADII, ATOM_COVALENT_RADII

logger = logging.getLogger(__name__)


class SimulationWidget:
    """Widget for displaying and interacting with MD simulation.
    
    Attributes:
        rect: Rectangle defining widget position and size.
        engine: MD engine instance.
    """
    
    BG_COLOR = colors.WIDGET_BG_COLOR
    CELL_COLOR = colors.SIMULATION_CELL_COLOR
    
    def __init__(self, rect: pygame.Rect, calculator=None, radius_type: str = "covalent"):
        """Initialize the simulation widget.
        
        Args:
            rect: Rectangle defining widget position and size.
            calculator: ASE calculator for MD engine.
            radius_type: Type of atomic radii to use ('vdw' or 'covalent').
        """
        self.rect = rect
        self.engine = None
        self.calculator = calculator
        self.radius_type = radius_type

        # Select radii based on type
        self.atom_radii = ATOM_VDW_RADII if radius_type == "vdw" else ATOM_COVALENT_RADII
        
        # Scale factor for converting Angstroms to pixels
        # Gets overridden later.
        self.scale = 10.0  # pixels per Angstrom
        
        self._create_engine()
        logger.info("SimulationWidget initialized")
        
    def _create_engine(self):
        """Create MD engine with initial test configuration."""
        # Create engine with H2 molecule for testing
        cell_size = 10.0  # Angstroms
        self.engine = MDEngine(
            calculator=self.calculator,
            timestep=1.0,
            temperature=300.0,
            cell_size=cell_size
        )
        
        # Add H2 molecule in center of cell
        center = cell_size / 2
        self.engine.add_atom('H', [center - 0.5, center, center])
        self.engine.add_atom('H', [center + 0.5, center, center])
        
        logger.info("Created test H2 molecule")
        
    def update(self, playing: bool):
        """Update simulation state.
        
        Args:
            playing: Whether simulation should be running.
        """
        if playing and self.engine:
            try:
                self.engine.run(steps=1)
            except Exception as e:
                logger.error(f"MD step failed: {e}")
                
    def render(self, surface: pygame.Surface):
        """Render the simulation.
        
        Args:
            surface: Surface to render onto.
        """
        # Draw background
        pygame.draw.rect(surface, self.BG_COLOR, self.rect)
        
        # Draw simulation cell boundary
        cell_rect = self._get_cell_rect()
        pygame.draw.rect(surface, self.CELL_COLOR, cell_rect)
        pygame.draw.rect(surface, colors.BORDER_COLOR, cell_rect, 2)
        
        # Draw atoms
        if self.engine and len(self.engine.atoms) > 0:
            self._render_atoms(surface)
            
    def _get_cell_rect(self) -> pygame.Rect:
        """Get the rectangle for the simulation cell display.
        
        Returns:
            Rectangle for cell, centered in widget with some margin.
        """
        margin = 20
        max_size = min(self.rect.width, self.rect.height) - 2 * margin
        
        return pygame.Rect(
            self.rect.centerx - max_size // 2,
            self.rect.centery - max_size // 2,
            max_size,
            max_size
        )
        
    def _render_atoms(self, surface: pygame.Surface):
        """Render all atoms in the simulation.
        
        Args:
            surface: Surface to render onto.
        """
        positions = self.engine.atoms.get_positions()
        symbols = self.engine.atoms.get_chemical_symbols()
        cell_size = self.engine.atoms.cell[0, 0]  # Cubic cell
        
        cell_rect = self._get_cell_rect()
        
        # Calculate scale: cell_size (Angstroms) -> cell_rect size (pixels)
        self.scale = cell_rect.width / cell_size
        
        # Sort atoms by z-coordinate for proper depth rendering
        z_coords = positions[:, 2]
        draw_order = np.argsort(z_coords)
        
        for idx in draw_order:
            pos = positions[idx]
            symbol = symbols[idx]
            
            # Project 3D -> 2D (simple orthogonal projection, xy plane)
            screen_x = cell_rect.left + pos[0] * self.scale
            screen_y = cell_rect.top + pos[1] * self.scale
            
            # Get atom properties
            color = ATOM_COLORS[symbol]
            radius_angstrom = self.atom_radii[symbol]
            
            # Scale radius based on z-depth for pseudo-3D effect
            z_depth = pos[2] / cell_size  # Normalize to 0-1
            depth_scale = 0.7 + 0.3 * z_depth  # Farther = smaller
            radius_pixels = int(radius_angstrom * self.scale * depth_scale)
            
            # Adjust brightness based on depth
            brightness = 0.6 + 0.4 * z_depth
            adjusted_color = tuple(int(c * brightness) for c in color)
            
            # Draw atom as circle
            if radius_pixels > 0:
                pygame.draw.circle(
                    surface,
                    adjusted_color,
                    (int(screen_x), int(screen_y)),
                    radius_pixels
                )
                # Draw outline
                pygame.draw.circle(
                    surface,
                    tuple(max(0, c - 40) for c in adjusted_color),
                    (int(screen_x), int(screen_y)),
                    radius_pixels,
                    1
                )
                
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events.
        
        Args:
            event: Pygame event to process.
        """
        # TODO: Handle atom placement clicks
        pass
        
    def set_rect(self, rect: pygame.Rect):
        """Update widget position and size.
        
        Args:
            rect: New rectangle defining widget position and size.
        """
        self.rect = rect
        logger.debug(f"SimulationWidget resized to {rect}")