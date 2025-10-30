"""Tests for the controls widget."""

import pytest
import pygame
from molecular_dynamics_toy.widgets.controls import ControlsWidget, PlayPauseButton, ResetButton, SpeedControl, TemperatureSlider


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

def test_temperature_slider_initialization(pygame_init):
    """Test that TemperatureSlider initializes correctly."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect)
    
    assert slider.rect == rect
    assert slider.temperature == 300.0
    assert slider.min_temp == 0.0
    assert slider.max_temp == 1000.0
    assert slider.dragging is False
    assert slider.hovered is False


def test_temperature_slider_custom_initial_temp(pygame_init):
    """Test that TemperatureSlider can be initialized with custom temperature."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect, initial_temp=500.0)
    
    assert slider.temperature == 500.0


def test_temperature_slider_custom_range(pygame_init):
    """Test that TemperatureSlider can have custom min/max."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect, min_temp=100.0, max_temp=2000.0)
    
    assert slider.min_temp == 100.0
    assert slider.max_temp == 2000.0


def test_temperature_slider_click_starts_drag(pygame_init):
    """Test that clicking slider starts dragging."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect)
    
    slider_rect = slider._get_slider_rect()
    clicked = slider.handle_click(slider_rect.center)
    
    assert clicked is True
    assert slider.dragging is True


def test_temperature_slider_release_stops_drag(pygame_init):
    """Test that releasing mouse stops dragging."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect)
    
    slider_rect = slider._get_slider_rect()
    slider.handle_click(slider_rect.center)
    assert slider.dragging is True
    
    slider.handle_release()
    assert slider.dragging is False


def test_temperature_slider_click_on_track(pygame_init):
    """Test that clicking on track updates temperature."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect, initial_temp=300.0)
    
    track_rect = slider._get_track_rect()
    
    # Click at start of track (should be min_temp)
    slider.handle_click((track_rect.left + 1, track_rect.centery))
    assert slider.temperature < slider.min_temp + 20  # Near minimum
    
    # Click at end of track (should be max_temp)
    slider.handle_click((track_rect.right - 1, track_rect.centery))
    assert slider.temperature > slider.max_temp - 20  # Near maximum


def test_temperature_slider_drag_updates_temperature(pygame_init):
    """Test that dragging slider updates temperature."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect, initial_temp=300.0)
    
    slider_rect = slider._get_slider_rect()
    slider.handle_click(slider_rect.center)
    
    # Drag to different position
    track_rect = slider._get_track_rect()
    slider.handle_drag((track_rect.right - 50, track_rect.centery))
    
    # Temperature should have increased significantly
    assert slider.temperature > 800


def test_temperature_slider_no_drag_when_not_dragging(pygame_init):
    """Test that handle_drag does nothing when not dragging."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect, initial_temp=500.0)
    
    track_rect = slider._get_track_rect()
    slider.handle_drag((track_rect.left, track_rect.centery))
    
    # Temperature should not have changed
    assert slider.temperature == 500.0


def test_temperature_slider_hover(pygame_init):
    """Test that hovering over slider updates hover state."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect)
    
    slider_rect = slider._get_slider_rect()
    
    # Hover over slider
    slider.handle_hover(slider_rect.center)
    assert slider.hovered is True
    
    # Hover outside slider
    slider.handle_hover((0, 0))
    assert slider.hovered is False


def test_temperature_slider_clamps_to_range(pygame_init):
    """Test that temperature is clamped to min/max range."""
    rect = pygame.Rect(10, 10, 400, 60)
    slider = TemperatureSlider(rect)
    
    track_rect = slider._get_track_rect()
    
    # Click far left (beyond track)
    slider.handle_click((track_rect.left - 100, track_rect.centery))
    assert slider.temperature >= slider.min_temp
    
    # Click far right (beyond track)
    slider.handle_click((track_rect.right + 100, track_rect.centery))
    assert slider.temperature <= slider.max_temp


def test_controls_widget_has_temperature_slider(pygame_init):
    """Test that ControlsWidget initializes with temperature slider."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    assert widget.temperature_slider is not None
    assert widget.temperature == 300.0


def test_controls_widget_temperature_property(pygame_init):
    """Test that temperature property reflects slider state."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    # Click on slider track
    track_rect = widget.temperature_slider._get_track_rect()
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': (track_rect.right - 50, track_rect.centery)}
    )
    widget.handle_event(event)
    
    # Temperature should have changed from default
    assert widget.temperature != 300.0
    assert widget.temperature > 800


def test_controls_widget_temperature_preserved_on_resize(pygame_init):
    """Test that temperature is preserved when widget is resized."""
    rect1 = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect1)
    
    # Set temperature to 750K
    track_rect = widget.temperature_slider._get_track_rect()
    widget.temperature_slider.handle_click((track_rect.left + track_rect.width * 0.75, track_rect.centery))
    
    temp_before = widget.temperature
    assert 700 < temp_before < 800  # Around 750K
    
    # Resize
    rect2 = pygame.Rect(0, 0, 600, 300)
    widget.set_rect(rect2)
    
    # Temperature should be preserved
    assert abs(widget.temperature - temp_before) < 1.0


def test_controls_widget_temperature_drag(pygame_init):
    """Test that dragging temperature slider works through widget."""
    rect = pygame.Rect(0, 0, 500, 250)
    widget = ControlsWidget(rect)
    
    slider_rect = widget.temperature_slider._get_slider_rect()
    
    # Start drag
    mousedown = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {'button': 1, 'pos': slider_rect.center}
    )
    widget.handle_event(mousedown)
    assert widget.temperature_slider.dragging is True
    
    # Drag
    track_rect = widget.temperature_slider._get_track_rect()
    mousemove = pygame.event.Event(
        pygame.MOUSEMOTION,
        {'pos': (track_rect.left + 50, track_rect.centery)}
    )
    widget.handle_event(mousemove)
    
    # Temperature should have changed
    assert widget.temperature < 150  # Dragged to low position
    
    # Release
    mouseup = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1})
    widget.handle_event(mouseup)
    assert widget.temperature_slider.dragging is False
