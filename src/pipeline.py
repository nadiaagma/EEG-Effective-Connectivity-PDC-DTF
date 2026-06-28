"""
Processing pipeline for a single EEG subject.
"""

import numpy as np

from config import (
    PROTOCOLS,
    FREQ_BANDS,
    METHOD,
)

from data_io import load_subject

from preprocessing import (
    normalize_data,
    bandpass_filter,
    create_epochs,
)

from mvar import estimate_mvar

from connectivity import compute_connectivity
from threshold import apply_threshold


def process_subject(subject_id):
    """
    Process one subject from raw EEG to connectivity matrices.

    Parameters
    ----------
    subject_id : str
        Subject identifier.

    Returns
    -------
    dict
        Dictionary containing connectivity matrices for all
        protocols and frequency bands.
    """

    # --------------------------------------------------
    # Load subject
    # --------------------------------------------------

    protocol_data, channel_names = load_subject(subject_id)

    # --------------------------------------------------
    # Normalize
    # --------------------------------------------------

    normalized_data, channel_mean, channel_std = normalize_data(
        protocol_data
    )

    # --------------------------------------------------
    # Band-pass filtering
    # --------------------------------------------------

    filtered_data = {
        protocol: bandpass_filter(
            eeg_data,
            channel_names,
        )
        for protocol, eeg_data in normalized_data.items()
    }

    # --------------------------------------------------
    # Connectivity estimation
    # --------------------------------------------------

    connectivity_results = {}
    threshold_results = {}

    for protocol in PROTOCOLS:

        epochs = create_epochs(
            filtered_data[protocol]
        )

        A, sigma, _ = estimate_mvar(epochs)

        connectivity_results[protocol] = {}
        threshold_results[protocol] = {}

        for band, (low, high) in FREQ_BANDS.items():

            frequencies = np.linspace(
                low,
                high,
                20,
            )

            connectivity_matrix = compute_connectivity(
                A,
                sigma,
                frequencies,
                method=METHOD,
            )

            thresholded_matrix, _, _ = apply_threshold(
                connectivity_matrix
            )

            connectivity_results[protocol][band] = connectivity_matrix

            threshold_results[protocol][band] = thresholded_matrix

    return {
        "subject": subject_id,

        "channels": channel_names,

        "protocols": PROTOCOLS,

        "connectivity": connectivity_results,

        "thresholded": threshold_results,

        "normalization": {
            "mean": channel_mean,
            "std": channel_std,
        },
    }