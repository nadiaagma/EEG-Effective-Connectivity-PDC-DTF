"""
Export utilities for EEG Effective Connectivity Analysis.

This module contains helper functions for exporting
results to disk.
"""

from pathlib import Path
import pickle

import numpy as np
import pandas as pd

from config import MNI_COORDS


def save_checkpoint(
    results,
    checkpoint_file,
):
    """
    Save subject analysis checkpoint.

    Parameters
    ----------
    results : dict
        Subject analysis results.

    checkpoint_file : pathlib.Path
        Output checkpoint file.
    """
    checkpoint_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(checkpoint_file, "wb") as file:
        pickle.dump(results, file)


def load_checkpoint(
    checkpoint_file,
):
    """
    Load subject checkpoint.

    Parameters
    ----------
    checkpoint_file : pathlib.Path

    Returns
    -------
    dict
        Loaded checkpoint.
    """
    with open(checkpoint_file, "rb") as file:
        return pickle.load(file)


def save_bnv(
    matrix,
    channel_names,
    output_dir,
    filename,
    metric="net_flow",
):
    """
    Export BrainNet Viewer node and edge files.

    Parameters
    ----------
    matrix : numpy.ndarray
        Connectivity matrix.

    channel_names : list[str]
        EEG channel names.

    output_dir : pathlib.Path

    filename : str
        Output filename without extension.

    metric : str
        Node coloring metric.
    """
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    in_strength = matrix.sum(axis=1)
    out_strength = matrix.sum(axis=0)
    net_flow = out_strength - in_strength

    color = {
        "net flow": net_flow,
        "total strength": out_strength + in_strength,
        "out strength": out_strength,
        "in strength": in_strength,
    }.get(
        metric,
        net_flow,
    )

    max_value = np.abs(net_flow).max()

    if max_value > 0:
        size = 1 + 5 * np.abs(net_flow) / max_value
    else:
        size = np.ones(len(channel_names))

    node_file = output_dir / f"{filename}.node"
    edge_file = output_dir / f"{filename}.edge"

    with open(node_file, "w") as file:

        for i, channel in enumerate(channel_names):

            x, y, z = MNI_COORDS.get(
                channel.strip(),
                (0, 0, 0),
            )

            file.write(
                f"{x:.4f} "
                f"{y:.4f} "
                f"{z:.4f} "
                f"{color[i]:.6f} "
                f"{size[i]:.4f} "
                f"{channel.strip()}\n"
            )

    np.savetxt(
        edge_file,
        matrix,
        fmt="%.6f",
        delimiter="\t",
    )


def save_csv(
    records,
    output_file,
):
    """
    Save a list of dictionaries as CSV.

    Parameters
    ----------
    records : list[dict]

    output_file : pathlib.Path
    """
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe = pd.DataFrame(records)

    dataframe.to_csv(
        output_file,
        index=False,
    )


def save_matrix(
    matrix,
    output_file,
    fmt="%.6f",
):
    """
    Save connectivity matrix.

    Parameters
    ----------
    matrix : numpy.ndarray

    output_file : pathlib.Path

    fmt : str
        Numeric format.
    """
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.savetxt(
        output_file,
        matrix,
        fmt=fmt,
        delimiter=",",
    )