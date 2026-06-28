from pathlib import Path

#Protocols
PROTOCOLS = ['EC', 'EO', 'M', 'ET', 'R']
PROTOCOL_NAMES = {
    'EC': 'Baseline Eyes Closed', 
    'EO': 'Baseline Eyes Open',
    'M' : 'Memory Task',
    'ET': 'Executive Task (Pornographic Images)',
    'R' : 'Recall Task',
}

# EEG Parameters 
SFREQ      = 250         
FREQ_BANDS = {
    'Theta': (4, 8),
    'Alpha': (8, 13),
    'Beta': (13, 30),
    'Gamma': (30, 40),
}
# CSV columns containing EEG channels
CHANNEL_START = 4
CHANNEL_END   = 14 

# MNI Coordinates for BNV (in mm)
MNI_COORDS = {
    'Fp1': (-24.54,  66.41,  11.97), 'Fp2': ( 25.25,  66.62,  12.19), 'F7' : (-56.68,  30.50,   4.33),
    'F8' : ( 59.39,  27.37,   6.97), 'F3' : (-38.23,  34.47,  46.92), 'F4' : ( 38.59,  34.99,  48.23),
    'Fz' : (  0.88,  34.43,  62.21), 'C3' : (-50.88, -21.18,  59.95), 'C4' : ( 50.78, -23.18,  63.58), 
    'Cz' : ( -0.47, -24.64,  80.16),
}

# MVAR, Connectivity, and Threshold Configuration
BANDPASS_L_FREQ = 1.0          
BANDPASS_H_FREQ = 40       
EPOCH_LENGTH_SEC = 2.0     
EPOCH_OVERLAP_SEC = 0.5    
MVAR_ORDER = 20   
METHOD = 'pdc' # Available: "pdc", "dtf"
THRESHOLD_PERCENTILE = 85             
DENSITY = 0.15

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "dataset"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# ======================================================
# Output Directories
# ======================================================

CHECKPOINT_DIR = OUTPUT_DIR / "checkpoints"

SUBJECT_OUTPUT_DIR = OUTPUT_DIR / "subject"

GROUP_OUTPUT_DIR = OUTPUT_DIR / "group"

SIMILARITY_OUTPUT_DIR = OUTPUT_DIR / "similarity"

STATISTICS_OUTPUT_DIR = OUTPUT_DIR / "statistics"

VISUALIZATION_OUTPUT_DIR = OUTPUT_DIR / "figures"

BNV_OUTPUT_DIR = OUTPUT_DIR / "brainnet"