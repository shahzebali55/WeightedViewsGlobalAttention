import numpy as np
def small_views(vs, piece_size=5):
    """
    Split views into smaller pieces such that each small view contains only atomic number + 3D coordinates.

    Parameters:
    - vs: numpy array of views
    - piece_size: size of each small view (default = 5: atomic number + 3D coordinates)
    
    Returns:
    - new_view: numpy array with views split into atomic pieces
    """
    # Check that the view size is divisible by the piece size
    if vs.shape[-1] % piece_size != 0:
        raise ValueError(f"View size {vs.shape[-1]} is not divisible by piece size {piece_size}.")
    
    single_atom_piece = vs.shape[-1] // piece_size
    
    new_view = np.reshape(vs, (vs.shape[0], vs.shape[1], single_atom_piece, piece_size))
    
    return new_view

atom_properties = {
    "H": {
        "electronegativity": 2.20, "atomic_mass": 1.008, "valence_electrons": 1,
        "group_number": 1, "covalent_radius": 31, "first_ionization_energy": 13.59,
        "electron_affinity": 0.754, "atomic_volume": 14.0
    },
    "C": {
        "electronegativity": 2.55, "atomic_mass": 12.01, "valence_electrons": 4,
        "group_number": 14, "covalent_radius": 76, "first_ionization_energy": 11.26,
        "electron_affinity": 1.263, "atomic_volume": 4.58
    },
    "N": {
        "electronegativity": 3.04, "atomic_mass": 14.007, "valence_electrons": 5,
        "group_number": 15, "covalent_radius": 71, "first_ionization_energy": 14.534,
        "electron_affinity": 0.07, "atomic_volume": 17.3
    },
    "O": {
        "electronegativity": 3.44, "atomic_mass": 15.999, "valence_electrons": 6,
        "group_number": 16, "covalent_radius": 66, "first_ionization_energy": 13.618,
        "electron_affinity": 1.461, "atomic_volume": 14
    },
    "S": {
        "electronegativity": 2.58, "atomic_mass": 32.06, "valence_electrons": 6,
        "group_number": 16, "covalent_radius": 105, "first_ionization_energy": 10.360,
        "electron_affinity": 2.077, "atomic_volume": 15.5
    },
    "F": {
        "electronegativity": 3.98, "atomic_mass": 18.998, "valence_electrons": 7,
        "group_number": 17, "covalent_radius": 57, "first_ionization_energy": 17.423,
        "electron_affinity": 3.339, "atomic_volume": 17.1
    },
    "P": {
        "electronegativity": 2.19, "atomic_mass": 30.974, "valence_electrons": 5,
        "group_number": 15, "covalent_radius": 107, "first_ionization_energy": 10.487,
        "electron_affinity": 0.745, "atomic_volume": 17.0
    },
    "Cl": {
        "electronegativity": 3.16, "atomic_mass": 35.45, "valence_electrons": 7,
        "group_number": 17, "covalent_radius": 102, "first_ionization_energy": 12.968,
        "electron_affinity": 3.617, "atomic_volume": 22.7
    },
    "Br": {
        "electronegativity": 2.96, "atomic_mass": 79.904, "valence_electrons": 7,
        "group_number": 17, "covalent_radius": 120, "first_ionization_energy": 11.814,
        "electron_affinity": 3.365, "atomic_volume": 23.5
    },
    "I": {
        "electronegativity": 2.66, "atomic_mass": 126.90, "valence_electrons": 7,
        "group_number": 17, "covalent_radius": 139, "first_ionization_energy": 10.451,
        "electron_affinity": 3.059, "atomic_volume": 25.7
    }
  

}

# Switch for atomic properties
single_atomic_property_switches = {
    "electronegativity": True,
    "atomic_mass": True,
    "valence_electrons": True,
    "group_number": True,
    "covalent_radius": True,
    "first_ionization_energy": True,
    "electron_affinity": True,
    "atomic_volume": True
}

atomic_identity_to_type = {
    (1.0, 1.0): "H",
    (2.0, 14.0): "C",
    (2.0, 15.0): "N",
    (2.0, 16.0): "O",
    (2.0, 17.0): "F",
    (3.0, 15.0): "P",
    (3.0, 16.0): "S",
    (3.0, 17.0): "Cl",
    (4.0, 17.0): "Br",
    (5.0, 17.0): "I"
}

def get_embeddings(single_atom, atom_properties, single_atomic_property_switches):
    """
    Build per-atom embeddings for QM8 using:
    [period, group, x, y, z] + selected atomic properties

    Parameters
    ----------
    single_atom : np.ndarray
        Shape (num_molecules, num_views, num_atoms, 5)
    atom_properties : dict
        Dictionary of atomic properties by atom symbol
    single_atomic_property_switches : dict
        Dictionary of True/False switches for atomic properties

    Returns
    -------
    np.ndarray
        Shape (num_molecules, num_views, num_atoms, 5 + num_selected_properties)
    """
    number_of_molecules = single_atom.shape[0]
    number_of_views = single_atom.shape[1]
    number_of_atoms = single_atom.shape[2]

    property_keys = [k for k, v in single_atomic_property_switches.items() if v]
    num_properties = len(property_keys)

    atom_embeddings = []

    for mol_id in range(number_of_molecules):
        molecule_extended = []
        for view_id in range(number_of_views):
            view_data = single_atom[mol_id, view_id]
            view_extended = []

            for atom_id in range(number_of_atoms):
                atom_vec = view_data[atom_id]

                period = atom_vec[0]
                group = atom_vec[1]
                coords = atom_vec[2:5]

                # padded atom
                if period == 0.0 and group == 0.0:
                    extended_atom = np.zeros(5 + num_properties)
                else:
                    atom_type = atomic_identity_to_type[(period, group)]
                    properties = [atom_properties[atom_type][prop] for prop in property_keys]
                    extended_atom = np.concatenate([atom_vec, properties])

                view_extended.append(extended_atom)

            molecule_extended.append(np.array(view_extended))
        atom_embeddings.append(np.array(molecule_extended))

    return np.array(atom_embeddings)