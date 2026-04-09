"""Energy vs time graph overlay widget for the simulation window."""

import logging
from collections import deque
from typing import NamedTuple

import pygame

from molecular_dynamics_toy.data import colors

logger = logging.getLogger(__name__)


class EnergyPoint(NamedTuple):
    """A single recorded energy sample."""
    time: float  # simulation time in femtoseconds
    ke: float    # kinetic energy in eV
    pe: float    # potential energy in eV


class EnergyGraphWidget:
    """Transparent overlay graph showing kinetic, potential, and total energy vs time.

    Renders as a semi-transparent panel anchored to the bottom edge of the
    simulation cell rectangle. Three lines are drawn:
      - Blue  : kinetic energy (KE)
      - Orange: potential energy (PE)
      - Green : total energy (KE + PE)

    The y-axis auto-scales to the visible data window. The x-axis spans the
    rolling history window.

    Attributes:
        energy_history: Shared deque of EnergyPoint records (owned by SimulationWidget).
        graph_height: Height of the graph panel in pixels.
        alpha: Transparency of the background panel (0=transparent, 255=opaque).
    """

    GRAPH_HEIGHT: int = 120
    ALPHA: int = 180

    # Colours
    BG_COLOR = colors.ENERGY_GRAPH_BG_COLOR
    LINE_KE_COLOR = colors.ENERGY_GRAPH_LINE_KE_COLOR
    LINE_PE_COLOR = colors.ENERGY_GRAPH_LINE_PE_COLOR
    LINE_TOTAL_COLOR = colors.ENERGY_GRAPH_LINE_TOTAL_COLOR
    AXIS_COLOR = colors.ENERGY_GRAPH_AXIS_COLOR
    TEXT_COLOR = colors.ENERGY_GRAPH_TEXT_COLOR

    # Layout constants
    MARGIN_LEFT: int = 40    # space for y-axis labels
    MARGIN_RIGHT: int = 10
    MARGIN_TOP: int = 8
    MARGIN_BOTTOM: int = 18  # space for x-axis label

    def __init__(self, energy_history: deque):
        """Initialise the graph widget.

        Args:
            energy_history: Deque of EnergyPoint records shared with SimulationWidget.
                            The widget reads from this deque but never writes to it.
        """
        self.energy_history = energy_history
        self.font_small = pygame.font.Font(None, 16)
        self.font_label = pygame.font.Font(None, 14)

    def render(self, surface: pygame.Surface, sim_rect: pygame.Rect):
        """Render the energy graph onto the given surface.

        The graph is positioned at the bottom of *sim_rect*.

        Args:
            surface: Main display surface to blit onto.
            sim_rect: Rectangle of the simulation cell (not the full widget rect).
        """
        graph_rect = pygame.Rect(
            sim_rect.left,
            sim_rect.bottom - self.GRAPH_HEIGHT,
            sim_rect.width,
            self.GRAPH_HEIGHT,
        )

        # Skip rendering if the graph area is too small to draw
        if graph_rect.width <= 0 or graph_rect.height <= 0:
            return

        # --- Draw semi-transparent background ---
        bg_surface = pygame.Surface((graph_rect.width, graph_rect.height), pygame.SRCALPHA)
        bg_color_alpha = (*self.BG_COLOR, self.ALPHA)
        bg_surface.fill(bg_color_alpha)
        surface.blit(bg_surface, graph_rect.topleft)

        # Plot area (inside margins)
        plot_rect = pygame.Rect(
            graph_rect.left + self.MARGIN_LEFT,
            graph_rect.top + self.MARGIN_TOP,
            graph_rect.width - self.MARGIN_LEFT - self.MARGIN_RIGHT,
            graph_rect.height - self.MARGIN_TOP - self.MARGIN_BOTTOM,
        )

        # Skip rendering if plot area is degenerate
        if plot_rect.width <= 0 or plot_rect.height <= 0:
            return

        # --- Draw axes ---
        # y-axis
        pygame.draw.line(
            surface, self.AXIS_COLOR,
            (plot_rect.left, plot_rect.top),
            (plot_rect.left, plot_rect.bottom),
            1,
        )
        # x-axis
        pygame.draw.line(
            surface, self.AXIS_COLOR,
            (plot_rect.left, plot_rect.bottom),
            (plot_rect.right, plot_rect.bottom),
            1,
        )

        # --- Draw x-axis label ---
        x_label = self.font_label.render("Time / fs", True, self.TEXT_COLOR)
        surface.blit(
            x_label,
            (plot_rect.centerx - x_label.get_width() // 2,
             graph_rect.bottom - self.MARGIN_BOTTOM + 3),
        )

        # --- Draw data lines and x-axis time labels ---
        if len(self.energy_history) >= 2:
            self._draw_lines(surface, plot_rect)
            self._draw_x_labels(surface, plot_rect)

        # --- Draw legend ---
        self._draw_legend(surface, graph_rect)

    def _draw_x_labels(self, surface: pygame.Surface, plot_rect: pygame.Rect):
        """Draw time tick labels at the left and right ends of the x-axis.

        Args:
            surface: Surface to draw onto.
            plot_rect: Plot area rectangle.
        """
        history = list(self.energy_history)
        t_start = history[0].time
        t_end = history[-1].time

        label_y = plot_rect.bottom + 2

        start_surf = self.font_label.render(f"{t_start:.0f}", True, self.TEXT_COLOR)
        surface.blit(start_surf, (plot_rect.left, label_y))

        end_surf = self.font_label.render(f"{t_end:.0f}", True, self.TEXT_COLOR)
        surface.blit(end_surf, (plot_rect.right - end_surf.get_width(), label_y))

    def _draw_lines(self, surface: pygame.Surface, plot_rect: pygame.Rect):
        """Draw the three energy lines onto the plot area.

        Args:
            surface: Surface to draw onto.
            plot_rect: Rectangle defining the drawable plot area (inside axes).
        """
        history = list(self.energy_history)

        time_values = [p.time for p in history]
        ke_values = [p.ke for p in history]
        pe_values = [p.pe for p in history]
        total_values = [p.ke + p.pe for p in history]

        all_values = ke_values + pe_values + total_values
        # Always include zero in the visible range
        y_min = min(0.0, min(all_values))
        y_max = max(0.0, max(all_values))

        # Avoid division by zero when all values are identical (e.g. all zero)
        y_range = y_max - y_min
        if abs(y_range) < 1e-10:
            y_range = 1.0
            y_min -= 0.5
            y_max = y_min + y_range

        n = len(history)
        t_min = time_values[0]
        t_max = time_values[-1]
        t_range = t_max - t_min if t_max > t_min else 1.0

        w = plot_rect.width
        h = plot_rect.height

        def to_screen(i: int, value: float):
            x = plot_rect.left + int((time_values[i] - t_min) / t_range * w)
            y = plot_rect.bottom - int((value - y_min) / y_range * h)
            return (x, y)

        # Draw zero-energy reference line (always visible since range includes zero)
        zero_y = plot_rect.bottom - int((0.0 - y_min) / y_range * h)
        pygame.draw.line(
            surface, self.AXIS_COLOR,
            (plot_rect.left, zero_y),
            (plot_rect.right, zero_y),
            1,
        )
        self._draw_y_label(surface, plot_rect, 0.0, zero_y)

        # Draw each series
        for series, color in (
            (ke_values, self.LINE_KE_COLOR),
            (pe_values, self.LINE_PE_COLOR),
            (total_values, self.LINE_TOTAL_COLOR),
        ):
            points = [to_screen(i, v) for i, v in enumerate(series)]
            if len(points) >= 2:
                pygame.draw.lines(surface, color, False, points, 1)

        # Draw y-axis tick labels (min and max), skipping if too close to zero label
        if abs(y_max) > abs(y_range) * 0.1:
            self._draw_y_label(surface, plot_rect, y_max, plot_rect.top)
        if abs(y_min) > abs(y_range) * 0.1:
            self._draw_y_label(surface, plot_rect, y_min, plot_rect.bottom)

    def _draw_y_label(self, surface: pygame.Surface, plot_rect: pygame.Rect,
                      value: float, y: int):
        """Draw a y-axis tick label.

        Args:
            surface: Surface to draw onto.
            plot_rect: Plot area rectangle (used for x positioning).
            value: Energy value to display.
            y: Screen y-coordinate for the label.
        """
        label = self.font_label.render(f"{value:.2f}", True, self.TEXT_COLOR)
        surface.blit(
            label,
            (plot_rect.left - label.get_width() - 3,
             y - label.get_height() // 2),
        )

    def _draw_legend(self, surface: pygame.Surface, graph_rect: pygame.Rect):
        """Draw a compact legend in the top-left corner of the graph panel.

        Args:
            surface: Surface to draw onto.
            graph_rect: Full graph panel rectangle.
        """
        entries = [
            ("KE",    self.LINE_KE_COLOR),
            ("PE",    self.LINE_PE_COLOR),
            ("Total", self.LINE_TOTAL_COLOR),
        ]

        swatch_size = 8
        entry_height = 12
        padding = 4
        legend_width = 48
        legend_height = len(entries) * entry_height + 2 * padding

        legend_x = graph_rect.left + self.MARGIN_LEFT + padding
        legend_y = graph_rect.top + self.MARGIN_TOP

        # Semi-transparent legend background
        legend_bg = pygame.Surface((legend_width, legend_height), pygame.SRCALPHA)
        legend_bg.fill((0, 0, 0, 120))
        surface.blit(legend_bg, (legend_x, legend_y))

        for i, (label, color) in enumerate(entries):
            row_y = legend_y + padding + i * entry_height
            # Colour swatch
            pygame.draw.rect(
                surface, color,
                pygame.Rect(legend_x + padding, row_y + 2, swatch_size, swatch_size),
            )
            # Label text
            text_surf = self.font_label.render(label, True, self.TEXT_COLOR)
            surface.blit(text_surf, (legend_x + padding + swatch_size + 3, row_y))
