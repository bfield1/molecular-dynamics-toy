"""Preset atomic configurations for loading into simulations."""

import logging
from typing import Dict, Callable, List
from ase import Atoms
from ase.build import molecule, bulk, graphene_nanoribbon

logger = logging.getLogger(__name__)


def create_water_molecule() -> Atoms:
    """Create a water molecule.
    
    Returns:
        Atoms object containing H2O in a cubic cell.
    """
    atoms = molecule('H2O')
    
    # Get bounding box
    positions = atoms.get_positions()
    min_pos = positions.min(axis=0)
    max_pos = positions.max(axis=0)
    size = max_pos - min_pos
    
    # Create cubic cell with appropriate vacuum
    cell_size = max(size) + 10.0  # 5 Å vacuum on each side
    atoms.set_cell([cell_size, cell_size, cell_size])
    atoms.center()
    atoms.pbc = True
    
    logger.info("Created water molecule preset")
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
    atoms = graphene_nanoribbon(4, 4, type='zigzag', saturated=False)
    
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


# Registry of all available presets
# Format: name -> (description, creation_function)
PRESETS: Dict[str, tuple[str, Callable[[], Atoms]]] = {
    "water": ("Water molecule", create_water_molecule),
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