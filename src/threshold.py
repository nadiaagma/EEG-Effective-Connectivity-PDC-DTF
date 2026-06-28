"""
Thresholding utilities for connectivity matrices.
"""

import numpy as np

from config import THRESHOLD_PERCENTILE


def apply_threshold(
    matrix,
    percentile=THRESHOLD_PERCENTILE,
):
    """
    Apply proportional thresholding to a connectivity matrix.

    Parameters
    ----------
    matrix : numpy.ndarray
        Connectivity matrix.

    percentile : float
        Threshold percentile.

    Returns
    -------
    tuple
        (
            thresholded_matrix,
            threshold_value,
            n_connections,
        )
    """
    mask = ~np.eye(
        matrix.shape[0],
        dtype=bool,
    )

    threshold_value = np.percentile(
        matrix[mask],
        percentile,
    )

    thresholded = matrix.copy()

    thresholded[
        thresholded < threshold_value
    ] = 0

    np.fill_diagonal(
        thresholded,
        0,
    )

    n_connections = int(
        np.sum(
            thresholded[mask] > 0
        )
    )

    return (
        thresholded,
        threshold_value,
        n_connections,
    )