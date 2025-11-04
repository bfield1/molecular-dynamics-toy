"""Preset atomic configurations for loading into simulations."""

import logging
from typing import Dict, Callable, List

import numpy as np
from ase import Atoms
from ase.build import molecule, bulk, graphene_nanoribbon

logger = logging.getLogger(__name__)


def _molecule_in_box(molecule_name: str, vacuum: float = 5.0) -> Atoms:
    """Create a molecule centered in a cubic box with vacuum.
    
    Args:
        molecule_name: Name of molecule (ASE molecule database).
        vacuum: Vacuum space on each side in Angstroms.
        
    Returns:
        Atoms object with molecule in cubic cell.
    """
    atoms = molecule(molecule_name)
    
    # Get bounding box
    positions = atoms.get_positions()
    min_pos = positions.min(axis=0)
    max_pos = positions.max(axis=0)
    size = max_pos - min_pos
    
    # Create cubic cell with appropriate vacuum
    cell_size = max(size) + 2 * vacuum
    atoms.set_cell([cell_size, cell_size, cell_size])
    atoms.center()
    atoms.pbc = True
    
    return atoms


def create_water_molecule() -> Atoms:
    """Create a water molecule.
    
    Returns:
        Atoms object containing H2O in a cubic cell.
    """
    atoms = _molecule_in_box('H2O', vacuum=5.0)
    atoms.rotate(90, 'y')
    logger.info("Created water molecule preset")
    return atoms


def create_ethanol_molecule() -> Atoms:
    """Create an ethanol molecule.
    
    Returns:
        Atoms object containing C2H5OH in a cubic cell.
    """
    atoms = _molecule_in_box('CH3CH2OH', vacuum=5.0)
    logger.info("Created ethanol molecule preset")
    return atoms


def create_methane_molecule() -> Atoms:
    """Create a methane molecule.
    
    Returns:
        Atoms object containing CH4 in a cubic cell.
    """
    atoms = _molecule_in_box('CH4', vacuum=5.0)
    logger.info("Created methane molecule preset")
    return atoms


def create_benzene_molecule() -> Atoms:
    """Create a benzene molecule.
    
    Returns:
        Atoms object containing C6H6 in a cubic cell.
    """
    atoms = _molecule_in_box('C6H6', vacuum=5.0)
    logger.info("Created benzene molecule preset")
    return atoms


def create_co2_molecule() -> Atoms:
    """Create a carbon dioxide molecule.
    
    Returns:
        Atoms object containing CO2 in a cubic cell.
    """
    atoms = _molecule_in_box('CO2', vacuum=5.0)
    atoms.rotate(90, 'y')
    logger.info("Created CO2 molecule preset")
    return atoms


def create_diamond_lattice() -> Atoms:
    """Create a diamond lattice structure.
    
    Returns:
        Atoms object containing diamond structure.
    """
    atoms = bulk('C', 'diamond', a=3.567, cubic=True)
    # Make it 2x2x2 supercell for better visualization
    #atoms = atoms.repeat((2, 2, 2))
    logger.info("Created diamond lattice preset")
    return atoms


def create_fcc_gold() -> Atoms:
    """Create an FCC gold structure.
    
    Returns:
        Atoms object containing FCC Au structure.
    """
    atoms = bulk('Au', 'fcc', a=4.08, cubic=True)
    # Make it 2x2x2 supercell
    atoms = atoms.repeat((2, 2, 2))
    logger.info("Created FCC gold preset")
    return atoms


def create_graphene_sheet() -> Atoms:
    """Create a graphene sheet.
    
    Returns:
        Atoms object containing graphene in a cubic cell.
    """
    # Create small graphene nanoribbon (in x-z plane)
    atoms = graphene_nanoribbon(3, 4, type='zigzag', saturated=False)
    
    # Rotate 90 degrees around x-axis to move from x-z to x-y plane
    atoms.rotate(90, 'x', rotate_cell=True)
    
    # Get bounding box in each dimension
    positions = atoms.get_positions()
    min_pos = positions.min(axis=0)
    max_pos = positions.max(axis=0)
    size = max_pos - min_pos
    
    # Create cubic cell with appropriate vacuum
    xy_size = max(size[0], size[1])
    cell_size = max(xy_size + 6.0, size[2] + 10.0)  # More vacuum perpendicular to sheet
    
    atoms.set_cell([cell_size, cell_size, cell_size])
    atoms.center()
    
    atoms.pbc = True
    
    logger.info("Created graphene sheet preset")
    return atoms


