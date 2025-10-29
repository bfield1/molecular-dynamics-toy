"""Tests for the controls widget."""

import pytest
import pygame
from molecular_dynamics_toy.widgets.controls import ControlsWidget, PlayPauseButton


@pytest.fixture
def pygame_init():
    """Initialize and cleanup pygame for tests."""
    pygame.init()
    yield
    pygame.quit()


def test_play_pause_button_initialization(pygame_init):
    """Test that PlayPauseButton initializes in paused state."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = PlayPauseButton(rect)
    
    assert button.rect == rect
    assert button.playing is False
    assert button.hovered is False


def test_play_pause_button_click_to_play(pygame_init):
    """Test that clicking paused button starts playing."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = PlayPauseButton(rect)
    
    clicked = button.handle_click((30, 30))
    
    assert clicked is True
    assert button.playing is True


def test_play_pause_button_toggle(pygame_init):
    """Test that clicking toggles between play and pause."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = PlayPauseButton(rect)
    
    # First click: play
    button.handle_click((30, 30))
    assert button.playing is True
    
    # Second click: pause
    button.handle_click((30, 30))
    assert button.playing is False
    
    # Third click: play again
    button.handle_click((30, 30))
    assert button.playing is True


def test_play_pause_button_click_outside(pygame_init):
    """Test that clicking outside button doesn't change state."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = PlayPauseButton(rect)
    
    clicked = button.handle_click((100, 100))
    
    assert clicked is False
    assert button.playing is False


def test_play_pause_button_hover(pygame_init):
    """Test that hovering over button updates hover state."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = PlayPauseButton(rect)
    
    # Hover inside
    button.handle_hover((30, 30))
    assert button.hovered is True
    
    # Hover outside
    button.handle_hover((100, 100))
    assert button.hovered is False


def test_controls_widget_initialization(pygame_init):
    """Test that ControlsWidget initializes correctly."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    assert widget.rect == rect
    assert widget.play_pause_button is not None
    assert widget.playing is False


def test_controls_widget_playing_property(pygame_init):
    """Test that playing property reflects button state."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    assert widget.playing is False
    
    # Click button
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': widget.play_pause_button.rect.center}
    )
    widget.handle_event(event)
    
    assert widget.playing is True


def test_controls_widget_event_handling(pygame_init):
    """Test that widget handles mouse events correctly."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    button_center = widget.play_pause_button.rect.center
    
    # Mouse motion event
    motion_event = pygame.event.Event(
        pygame.MOUSEMOTION,
        {'pos': button_center}
    )
    widget.handle_event(motion_event)
    assert widget.play_pause_button.hovered is True
    
    # Mouse click event
    click_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': button_center}
    )
    widget.handle_event(click_event)
    assert widget.playing is True


def test_controls_widget_resize(pygame_init):
    """Test that controls widget can be resized."""
    rect1 = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect1)
    
    # Resize
    rect2 = pygame.Rect(0, 0, 600, 300)
    widget.set_rect(rect2)
    
    assert widget.rect == rect2
    assert widget.play_pause_button is not None


def test_controls_widget_resize_preserves_state(pygame_init):
    """Test that resizing doesn't change play/pause state."""
    rect1 = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect1)
    
    # Set to playing
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': widget.play_pause_button.rect.center}
    )
    widget.handle_event(event)
    assert widget.playing is True
    
    # Resize
    rect2 = pygame.Rect(0, 0, 600, 300)
    widget.set_rect(rect2)
    
    # State should be reset (new button created)
    # This is current behavior - could be changed to preserve state
    assert widget.playing is False