# WeightedViewsGlobalAttention


# Weighted Views Transformer for Molecular Learning

This repository contains the implementation of the Weighted Views framework combined with Transformer-based architectures for:
- QM7 molecular property prediction
- Enantiomer ranking using docking scores

---

## Repository Structure
```text
Weighted_Views_Transformer/
├── Code/
   ├── common_utils
        └─  enantiomer_single_atom.py
        └─  qm7_single_atom.py
        └─  qm7_weightedviews.py
        └─  views_test.py
        └─  views_train.py
        └─  views_val.py
   ├── Enantiomer_ranking
        └─  Enantiomer _work.ipynb     
   ├── QM7
        └─ qm7_work.ipynb       
├── Data/
│   ├── Enantiomer_ranking_dataset
│   │   └─   sample_test.pkl
        └─   sample_train.pkl
        └─   sample_val.pkl 
│   ├── QM7 dataset
│   │   └─ qm7.mat
├── Results/
└── README.md
```

---
## files

1) qm8_weighted_views (complete): This file contains the routine to generate weights and views of molecules.
2) qm8_additional.py (complete): This file contain switches to add a specific single add property to analysis.
3) qm8_analysis contains the file to run main analysis.
4) qm8.csv contains complete raw dataset.
5) qm8_processed.pkl contain atomic number and 3d coordinates of data. 
