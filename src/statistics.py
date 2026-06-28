"""
Statistical analysis utilities.
"""

import numpy as np
import pandas as pd

from scipy.stats import mannwhitneyu
from scipy.stats import wilcoxon

from statsmodels.stats.multitest import multipletests


# ======================================================
# Basic Statistical Tests
# ======================================================

def mann_whitney_test(
    group_a,
    group_b,
    alternative="two-sided",
):
    """
    Perform Mann-Whitney U test.

    Returns
    -------
    tuple
        (u_statistic, p_value)
    """

    if (
        len(group_a) <= 1
        or len(group_b) <= 1
    ):
        return np.nan, np.nan

    return mannwhitneyu(
        group_a,
        group_b,
        alternative=alternative,
    )


def wilcoxon_test(
    values,
    alternative="greater",
):
    """
    Perform one-sample Wilcoxon signed-rank test.

    Returns
    -------
    tuple
        (w_statistic, p_value)
    """

    if (
        len(values) <= 1
        or all(v == 0 for v in values)
    ):
        return np.nan, np.nan

    try:

        return wilcoxon(
            values,
            alternative=alternative,
        )

    except ValueError:

        return np.nan, np.nan


# ======================================================
# FDR Correction
# ======================================================

def fdr_correction(
    dataframe,
    p_column="p-value",
    group_columns=None,
    alpha=0.05,
    method="fdr_bh",
):
    """
    Apply Benjamini-Hochberg FDR correction.
    """

    dataframe = dataframe.copy()

    dataframe["p-FDR"] = np.nan
    dataframe["Significant"] = False

    if group_columns is None:

        valid = dataframe[p_column].notna()

        if valid.sum() > 0:

            reject, pvals, _, _ = multipletests(
                dataframe.loc[valid, p_column],
                alpha=alpha,
                method=method,
            )

            dataframe.loc[valid, "p-FDR"] = pvals
            dataframe.loc[valid, "Significant"] = reject

        return dataframe

    for _, group in dataframe.groupby(group_columns):

        valid = group[p_column].notna()

        if valid.sum() == 0:
            continue

        reject, pvals, _, _ = multipletests(
            group.loc[valid, p_column],
            alpha=alpha,
            method=method,
        )

        dataframe.loc[
            group.loc[valid].index,
            "p-FDR",
        ] = pvals

        dataframe.loc[
            group.loc[valid].index,
            "Significant",
        ] = reject

    return dataframe


# ======================================================
# Helper Wrappers
# ======================================================

def compare_similarity_groups(
    addiction_values,
    normal_values,
):
    """
    Compare Within Addiction vs Within Normal.
    """

    u, p = mann_whitney_test(
        addiction_values,
        normal_values,
    )

    return {
        "U Statistic": u,
        "p-value": p,
    }


def test_excess_similarity(
    excess_values,
):
    """
    Test whether excess Jaccard similarity
    is significantly larger than zero.
    """

    w, p = wilcoxon_test(
        excess_values
    )

    return {
        "W Statistic": w,
        "p-value": p,
    }


def compare_global_metrics(
    addiction_values,
    normal_values,
):
    """
    Compare one global graph metric
    between groups.
    """

    u, p = mann_whitney_test(
        addiction_values,
        normal_values,
    )

    return {
        "U Statistic": u,
        "p-value": p,
    }


def compare_node_metrics(
    addiction_values,
    normal_values,
):
    """
    Compare one node metric
    between groups.
    """

    u, p = mann_whitney_test(
        addiction_values,
        normal_values,
    )

    return {
        "U Statistic": u,
        "p-value": p,
    }