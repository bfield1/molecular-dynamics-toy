"""Tests for the GUI application and widgets."""

import pytest
import pygame
from molecular_dynamics_toy.app import MDApplication


@pytest.fixture
def pygame_init():
    """Initialize and cleanup pygame for tests."""
    pygame.init()
    yield
    pygame.quit()


def test_application_initialization(pygame_init):
    """Test that MDApplication initializes without crashing."""
    app = MDApplication(fps=30, calculator="mock")

    assert app.screen is not None
    assert app.clock is not None
    assert app.fps == 30
    assert app.running is False  # Not started yet


def test_application_has_correct_dimensions(pygame_init):
    """Test that application window has expected dimensions."""
    app = MDApplication(calculator="mock")

    assert app.WINDOW_WIDTH == 1400
    assert app.WINDOW_HEIGHT == 800
    assert app.screen.get_width() == 1400
    assert app.screen.get_height() == 800
