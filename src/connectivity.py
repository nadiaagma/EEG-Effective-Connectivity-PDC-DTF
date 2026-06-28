"""
Effective connectivity estimation using PDC or DTF.
"""

import numpy as np

from config import (
    SFREQ,
)


def compute_connectivity(
    A,
    sigma,
    frequencies,
    method="dtf",
):
    """
    Compute effective connectivity using PDC or DTF.

    Parameters
    ----------
    A : numpy.ndarray
        MVAR coefficient matrices.

    sigma : numpy.ndarray
        Residual covariance matrix.

    frequencies : numpy.ndarray
        Frequency samples (Hz).

    method : str
        Connectivity method.
        Available:
            - "pdc"
            - "dtf"

    Returns
    -------
    numpy.ndarray
        Average connectivity matrix.
    """
    order, n_channels, _ = A.shape

    connectivity = np.zeros(
        (
            len(frequencies),
            n_channels,
            n_channels,
        )
    )

    for fi, frequency in enumerate(frequencies):

        A_f = np.eye(
            n_channels,
            dtype=complex,
        )

        for k in range(order):
            A_f -= (
                A[k]
                * np.exp(
                    -2j
                    * np.pi
                    * frequency
                    * (k + 1)
                    / SFREQ
                )
            )

        if method == "pdc":

            for i in range(n_channels):

                denominator = np.sqrt(
                    np.sum(
                        np.abs(A_f[:, i]) ** 2
                    )
                )

                if denominator > 1e-10:
                    connectivity[
                        fi,
                        :,
                        i,
                    ] = (
                        np.abs(A_f[:, i])
                        / denominator
                    )

        elif method == "dtf":

            try:

                H_f = np.linalg.inv(A_f)

                for i in range(n_channels):

                    denominator = np.sqrt(
                        np.sum(
                            np.abs(H_f[i, :]) ** 2
                        )
                    )

                    if denominator > 1e-10:
                        connectivity[
                            fi,
                            i,
                            :,
                        ] = (
                            np.abs(H_f[i, :])
                            / denominator
                        )

            except np.linalg.LinAlgError:
                pass

    connectivity = connectivity.mean(axis=0)

    np.fill_diagonal(
        connectivity,
        0,
    )

    return connectivity