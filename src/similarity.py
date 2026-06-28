"""
Similarity analysis utilities.

This module computes

- Binary Jaccard Similarity
- Expected Jaccard Similarity
- Excess Jaccard Similarity

for all subjects.
"""

import numpy as np

from config import (
    PROTOCOLS,
    FREQ_BANDS,
)


# ======================================================
# Basic Metrics
# ======================================================

def compute_network_density(matrix):
    """
    Compute graph density excluding self-connections.
    """
    n = matrix.shape[0]

    mask = ~np.eye(
        n,
        dtype=bool,
    )

    return float(
        (matrix[mask] > 0).sum()
        / mask.sum()
    )


def compute_jaccard(
    matrix_a,
    matrix_b,
):
    """
    Binary Jaccard similarity.
    """

    mask = ~np.eye(
        matrix_a.shape[0],
        dtype=bool,
    )

    a = (
        matrix_a > 0
    ).astype(int)[mask]

    b = (
        matrix_b > 0
    ).astype(int)[mask]

    union = np.sum(a | b)

    if union == 0:
        return 0.0

    return float(
        np.sum(a & b)
        / union
    )


def expected_jaccard(
    density_a,
    density_b,
):
    """
    Expected Jaccard similarity.
    """

    denominator = (
        density_a
        + density_b
        - density_a * density_b
    )

    if denominator <= 1e-10:
        return 0.0

    return float(
        density_a
        * density_b
        / denominator
    )


def excess_jaccard(
    observed,
    expected,
):
    """
    Excess Jaccard similarity.
    """

    return observed - expected


# ======================================================
# Similarity Matrix
# ======================================================

def build_similarity_matrix(
    subject_results,
    subjects,
    protocol,
    band,
):
    """
    Build observed and expected
    similarity matrices.
    """

    n = len(subjects)

    observed = np.zeros((n, n))
    expected = np.zeros((n, n))

    densities = {}

    for subject in subjects:

        matrix = (
            subject_results[subject]
            ["thresholded"][protocol][band]
        )

        densities[subject] = (
            compute_network_density(matrix)
        )

    for i in range(n):

        matrix_i = (
            subject_results[
                subjects[i]
            ]["thresholded"][protocol][band]
        )

        for j in range(n):

            matrix_j = (
                subject_results[
                    subjects[j]
                ]["thresholded"][protocol][band]
            )

            observed[i, j] = compute_jaccard(
                matrix_i,
                matrix_j,
            )

            if i != j:

                expected[i, j] = expected_jaccard(
                    densities[subjects[i]],
                    densities[subjects[j]],
                )

    excess = observed - expected

    return (
        observed,
        expected,
        excess,
    )


# ======================================================
# Group Similarity
# ======================================================

def split_similarity_groups(
    similarity_matrix,
    excess_matrix,
    subjects,
    group_lookup,
):
    """
    Split similarity values into

    - Within Addiction
    - Within Normal
    - Between Groups
    """

    within_addiction = []

    within_normal = []

    between_groups = []

    excess_addiction = []

    excess_normal = []

    excess_between = []

    n = len(subjects)

    for i in range(n):

        for j in range(i + 1, n):

            group_i = group_lookup[
                subjects[i]
            ]

            group_j = group_lookup[
                subjects[j]
            ]

            similarity = similarity_matrix[
                i,
                j,
            ]

            excess = excess_matrix[
                i,
                j,
            ]

            if (
                group_i == "Addiction"
                and group_j == "Addiction"
            ):

                within_addiction.append(
                    similarity
                )

                excess_addiction.append(
                    excess
                )

            elif (
                group_i == "Non-Addiction"
                and group_j == "Non-Addiction"
            ):

                within_normal.append(
                    similarity
                )

                excess_normal.append(
                    excess
                )

            else:

                between_groups.append(
                    similarity
                )

                excess_between.append(
                    excess
                )

    return {

        "Within Addiction":
            within_addiction,

        "Within Normal":
            within_normal,

        "Between Groups":
            between_groups,

        "Excess Within Addiction":
            excess_addiction,

        "Excess Within Normal":
            excess_normal,

        "Excess Between Groups":
            excess_between,
    }


# ======================================================
# High-Level API
# ======================================================

def run_similarity_analysis(
    subject_results,
    participants,
):
    """
    Run similarity analysis
    for every protocol and band.

    Returns
    -------
    dict
    """

    subjects = (
        participants["Subject"]
        .tolist()
    )

    group_lookup = dict(

        zip(
            participants["Subject"],
            participants["Group"],
        )

    )

    report = {}

    for protocol in PROTOCOLS:

        report[protocol] = {}

        for band in FREQ_BANDS:

            observed, expected, excess = (
                build_similarity_matrix(
                    subject_results,
                    subjects,
                    protocol,
                    band,
                )
            )

            split = split_similarity_groups(

                observed,

                excess,

                subjects,

                group_lookup,

            )

            report[protocol][band] = {

                "Observed":
                    observed,

                "Expected":
                    expected,

                "Excess":
                    excess,

                "Groups":
                    split,

            }

    return report