def create_nacl_crystal() -> Atoms:
    """Create a NaCl (rock salt) crystal structure.
    
    Returns:
        Atoms object containing NaCl structure.
    """
    atoms = bulk('NaCl', 'rocksalt', a=5.64, cubic=True)
    logger.info("Created NaCl crystal preset")
    return atoms

def create_copper_fcc() -> Atoms:
    """Create an FCC copper structure.
    
    Returns:
        Atoms object containing FCC Cu structure.
    """
    atoms = bulk('Cu', 'fcc', a=3.61, cubic=True)
    # Make it 2x2x2 supercell
    atoms = atoms.repeat((2, 2, 2))
    logger.info("Created FCC copper preset")
    return atoms

def create_ice_crystal() -> Atoms:
    """Create an ice crystal structure (simplified cubic ice).
    
    Returns:
        Atoms object containing simplified ice structure in cubic cell.
    """
    
    
    # Create a simplified cubic ice structure
    # Real ice Ih is hexagonal, but we'll make a cubic approximation
    # O-O distance in ice is ~2.76 Angstrom
    a = 2.76  # O-O lattice parameter
    
    # Create oxygen positions in a cubic arrangement
    o_positions = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                o_positions.append([i * a, j * a, k * a])
    
    atoms = Atoms('O' + str(len(o_positions)), positions=o_positions)
    
    # Add hydrogens in approximate tetrahedral positions
    # Each O has ~4 H neighbors in ice, but we'll add 2 per O for simplicity
    # O-H bond length is ~0.96 Angstrom
    h_positions = []
    for pos in o_positions:
        # Add H atoms at reasonable bond distances and angles
        h_positions.append(pos + np.array([0.96, 0, 0]))
        h_positions.append(pos + np.array([0, 0.96, 0]))
    
    h_atoms = Atoms('H' + str(len(h_positions)), positions=h_positions)
    atoms += h_atoms
    
    # Set cubic cell
    cell_size = 2 * a
    atoms.set_cell([cell_size, cell_size, cell_size])
    atoms.center()
    atoms.pbc = True
    
    logger.info("Created simplified ice crystal preset")
    return atoms

# Registry of all available presets
# Format: name -> (description, creation_function)
PRESETS: Dict[str, tuple[str, Callable[[], Atoms]]] = {
    "water": ("Water molecule", create_water_molecule),
    "ice": ("Ice crystal", create_ice_crystal),
    "ethanol": ("Ethanol molecule", create_ethanol_molecule),
    "methane": ("Methane molecule", create_methane_molecule),
    "benzene": ("Benzene molecule", create_benzene_molecule),
    "co2": ("Carbon dioxide", create_co2_molecule),
    "diamond": ("Diamond lattice", create_diamond_lattice),
    "gold": ("FCC gold", create_fcc_gold),
    "graphene": ("Graphene sheet", create_graphene_sheet),
    "nacl": ("NaCl crystal", create_nacl_crystal),
    "copper": ("FCC copper", create_copper_fcc),
}


def get_preset_names() -> List[str]:
    """Get list of all preset names.
    
    Returns:
        List of preset identifiers.
    """
    return list(PRESETS.keys())


def get_preset_display_name(preset_id: str) -> str:
    """Get display name for a preset.
    
    Args:
        preset_id: Preset identifier.
        
    Returns:
        Human-readable name for the preset.
    """
    if preset_id in PRESETS:
        return PRESETS[preset_id][0]
    return preset_id


def create_preset(preset_id: str) -> Atoms:
    """Create atoms for a given preset.
    
    Args:
        preset_id: Preset identifier.
        
    Returns:
        Atoms object for the preset.
        
    Raises:
        ValueError: If preset_id is not recognized.
    """
    if preset_id not in PRESETS:
        raise ValueError(f"Unknown preset: {preset_id}")
    
    _, creator_func = PRESETS[preset_id]
    return creator_func()