"""Tests for the MD engine."""

import pytest
import numpy as np
from ase import Atoms
from molecular_dynamics_toy.engine import MDEngine

# from mattersim.forcefield import MatterSimCalculator

# calculator = MatterSimCalculator(device="cpu")


class MockCalculator:
    """Mock calculator for testing without heavy dependencies."""
    
    def __init__(self):
        self.results = {}
    
    def get_potential_energy(self, atoms):
        """Return dummy energy."""
        return 0.0
    
    def get_forces(self, atoms):
        """Return simple harmonic forces for H2-like molecule."""
        if len(atoms) < 2:
            return np.zeros((len(atoms), 3))
        
        forces = np.zeros((len(atoms), 3))
        
        # Simple pairwise harmonic potential centered at 0.74 Å
        equilibrium_distance = 0.74
        k = 100.0  # Force constant in eV/Å²
        
        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):
                vec = atoms.positions[j] - atoms.positions[i]
                dist = np.linalg.norm(vec)
                if dist > 0:
                    force_mag = k * (dist - equilibrium_distance)
                    force_vec = force_mag * vec / dist
                    forces[i] += force_vec
                    forces[j] -= force_vec
        
        return forces


def test_mdengine_initialization():
    """Test MDEngine initializes with correct defaults."""
    engine = MDEngine(calculator=MockCalculator())
    
    assert engine.timestep == 1.0
    assert engine.temperature == 300.0
    assert len(engine.atoms) == 0
    assert engine.calculator is not None


def test_add_atom():
    """Test adding atoms to the simulation."""
    engine = MDEngine(calculator=MockCalculator())
    
    engine.add_atom('H', [-0.4, 0, 0])
    engine.add_atom('H', [0.4, 0, 0])
    
    assert len(engine.atoms) == 2
    assert engine.atoms[0].symbol == 'H'
    assert engine.atoms[1].symbol == 'H'
    np.testing.assert_array_almost_equal(
        engine.atoms.get_positions()[0], [-0.4, 0, 0]
    )


def test_temperature_setter():
    """Test temperature property setter."""
    engine = MDEngine(calculator=MockCalculator())
    engine.add_atom('H', [0, 0, 0])
    
    engine.temperature = 100
    assert engine.temperature == 100


def test_h2_molecule_equilibration():
    """Test H2 molecule equilibrates to correct bond length.
    
    Creates an H2 molecule, runs MD, and checks that the bond length
    is close to the experimental value of 0.74 Å.
    """
    engine = MDEngine(calculator=MockCalculator(), temperature=100)
    
    # Add H2 molecule slightly displaced from equilibrium
    engine.add_atom('H', [-0.4, 0, 0])
    engine.add_atom('H', [0.4, 0, 0])
    
    # Run simulation
    engine.run(100)
    
    # Check bond length is in reasonable range
    bond_length = engine.atoms.get_distance(0, 1, mic=True)
    assert 0.69 < bond_length < 0.79, f"Bond length {bond_length:.3f} Å out of range"


def test_empty_simulation_runs():
    """Test that running with no atoms doesn't crash."""
    engine = MDEngine(calculator=MockCalculator())
    engine.run(10)  # Should not raise
    assert len(engine.atoms) == 0


def test_atoms_setter():
    """Test setting atoms object directly."""
    engine = MDEngine(calculator=MockCalculator())
    
    new_atoms = Atoms('H2', positions=[[-0.37, 0, 0], [0.37, 0, 0]], 
                      cell=[20, 20, 20], pbc=True)
    engine.atoms = new_atoms
    
    assert len(engine.atoms) == 2
    assert engine.atoms.calc is engine.calculator
