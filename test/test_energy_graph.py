"""Tests for the EnergyGraphWidget."""

import os
import pytest
from collections import deque

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from molecular_dynamics_toy.widgets.energy_graph import EnergyGraphWidget, EnergyPoint


@pytest.fixture(autouse=True)
def pygame_init():
    """Initialise and quit pygame around each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def surface():
    """Return a small off-screen surface for rendering tests."""
    return pygame.Surface((800, 800))


@pytest.fixture
def sim_rect():
    """Return a representative simulation cell rectangle."""
    return pygame.Rect(50, 50, 700, 700)


def make_widget(maxlen: int = 300) -> EnergyGraphWidget:
    """Helper: create an EnergyGraphWidget with a fresh empty deque."""
    history: deque = deque(maxlen=maxlen)
    return EnergyGraphWidget(history)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_instantiation_empty_deque():
    """EnergyGraphWidget can be created with an empty deque."""
    widget = make_widget()
    assert widget.energy_history is not None
    assert len(widget.energy_history) == 0


def test_instantiation_stores_reference():
    """EnergyGraphWidget holds a reference to the same deque object."""
    history: deque = deque(maxlen=300)
    widget = EnergyGraphWidget(history)
    assert widget.energy_history is history


# ---------------------------------------------------------------------------
# Rendering — no crash guarantees
# ---------------------------------------------------------------------------

def test_render_empty_history(surface, sim_rect):
    """render() does not raise when energy history is empty."""
    widget = make_widget()
    widget.render(surface, sim_rect)  # must not raise


def test_render_one_point(surface, sim_rect):
    """render() does not raise with a single data point."""
    history: deque = deque(maxlen=300)
    history.append(EnergyPoint(step=1, ke=1.0, pe=-2.0))
    widget = EnergyGraphWidget(history)
    widget.render(surface, sim_rect)  # must not raise


def test_render_two_points(surface, sim_rect):
    """render() does not raise with exactly two data points (minimum for a line)."""
    history: deque = deque(maxlen=300)
    history.append(EnergyPoint(step=1, ke=1.0, pe=-2.0))
    history.append(EnergyPoint(step=2, ke=1.1, pe=-2.1))
    widget = EnergyGraphWidget(history)
    widget.render(surface, sim_rect)  # must not raise


def test_render_full_history(surface, sim_rect):
    """render() does not raise with a full rolling window of 300 points."""
    history: deque = deque(maxlen=300)
    for i in range(300):
        history.append(EnergyPoint(step=i, ke=float(i) * 0.01, pe=-float(i) * 0.02))
    widget = EnergyGraphWidget(history)
    widget.render(surface, sim_rect)  # must not raise


def test_render_constant_energy(surface, sim_rect):
    """render() handles the degenerate case where all energy values are identical."""
    history: deque = deque(maxlen=300)
    for i in range(50):
        history.append(EnergyPoint(step=i, ke=1.0, pe=-1.0))
    widget = EnergyGraphWidget(history)
    widget.render(surface, sim_rect)  # must not raise (y_range guard)


# ---------------------------------------------------------------------------
# Graph positioning
# ---------------------------------------------------------------------------

def test_graph_positioned_within_sim_rect(surface, sim_rect):
    """The graph panel must be entirely within the simulation rect vertically."""
    widget = make_widget()
    # The graph bottom should equal sim_rect.bottom
    graph_bottom = sim_rect.bottom
    graph_top = sim_rect.bottom - widget.GRAPH_HEIGHT
    assert graph_top >= sim_rect.top, (
        f"Graph top ({graph_top}) is above sim_rect top ({sim_rect.top})"
    )
    assert graph_bottom == sim_rect.bottom


def test_graph_height_constant():
    """GRAPH_HEIGHT class constant is a positive integer."""
    assert isinstance(EnergyGraphWidget.GRAPH_HEIGHT, int)
    assert EnergyGraphWidget.GRAPH_HEIGHT > 0


def test_alpha_constant_in_range():
    """ALPHA class constant is in the valid pygame range [0, 255]."""
    assert 0 <= EnergyGraphWidget.ALPHA <= 255


# ---------------------------------------------------------------------------
# EnergyPoint named tuple
# ---------------------------------------------------------------------------

def test_energy_point_fields():
    """EnergyPoint stores step, ke, and pe correctly."""
    pt = EnergyPoint(step=42, ke=3.14, pe=-1.59)
    assert pt.step == 42
    assert pt.ke == pytest.approx(3.14)
    assert pt.pe == pytest.approx(-1.59)


def test_energy_point_total():
    """Total energy can be computed from EnergyPoint fields."""
    pt = EnergyPoint(step=1, ke=2.0, pe=-5.0)
    assert pt.ke + pt.pe == pytest.approx(-3.0)
