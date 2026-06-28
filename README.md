# EEG Effective Connectivity of the Frontocentral Network in Adolescents with Problematic Pornography Use Using Partial Directed Coherence and Directed Transfer Function

EEG Effective Connectivity Analysis using **Partial Directed Coherence (PDC)** and **Directed Transfer Function (DTF)** to investigate alterations in the frontocentral brain network of adolescents with **Problematic Pornography Use (PPU)**.

---

# Overview

This repository provides a complete EEG analysis pipeline for estimating effective brain connectivity from multichannel EEG recordings using **Multivariate Autoregressive (MVAR)** modeling.

The framework compares **Partial Directed Coherence (PDC)** and **Directed Transfer Function (DTF)** to investigate alterations in the frontocentral network associated with **Problematic Pornography Use (PPU)**. The pipeline covers every stage of the analysis, from EEG preprocessing and connectivity estimation to graph theoretical analysis, statistical testing, visualization, and BrainNet Viewer export.

---

# Dataset

This repository is designed to process a publicly available EEG dataset consisting of adolescent participants.

## Participants

* 14 adolescents

  * 7 Problematic Pornography Use (PPU)
  * 7 Healthy Controls

## EEG Recording

Sampling Frequency

```
250 Hz
```

Selected EEG Channels

```
Fp1
Fp2
F7
F8
F3
F4
Fz
C3
C4
Cz
```

Experimental Protocols

| Code | Description                        |
| ---- | ---------------------------------- |
| EC   | Eyes Closed (Baseline)             |
| EO   | Eyes Open (Baseline)               |
| M    | Memorization Task                  |
| ET   | Executive Task (Stimulus Exposure) |
| R    | Recall Task (Post-Stimulus)        |

---

# Features & Processing Pipeline

The repository executes the following automated analysis pipeline.

## EEG Preprocessing

* Per-channel Z-score normalization
* FIR bandpass filtering (1–40 Hz)
* Sliding-window epoch segmentation

## MVAR Estimation

* Multivariate Autoregressive (MVAR) model estimation

## Effective Connectivity Estimation

* Partial Directed Coherence (PDC)
* Directed Transfer Function (DTF)

## Network Thresholding

* Density-based proportional thresholding

## Graph Analysis

Global Metrics

* Global Efficiency
* Clustering Coefficient
* Modularity

Node Metrics

* In-strength
* Out-strength
* Net Flow

## Similarity Analysis

* Jaccard Similarity
* Expected Jaccard Similarity
* Excess Jaccard Similarity

## Statistical Analysis

* Mann–Whitney U Test
* Wilcoxon Signed-Rank Test
* Benjamini–Hochberg False Discovery Rate (FDR) correction

## Visualization & Export

Automatically generates

* Connectivity heatmaps
* CSV reports
* Statistical summaries
* BrainNet Viewer (.node/.edge) files

---

# Configuration

All configurable parameters are defined in

```
src/config.py
```

| Parameter           | Default Value             |
| ------------------- | ------------------------- |
| Sampling Rate       | 250 Hz                    |
| Bandpass Filter     | 1–40 Hz                   |
| Epoch Window        | 2 s (0.5 s overlap)       |
| MVAR Order          | 20                        |
| Threshold Density   | 0.15                      |
| Connectivity Method | PDC / DTF                 |
| Frequency Bands     | Theta, Alpha, Beta, Gamma |

---

# Repository Structure

```text
EEG-Effective-Connectivity-PDC-DTF/
├── dataset/
│   ├── participants.csv
│   └── EEG recordings
│
├── examples/
│
├── outputs/
│   ├── subject/
│   ├── group/
│   ├── similarity/
│   ├── statistics/
│   ├── figures/
│   └── checkpoints/
│
├── src/
│   ├── analysis.py
│   ├── analysis_export.py
│   ├── analysis_statistics.py
│   ├── analysis_visualization.py
│   ├── aggregation.py
│   ├── config.py
│   ├── connectivity.py
│   ├── data_io.py
│   ├── export.py
│   ├── graph_metrics.py
│   ├── local_metrics.py
│   ├── mvar.py
│   ├── pipeline.py
│   ├── preprocessing.py
│   ├── similarity.py
│   ├── statistics.py
│   ├── threshold.py
│   └── visualization.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

# Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/EEG-Effective-Connectivity-PDC-DTF.git

cd EEG-Effective-Connectivity-PDC-DTF
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

Main dependencies include

* NumPy
* SciPy
* Pandas
* Matplotlib
* NetworkX
* MNE-Python
* Statsmodels

---

## 3. Run the complete analysis

```bash
python run_analysis.py
```

The pipeline automatically performs

* EEG preprocessing
* MVAR estimation
* Effective connectivity estimation
* Graph analysis
* Similarity analysis
* Statistical analysis
* Visualization
* BrainNet Viewer export

---

# Generated Outputs

Upon successful execution, the pipeline populates the `outputs/` directory with the following results.

## Connectivity Outputs

* Subject-level connectivity matrices
* Group-average connectivity matrices
* Thresholded connectivity matrices
* BrainNet Viewer (.node / .edge) files

## Statistical Reports

* Similarity Analysis
* Wilcoxon Excess Similarity
* Mann–Whitney U Similarity
* Mann–Whitney U Global Metrics
* Mann–Whitney U Node Metrics
* Global Metrics
* Node Metrics

## Figures

Publication-ready figures including

* Connectivity heatmaps
* Group-average connectivity matrices
* Graph metric comparisons
* Similarity visualizations

---

# BrainNet Viewer

The repository automatically exports

```
.node

.edge
```

files compatible with **BrainNet Viewer**, allowing three-dimensional visualization of effective brain connectivity networks.

---

# Citation

If you use this repository or its methodology in your research, please cite:

> Nadia. *EEG Effective Connectivity of the Frontocentral Network in Adolescents with Problematic Pornography Use Using Partial Directed Coherence and Directed Transfer Function.* Bachelor's Thesis, Department of Electrical Engineering and Information Technology, Faculty of Engineering, Universitas Gadjah Mada, Yogyakarta, Indonesia, 2026.

---

# Author

**Nadia**

Department of Electrical Engineering and Information Technology

Faculty of Engineering

Universitas Gadjah Mada

Yogyakarta, Indonesia

---

# Acknowledgements

This work was completed as part of an undergraduate research project at the **Department of Electrical Engineering and Information Technology, Faculty of Engineering, Universitas Gadjah Mada**.

The implementation utilizes several outstanding open-source scientific software packages, including

* MNE-Python
* NumPy
* SciPy
* Pandas
* Matplotlib
* NetworkX
* Statsmodels
* BrainNet Viewer

---

# License

This project is released under the **MIT License**.

See the `LICENSE` file for more information.
