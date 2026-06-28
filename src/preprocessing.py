"""
Preprocessing utilities for EEG Effective Connectivity Analysis.
"""

import mne
import numpy as np

from config import (
    SFREQ,
    BANDPASS_L_FREQ,
    BANDPASS_H_FREQ,
    EPOCH_LENGTH_SEC,
    EPOCH_OVERLAP_SEC,
)


def normalize_data(protocol_data):
    """
    Apply channel-wise z-score normalization across all protocols.

    Parameters
    ----------
    protocol_data : dict
        Dictionary mapping protocol names to EEG arrays.

    Returns
    -------
    tuple
        A tuple containing:
            - normalized_data : dict
                Channel-wise normalized EEG data.
            - channel_mean : numpy.ndarray
                Mean value of each EEG channel.
            - channel_std : numpy.ndarray
                Standard deviation of each EEG channel.
    """
    all_data = np.concatenate(
        list(protocol_data.values()),
        axis=1
    )

    channel_mean = all_data.mean(axis=1, keepdims=True)
    channel_std = all_data.std(axis=1, keepdims=True)

    # Prevent division by zero
    channel_std[channel_std < 1e-6] = 1.0

    normalized_data = {
        protocol: (data - channel_mean) / channel_std
        for protocol, data in protocol_data.items()
    }

    return normalized_data, channel_mean, channel_std


def bandpass_filter(
    eeg_data,
    channel_names,
    l_freq=BANDPASS_L_FREQ,
    h_freq=BANDPASS_H_FREQ,
    sfreq=SFREQ,
):
    """
    Apply FIR band-pass filtering.

    Parameters
    ----------
    eeg_data : numpy.ndarray
        EEG data with shape (n_channels, n_samples).

    channel_names : list[str]
        EEG channel names.

    Returns
    -------
    numpy.ndarray
        Filtered EEG data.
    """
    info = mne.create_info(
        channel_names,
        sfreq,
        ch_types="eeg",
    )

    raw = mne.io.RawArray(
        eeg_data,
        info,
        verbose=False,
    )

    raw.filter(
        l_freq=l_freq,
        h_freq=h_freq,
        method="fir",
        verbose=False,
    )

    return raw.get_data()


def create_epochs(
    eeg_data,
    epoch_length_sec=EPOCH_LENGTH_SEC,
    overlap_sec=EPOCH_OVERLAP_SEC,
    sfreq=SFREQ,
):
    """
    Segment EEG into overlapping epochs.

    Parameters
    ----------
    eeg_data : numpy.ndarray
        EEG data with shape (n_channels, n_samples).

    Returns
    -------
    list[numpy.ndarray]
        List of EEG epochs.
    """
    epoch_samples = int(epoch_length_sec * sfreq)
    overlap_samples = int(overlap_sec * sfreq)
    step = epoch_samples - overlap_samples

    _, n_samples = eeg_data.shape

    epochs = []
    start = 0

    while start + epoch_samples <= n_samples:
        epochs.append(
            eeg_data[:, start:start + epoch_samples]
        )
        start += step

    return epochs