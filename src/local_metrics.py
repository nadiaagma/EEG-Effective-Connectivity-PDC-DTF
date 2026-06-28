"""
Node-level graph metrics for effective connectivity analysis.
"""

import numpy as np


def compute_node_metrics(matrix, channel_names):
    """
    Compute node-level metrics from a connectivity matrix.

    Parameters
    ----------
    matrix : numpy.ndarray
        Thresholded connectivity matrix.

    channel_names : list[str]
        EEG channel names.

    Returns
    -------
    list[dict]
        Node metrics for each EEG channel.
    """
    in_strength = matrix.sum(axis=1)
    out_strength = matrix.sum(axis=0)
    net_flow = out_strength - in_strength

    metrics = []

    for i, channel in enumerate(channel_names):

        metrics.append(
            {
                "Channel": channel,
                "Out strength": out_strength[i],
                "In strength": in_strength[i],
                "Net flow": net_flow[i],
            }
        )

    return metrics