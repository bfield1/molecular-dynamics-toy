"""Tests for widgets.base."""

import pytest
import pygame
from molecular_dynamics_toy.widgets.base import TextButton

@pytest.fixture
def pygame_init():
    """Initialize and cleanup pygame for tests."""
    pygame.init()
    yield
    pygame.quit()


def test_text_button_initialization(pygame_init):
    """Test that TextButton initializes correctly."""
    rect = pygame.Rect(10, 10, 60, 30)
    button = TextButton(rect, "Test")
    
    assert button.rect == rect
    assert button.text == "Test"
    assert button.enabled is True
    assert button.hovered is False


def test_text_button_custom_font_size(pygame_init):
    """Test that TextButton can use custom font size."""
    rect = pygame.Rect(10, 10, 60, 30)
    button = TextButton(rect, "Test", font_size=24)
    
    assert button.font.get_height() > 0  # Font was created


def test_text_button_click(pygame_init):
    """Test that clicking text button works."""
    rect = pygame.Rect(10, 10, 60, 30)
    button = TextButton(rect, "Test")
    
    clicked = button.handle_click((30, 20))
    
    assert clicked is True


def test_text_button_with_callback(pygame_init):
    """Test that text button calls callback when clicked."""
    rect = pygame.Rect(10, 10, 60, 30)
    callback_called = []
    
    def callback():
        callback_called.append(True)
    
    button = TextButton(rect, "Test", callback=callback)
    button.handle_click((30, 20))
    
    assert len(callback_called) == 1


def test_text_button_disabled(pygame_init):
    """Test that disabled text button doesn't respond to clicks."""
    rect = pygame.Rect(10, 10, 60, 30)
    callback_called = []
    
    def callback():
        callback_called.append(True)
    
    button = TextButton(rect, "Test", callback=callback, enabled=False)
    clicked = button.handle_click((30, 20))
    
    assert clicked is False
    assert len(callback_called) == 0


def test_text_button_render(pygame_init):
    """Test that text button renders without crashing."""
    rect = pygame.Rect(10, 10, 60, 30)
    button = TextButton(rect, "Test")
    
    surface = pygame.Surface((100, 100))
    button.render(surface)  # Should not raise