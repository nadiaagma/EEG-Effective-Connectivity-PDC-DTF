"""
Input/output utilities for EEG Effective Connectivity Analysis.

This module handles dataset loading and validation.
"""

import pandas as pd

from config import (
    DATASET_DIR,
    PROTOCOLS,
    CHANNEL_START,
    CHANNEL_END,
)


def load_participants():
    """
    Load participant metadata from the dataset directory.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing participant information.
        Expected columns:
            - Subject
            - Group

    Raises
    ------
    FileNotFoundError
        If participants.csv cannot be found.
    """
    participant_file = DATASET_DIR / "participants.csv"

    if not participant_file.exists():
        raise FileNotFoundError(
            f"Participant file not found: {participant_file}"
        )

    return pd.read_csv(participant_file)


def load_subject_files(subject_id):
    """
    Get all protocol file paths for a subject.

    Parameters
    ----------
    subject_id : str
        Subject identifier (e.g., "S01").

    Returns
    -------
    dict
        Dictionary mapping protocol names to CSV file paths.

    Raises
    ------
    FileNotFoundError
        If the subject folder or any protocol file is missing.
    """
    subject_dir = DATASET_DIR / subject_id

    if not subject_dir.exists():
        raise FileNotFoundError(
            f"Subject folder not found: {subject_dir}"
        )

    protocol_files = {}

    for protocol in PROTOCOLS:
        file_path = subject_dir / f"{protocol}.csv"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing protocol file: {file_path}"
            )

        protocol_files[protocol] = file_path

    return protocol_files


def load_protocol(file_path):
    """
    Load EEG data from a protocol CSV file.

    Parameters
    ----------
    file_path : pathlib.Path
        Path to the protocol CSV file.

    Returns
    -------
    tuple
        A tuple containing:
            - eeg_data : numpy.ndarray
                EEG data with shape (n_channels, n_samples).
            - channel_names : list[str]
                List of EEG channel names.

    Raises
    ------
    ValueError
        If the CSV file is empty or contains invalid data.
    """
    df = pd.read_csv(file_path, sep=";")

    if df.empty:
        raise ValueError(
            f"Empty CSV file: {file_path}"
        )

    # Select EEG channels
    df = df.iloc[:, CHANNEL_START:CHANNEL_END]

    # Clean channel names
    channel_names = [
        column.split(" - ")[1].strip()
        if " - " in column
        else column.strip()
        for column in df.columns
    ]

    # Remove rows containing NaN values
    df = df.dropna()

    if df.empty:
        raise ValueError(
            f"No valid EEG samples after removing NaN values: {file_path}"
        )

    eeg_data = df.to_numpy(dtype=float).T

    return eeg_data, channel_names


def load_subject(subject_id: str) -> tuple:
    """
    Load all protocol recordings for a subject.

    Parameters
    ----------
    subject_id : str
        Subject identifier (e.g., "S01").

    Returns
    -------
    tuple
        A tuple containing:
            - protocol_data : dict
                Dictionary mapping protocol names to EEG arrays.
            - channel_names : list[str]
                EEG channel names.
    """
    protocol_files = load_subject_files(subject_id)

    protocol_data = {}
    channel_names = None

    for protocol in PROTOCOLS:
        eeg_data, channels = load_protocol(protocol_files[protocol])

        protocol_data[protocol] = eeg_data

        if channel_names is None:
            channel_names = channels

    return protocol_data, channel_names