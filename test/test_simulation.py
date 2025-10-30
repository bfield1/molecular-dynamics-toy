"""Tests for the simulation widget."""

import pytest
import pygame
import numpy as np
from molecular_dynamics_toy.widgets.simulation import SimulationWidget
from molecular_dynamics_toy.calculators import get_calculator


@pytest.fixture
def pygame_init():
    """Initialize and cleanup pygame for tests."""
    pygame.init()
    yield
    pygame.quit()


def test_simulation_widget_initialization(pygame_init):
    """Test that SimulationWidget initializes correctly."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc)
    
    assert widget.rect == rect
    assert widget.engine is not None
    assert widget.calculator is calc
    assert widget.radius_type == "covalent"


def test_simulation_widget_update_when_paused(pygame_init):
    """Test that simulation doesn't advance when paused."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc)
    
    initial_positions = widget.engine.atoms.get_positions().copy()
    
    # Update with playing=False
    widget.update(playing=False)
    
    final_positions = widget.engine.atoms.get_positions()
    np.testing.assert_array_equal(initial_positions, final_positions)


def test_simulation_widget_update_when_playing(pygame_init):
    """Test that simulation advances when playing."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc)
    
    # Add an atom
    widget.engine.add_atom("H", [2,2,2])
    widget.engine.add_atom("H", [2,3,2])
    initial_positions = widget.engine.atoms.get_positions().copy()
    
    # Update with playing=True
    widget.update(playing=True)
    
    final_positions = widget.engine.atoms.get_positions()
    
    # Positions should have changed (atoms have velocities from temperature)
    assert not np.array_equal(initial_positions, final_positions)


def test_simulation_widget_covalent_radii(pygame_init):
    """Test that widget can use covalent radii."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc, radius_type="covalent")
    
    assert widget.radius_type == "covalent"
    
    # Check that covalent radii are generally smaller
    from molecular_dynamics_toy.data.atom_properties import ATOM_VDW_RADII, ATOM_COVALENT_RADII
    assert ATOM_COVALENT_RADII['H'] < ATOM_VDW_RADII['H']
    assert widget.atom_radii['H'] == ATOM_COVALENT_RADII['H']


def test_simulation_widget_vdw_radii_default(pygame_init):
    """Test that widget defaults to van der Waals radii."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc, radius_type="vdw")
    
    from molecular_dynamics_toy.data.atom_properties import ATOM_VDW_RADII
    assert widget.atom_radii['H'] == ATOM_VDW_RADII['H']


def test_simulation_widget_resize(pygame_init):
    """Test that simulation widget can be resized."""
    rect1 = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect1, calculator=calc)
    
    rect2 = pygame.Rect(0, 0, 800, 800)
    widget.set_rect(rect2)
    
    assert widget.rect == rect2


def test_simulation_widget_get_cell_rect(pygame_init):
    """Test that cell rect is calculated correctly."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc)
    
    cell_rect = widget._get_cell_rect()
    
    # Cell should be square and centered with margin
    assert cell_rect.width == cell_rect.height
    assert cell_rect.width <= rect.width - 40  # 2*margin
    assert cell_rect.centerx == rect.centerx
    assert cell_rect.centery == rect.centery


def test_simulation_widget_render_doesnt_crash(pygame_init):
    """Test that rendering doesn't crash."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc)
    
    surface = pygame.Surface((700, 700))
    
    # Should not raise
    widget.render(surface)


def test_simulation_widget_handle_event(pygame_init):
    """Test that widget handles events without crashing."""
    rect = pygame.Rect(0, 0, 700, 700)
    calc = get_calculator("mock")
    widget = SimulationWidget(rect, calculator=calc)
    
    # Create a dummy event
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (100, 100)})
    
    # Should not raise (currently does nothing)
    widget.handle_event(event)