"""
Multivariate Autoregressive (MVAR) model estimation utilities.
"""

import numpy as np
from scipy import linalg as scipy_linalg

from config import MVAR_ORDER

def fit_mvar(epoch, order):
    """
    Estimate MVAR coefficients for a single EEG epoch.

    Parameters
    ----------
    epoch : numpy.ndarray
        EEG epoch with shape (n_channels, n_samples).

    order : int
        MVAR model order.

    Returns
    -------
    tuple
        (A, sigma, bic)
    """
    n_channels, n_samples = epoch.shape
    n_obs = n_samples - order

    if n_obs <= n_channels * order:
        return None, None, np.inf

    Y = epoch[:, order:]

    X = np.zeros((n_channels * order, n_obs))

    for lag in range(order):
        col_start = order - lag - 1

        X[
            lag * n_channels:(lag + 1) * n_channels,
            :
        ] = epoch[:, col_start:col_start + n_obs]

    try:
        A_flat_T, _, _, _ = scipy_linalg.lstsq(
            X.T,
            Y.T,
            lapack_driver="gelsy",
        )

    except (
        ValueError,
        scipy_linalg.LinAlgError,
    ):
        return None, None, np.inf

    A_flat = A_flat_T.T

    A = np.stack(
        [
            A_flat[
                :,
                lag * n_channels:(lag + 1) * n_channels
            ]
            for lag in range(order)
        ],
        axis=0,
    )

    residuals = Y - A_flat @ X

    sigma = (residuals @ residuals.T) / n_obs

    det_sigma = np.linalg.det(sigma)

    if det_sigma <= 0:
        return A, sigma, np.inf

    k = order * n_channels ** 2

    bic = np.log(det_sigma) + (
        k * np.log(n_obs)
    ) / n_obs

    return A, sigma, bic


def estimate_mvar(
    epochs,
    order=MVAR_ORDER,
):
    """
    Estimate MVAR coefficients by averaging across epochs.

    Parameters
    ----------
    epochs : list[numpy.ndarray]
        List of EEG epochs.

    order : int
        MVAR model order.

    Returns
    -------
    tuple
        (A_mean, sigma_mean, order)
    """
    n_channels = epochs[0].shape[0]

    A_list = []
    sigma_list = []

    for epoch in epochs:

        epoch = np.nan_to_num(
            epoch,
            nan=0.0,
            posinf=0.0,
            neginf=0.0,
        )

        A, sigma, bic = fit_mvar(
            epoch,
            order,
        )

        if (
            A is not None
            and np.isfinite(bic)
        ):
            A_list.append(A)
            sigma_list.append(sigma)

    if not A_list:

        return (
            np.zeros(
                (
                    order,
                    n_channels,
                    n_channels,
                )
            ),
            np.eye(n_channels),
            order,
        )

    return (
        np.mean(A_list, axis=0),
        np.mean(sigma_list, axis=0),
        order,
    )