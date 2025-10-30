"""Tests for the controls widget."""

import pytest
import pygame
from molecular_dynamics_toy.widgets.controls import ControlsWidget, PlayPauseButton, ResetButton, SpeedControl


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
    
    # State should be preserved
    assert widget.playing is True

def test_reset_button_initialization(pygame_init):
    """Test that ResetButton initializes correctly."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = ResetButton(rect)
    
    assert button.rect == rect
    assert button.hovered is False


def test_reset_button_click(pygame_init):
    """Test that clicking reset button returns True."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = ResetButton(rect)
    
    clicked = button.handle_click((30, 30))
    
    assert clicked is True


def test_reset_button_click_outside(pygame_init):
    """Test that clicking outside reset button returns False."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = ResetButton(rect)
    
    clicked = button.handle_click((100, 100))
    
    assert clicked is False


def test_reset_button_hover(pygame_init):
    """Test that hovering over reset button updates hover state."""
    rect = pygame.Rect(10, 10, 60, 60)
    button = ResetButton(rect)
    
    # Hover inside
    button.handle_hover((30, 30))
    assert button.hovered is True
    
    # Hover outside
    button.handle_hover((100, 100))
    assert button.hovered is False


def test_controls_widget_has_reset_button(pygame_init):
    """Test that ControlsWidget initializes with reset button."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    assert widget.reset_button is not None
    assert widget.reset_requested is False


def test_controls_widget_reset_requested(pygame_init):
    """Test that clicking reset button sets reset_requested flag."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    # Click reset button
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': widget.reset_button.rect.center}
    )
    widget.handle_event(event)
    
    assert widget.reset_requested is True


def test_controls_widget_reset_flag_persists(pygame_init):
    """Test that reset_requested flag persists until cleared externally."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    # Click reset button
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': widget.reset_button.rect.center}
    )
    widget.handle_event(event)
    
    assert widget.reset_requested is True
    
    # Flag should persist (not auto-clear)
    widget.update()
    assert widget.reset_requested is True
    
    # Must be cleared externally
    widget.reset_requested = False
    assert widget.reset_requested is False

def test_speed_control_initialization(pygame_init):
    """Test that SpeedControl initializes correctly."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect)
    
    assert control.rect == rect
    assert control.speed == 1
    assert control.decrease_hovered is False
    assert control.increase_hovered is False


def test_speed_control_custom_initial_speed(pygame_init):
    """Test that SpeedControl can be initialized with custom speed."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect, initial_speed=5)
    
    assert control.speed == 5


def test_speed_control_increase(pygame_init):
    """Test that clicking increase button increments speed."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect)
    
    initial_speed = control.speed
    clicked = control.handle_click(control.increase_button_rect.center)
    
    assert clicked is True
    assert control.speed == initial_speed + 1


def test_speed_control_decrease(pygame_init):
    """Test that clicking decrease button decrements speed."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect, initial_speed=5)
    
    initial_speed = control.speed
    clicked = control.handle_click(control.decrease_button_rect.center)
    
    assert clicked is True
    assert control.speed == initial_speed - 1


def test_speed_control_minimum_speed(pygame_init):
    """Test that speed cannot go below 1."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect, initial_speed=1)
    
    # Try to decrease below 1
    control.handle_click(control.decrease_button_rect.center)
    
    assert control.speed == 1


def test_speed_control_multiple_increases(pygame_init):
    """Test that speed can be increased multiple times."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect)
    
    for i in range(5):
        control.handle_click(control.increase_button_rect.center)
    
    assert control.speed == 6


def test_speed_control_hover(pygame_init):
    """Test that hovering updates button hover states."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect)
    
    # Hover over decrease button
    control.handle_hover(control.decrease_button_rect.center)
    assert control.decrease_hovered is True
    assert control.increase_hovered is False
    
    # Hover over increase button
    control.handle_hover(control.increase_button_rect.center)
    assert control.decrease_hovered is False
    assert control.increase_hovered is True
    
    # Hover outside
    control.handle_hover((0, 0))
    assert control.decrease_hovered is False
    assert control.increase_hovered is False


def test_speed_control_click_outside(pygame_init):
    """Test that clicking outside buttons doesn't change speed."""
    rect = pygame.Rect(10, 10, 200, 60)
    control = SpeedControl(rect, initial_speed=3)
    
    # Click in text area (middle)
    clicked = control.handle_click(control.text_rect.center)
    
    assert clicked is False
    assert control.speed == 3


def test_controls_widget_has_speed_control(pygame_init):
    """Test that ControlsWidget initializes with speed control."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    assert widget.speed_control is not None
    assert widget.speed == 1


def test_controls_widget_speed_property(pygame_init):
    """Test that speed property reflects speed control state."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    # Increase speed
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': widget.speed_control.increase_button_rect.center}
    )
    widget.handle_event(event)
    
    assert widget.speed == 2


def test_controls_widget_speed_preserved_on_resize(pygame_init):
    """Test that speed is preserved when widget is resized."""
    rect1 = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect1)
    
    # Set speed to 5
    for _ in range(4):
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 1, 'pos': widget.speed_control.increase_button_rect.center}
        )
        widget.handle_event(event)
    
    assert widget.speed == 5
    
    # Resize
    rect2 = pygame.Rect(0, 0, 600, 300)
    widget.set_rect(rect2)
    
    # Speed should be preserved
    assert widget.speed == 5


