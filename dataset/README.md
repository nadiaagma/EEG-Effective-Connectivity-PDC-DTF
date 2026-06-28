# EEG Dataset

This directory contains the input EEG recordings required by the EEG Effective Connectivity Analysis pipeline.

The analysis is designed for the publicly available EEG dataset published by **Kang et al. (2021)**, which contains EEG recordings from adolescents with **Problematic Pornography Use (PPU)** and healthy controls during resting-state and executive function tasks.

---

# Dataset Source

This repository is built to process the dataset described in the following publication:

> Kang, X., Agastya, I. M. A., Handayani, D. O. D., Kit, M. H., & Rahman, A. W. B. A. (2021). *Electroencephalogram (EEG) dataset with porn addiction and healthy teenagers under rest and executive function task*. Data in Brief, 39, 107467.

**DOI**

https://doi.org/10.1016/j.dib.2021.107467

**Data Article**

https://www.sciencedirect.com/science/article/pii/S2352340921007496

Please cite the original publication if you use this dataset in your research.

---

# Dataset Overview

- **Participants:** 14 adolescents
  - 7 with Problematic Pornography Use (PPU)
  - 7 Healthy Controls

- **Sampling Frequency:** 250 Hz

- **EEG Channels Used in This Repository (10 channels)**

```
Fp1 Fp2

F7 F3 Fz F4 F8

C3 Cz C4
```

Although the original recordings contain 19 EEG channels, this repository analyzes only the frontocentral network consisting of the ten channels listed above.

---

# Experimental Protocols

Each participant contains five EEG recordings corresponding to the following experimental conditions.

| Protocol | Description |
|----------|-------------|
| EC | Eyes Closed (Baseline) |
| EO | Eyes Open (Baseline) |
| M | Memorization Task |
| ET | Executive Task (Pornographic Stimulus Exposure) |
| R | Recall Task |

---

# Expected Folder Structure

```
dataset/
│
├── participants.csv
│
├── S01/
│   ├── EC.csv
│   ├── EO.csv
│   ├── M.csv
│   ├── ET.csv
│   └── R.csv
│
├── S02/
│   └── ...
│
├── ...
│
└── S14/
    └── ...
```

---

# participants.csv

The participant metadata file must contain at least the following columns.

| Column | Description |
|---------|-------------|
| Subject | Subject identifier (e.g., S01) |
| Group | Addiction or Control |

Example:

| Subject | Group |
|---------|---------|
| S01 | Addiction |
| S02 | Addiction |
| ... | ... |
| S14 | Control |

---

# EEG Recording Format

Each protocol recording should be stored as a semicolon-separated CSV file.

Example:

```
Time;EEG Fp1;EEG Fp2;EEG F7;...;EEG Cz
```

The analysis automatically extracts the EEG channels specified in `src/config.py`.

Additional columns may exist in the CSV files and will be ignored according to the configured channel indices.

---

# Data Availability

The original EEG recordings are **not distributed with this repository**.

Users should obtain the dataset from the official publication referenced above and place the EEG recordings into this directory following the folder structure described in this document.

Only the participant metadata file (`participants.csv`) is included in this repository.

---

# Notes

The analysis pipeline assumes the following default configuration:

- Sampling frequency: **250 Hz**
- Five EEG recordings per participant
- One folder per participant
- Protocol filenames:
  - `EC.csv`
  - `EO.csv`
  - `M.csv`
  - `ET.csv`
  - `R.csv`

If your dataset uses different filenames, folder structures, or channel ordering, please update the corresponding parameters in:

```
src/config.py
```

or modify the loading procedures implemented in:

```
src/data_io.py
```

before running the analysis.