"""
Group-level aggregation utilities.

This module provides helper functions for averaging
subject connectivity matrices and computing
group-level graph metrics.
"""

import numpy as np

from graph_metrics import (
    compute_weighted_metrics,
)

from local_metrics import (
    compute_node_metrics,
)
from threshold import apply_threshold


# ======================================================
# Subject Matrix Access
# ======================================================

def get_connectivity_matrix(
    subject_results,
    subject_id,
    protocol,
    band,
):
    """
    Retrieve a subject connectivity matrix.

    Parameters
    ----------
    subject_results : dict

    subject_id : str

    protocol : str

    band : str

    Returns
    -------
    numpy.ndarray
    """
    return (
        subject_results[subject_id]
        ["connectivity"][protocol][band]
    )


def get_thresholded_matrix(
    subject_results,
    subject_id,
    protocol,
    band,
):
    """
    Retrieve a subject thresholded connectivity matrix.

    Parameters
    ----------
    subject_results : dict

    subject_id : str

    protocol : str

    band : str

    Returns
    -------
    numpy.ndarray
    """
    return (
        subject_results[subject_id]
        ["thresholded"][protocol][band]
    )


# ======================================================
# Averaging
# ======================================================

def average_connectivity(
    subject_results,
    subjects,
    protocol,
    band,
):
    """
    Average raw connectivity matrices.

    Parameters
    ----------
    subject_results : dict

    subjects : list[str]

    protocol : str

    band : str

    Returns
    -------
    numpy.ndarray
    """

    matrices = [
        get_connectivity_matrix(
            subject_results,
            subject,
            protocol,
            band,
        )
        for subject in subjects
    ]

    return np.mean(
        matrices,
        axis=0,
    )


def average_thresholded(
    subject_results,
    subjects,
    protocol,
    band,
):
    """
    Average thresholded connectivity matrices.

    Parameters
    ----------
    subject_results : dict

    subjects : list[str]

    protocol : str

    band : str

    Returns
    -------
    numpy.ndarray
    """

    matrices = [
        get_thresholded_matrix(
            subject_results,
            subject,
            protocol,
            band,
        )
        for subject in subjects
    ]

    return np.mean(
        matrices,
        axis=0,
    )


def get_group_average(
    subject_results,
    subjects,
    protocol,
    band,
    thresholded=True,
):
    """
    Retrieve the average connectivity matrix
    for a subject group.

    Parameters
    ----------
    thresholded : bool
        If True, average thresholded matrices.
        Otherwise, average raw connectivity matrices.

    Returns
    -------
    numpy.ndarray
    """

    if thresholded:

        return average_thresholded(
            subject_results,
            subjects,
            protocol,
            band,
        )

    return average_connectivity(
        subject_results,
        subjects,
        protocol,
        band,
    )


# ======================================================
# Graph Metrics
# ======================================================

def compute_group_global_metrics(
    subject_results,
    subjects,
    protocol,
    band,
):
    """
    Compute weighted global metrics
    from an averaged thresholded matrix.

    Returns
    -------
    dict
    """

    matrix = get_group_average(
        subject_results,
        subjects,
        protocol,
        band,
        thresholded=True,
    )

    return compute_weighted_metrics(
        matrix,
    )


def compute_group_node_metrics(
    subject_results,
    subjects,
    protocol,
    band,
    channel_names,
):
    """
    Compute node-level metrics
    from an averaged thresholded matrix.

    Returns
    -------
    list[dict]
    """

    matrix = get_group_average(
        subject_results,
        subjects,
        protocol,
        band,
        thresholded=True,
    )

    return compute_node_metrics(
        matrix,
        channel_names,
    )


# ======================================================
# Convenience
# ======================================================

def summarize_group(
    subject_results,
    subjects,
    protocol,
    band,
    channel_names,
):

    matrices = [
        subject_results[s]["thresholded"][protocol][band]
        for s in subjects
    ]

    average_matrix = np.mean(
        matrices,
        axis=0,
    )

    thresholded_matrix, _, _ = apply_threshold(
        average_matrix
    )

    return {

        "matrix": thresholded_matrix,

        "channels": channel_names,

        "global_metrics":
            compute_weighted_metrics(
                thresholded_matrix,
            ),

        "node_metrics":
            compute_node_metrics(
                thresholded_matrix,
                channel_names,
            ),
    }