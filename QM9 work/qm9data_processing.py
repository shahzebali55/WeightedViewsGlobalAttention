"""
Qm9 dataset:
    - "mol_id" - Molecule ID (gdb9 index) mapping to the .sdf file
    - "A" - Rotational constant (unit: GHz)
    - "B" - Rotational constant (unit: GHz)
    - "C" - Rotational constant (unit: GHz)
    - "mu" - Dipole moment (unit: D)
    - "alpha" - Isotropic polarizability (unit: Bohr^3)
    - "homo" - Highest occupied molecular orbital energy (unit: Hartree)
    - "lumo" - Lowest unoccupied molecular orbital energy (unit: Hartree)
    - "gap" - Gap between HOMO and LUMO (unit: Hartree)
    - "r2" - Electronic spatial extent (unit: Bohr^2)
    - "zpve" - Zero point vibrational energy (unit: Hartree)
    - "u0" - Internal energy at 0K (unit: Hartree)
    - "u298" - Internal energy at 298.15K (unit: Hartree)
    - "h298" - Enthalpy at 298.15K (unit: Hartree)
    - "g298" - Free energy at 298.15K (unit: Hartree)
    - "cv" - Heat capavity at 298.15K (unit: cal/(mol*K))
    - "u0_atom" - Atomization energy at 0K (unit: kcal/mol)
    - "u298_atom" - Atomization energy at 298.15K (unit: kcal/mol)
    - "h298_atom" - Atomization enthalpy at 298.15K (unit: kcal/mol)
    - "g298_atom" - Atomization free energy at 298.15K (unit: kcal/mol)

information source: https://github.com/deepchem/deepchem/blob/master/deepchem/molnet/load_function/qm9_datasets.py
data source: https://figshare.com/collections/Quantum_chemistry_structures_and_properties_of_134_kilo_molecules/978904
More information :https://www.nature.com/articles/sdata201422#Tab3
"""

import os
import numpy as np
import re

# Only these 12 targets
TARGET_NAMES = [
    "mu", "alpha", "homo", "lumo", "gap", "r2",
    "zpve", "u0", "u298", "h298", "g298", "cv"
]

def fix_values(value):
    # converts things like 1.23*^5 to 1.23e5
    return float(re.sub(r'(\d+)\*\^([-+]?\d+)', r'\1e\2', value))

def extract_qm9_data_and_targets(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # line 1: number of atoms
        num_atoms = int(lines[0].strip())

        # line 2: QM9 properties line
        props = lines[1].strip().split()

        # Standard QM9 property positions:
        # 0: mol_id
        # 1: A
        # 2: B
        # 3: C
        # 4: mu
        # 5: alpha
        # 6: homo
        # 7: lumo
        # 8: gap
        # 9: r2
        # 10: zpve
        # 11: u0
        # 12: u298
        # 13: h298
        # 14: g298
        # 15: cv

        if len(props) < 16:
            raise ValueError(f"Property line has only {len(props)} values, expected at least 16.")

        targets = {
            "mu":   fix_values(props[4]),
            "alpha":fix_values(props[5]),
            "homo": fix_values(props[6]),
            "lumo": fix_values(props[7]),
            "gap":  fix_values(props[8]),
            "r2":   fix_values(props[9]),
            "zpve": fix_values(props[10]),
            "u0":   fix_values(props[11]),
            "u298": fix_values(props[12]),
            "h298": fix_values(props[13]),
            "g298": fix_values(props[14]),
            "cv":   fix_values(props[15]),
        }

        atom_data = []
        for line in lines[2:2 + num_atoms]:
            parts = line.strip().split()
            if len(parts) >= 4:
                element = parts[0]
                x, y, z = map(fix_values, parts[1:4])
                atom_data.append((element, np.array([x, y, z], dtype=np.float32)))

        return atom_data, targets

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None


def process_qm9_files(directory, max_molecules=500):
    all_molecules = []
    all_targets = []

    filenames = sorted([f for f in os.listdir(directory) if f.endswith(".xyz")])[:max_molecules]

    for filename in filenames:
        file_path = os.path.join(directory, filename)
        atom_data, targets = extract_qm9_data_and_targets(file_path)

        if atom_data is not None and targets is not None:
            all_molecules.append(atom_data)
            all_targets.append([targets[name] for name in TARGET_NAMES])

    all_targets = np.array(all_targets, dtype=np.float32)

    print(f"Total .xyz files processed: {len(all_molecules)}")
    print(f"Target array shape: {all_targets.shape}")  

    return all_molecules, all_targets



directory_path = "qm9_data"

# run
all_molecules, y = process_qm9_files(directory_path, max_molecules=500)


   

    
