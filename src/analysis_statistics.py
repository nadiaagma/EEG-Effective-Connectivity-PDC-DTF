"""
High-level statistical analysis.

This module performs:

1. Similarity analysis
2. Wilcoxon analysis
3. Mann-Whitney analysis
"""

import numpy as np
import pandas as pd

from config import (
    PROTOCOLS,
    FREQ_BANDS,
)

from local_metrics import (
    compute_node_metrics,
)

from graph_metrics import (
    compute_weighted_metrics,
)

from similarity import (
    compute_network_density,
    compute_jaccard,
    expected_jaccard,
)

from statistics import (
    mann_whitney_test,
    wilcoxon_test,
    fdr_correction,
)


# ======================================================
# Similarity Analysis
# ======================================================

def run_similarity_analysis(
    subject_results,
    participants,
):
    """
    Compute Jaccard similarity between all subjects.

    Parameters
    ----------
    subject_results : dict

    participants : pandas.DataFrame

    Returns
    -------
    tuple
        (
            similarity_dataframe,
            wilcoxon_dataframe,
            saved_values,
        )
    """

    subjects = participants["Subject"].tolist()

    groups = {
        row.Subject: row.Group
        for _, row in participants.iterrows()
    }

    similarity_records = []

    wilcoxon_records = []

    saved_values = {}

    for protocol in PROTOCOLS:

        for band in FREQ_BANDS:

            print(
                f"Similarity: {protocol} {band}"
            )

            matrices = {

                subject:
                subject_results[subject]
                ["thresholded"][protocol][band]

                for subject in subjects

            }

            densities = {

                subject:
                compute_network_density(matrix)

                for subject, matrix
                in matrices.items()

            }

            n = len(subjects)

            similarity = np.zeros((n, n))

            expected = np.zeros((n, n))

            for i in range(n):

                for j in range(n):

                    similarity[i, j] = compute_jaccard(
                        matrices[subjects[i]],
                        matrices[subjects[j]],
                    )

                    if i != j:

                        expected[i, j] = expected_jaccard(
                            densities[subjects[i]],
                            densities[subjects[j]],
                        )

            excess = similarity - expected

            within_addiction = []
            within_normal = []
            between = []

            excess_addiction = []
            excess_normal = []
            excess_between = []

            for i in range(n):

                for j in range(i + 1, n):

                    g1 = groups[subjects[i]]
                    g2 = groups[subjects[j]]

                    value = similarity[i, j]

                    value_excess = excess[i, j]

                    if g1 == g2 == "Addiction":

                        within_addiction.append(value)
                        excess_addiction.append(value_excess)

                    elif g1 == g2 == "Control":

                        within_normal.append(value)
                        excess_normal.append(value_excess)

                    else:

                        between.append(value)
                        excess_between.append(value_excess)

            saved_values[(protocol, band)] = (
                within_addiction,
                within_normal,
                between,
            )

            expected_global = np.mean(

                [
                    expected_jaccard(
                        densities[subjects[i]],
                        densities[subjects[j]],
                    )

                    for i in range(n)

                    for j in range(i + 1, n)
                ]

            )

            similarity_records.append(

                {
                    "Protocol": protocol,
                    "Band": band,

                    "Within Addiction":
                        np.mean(within_addiction)
                        if within_addiction else np.nan,

                    "Within Normal":
                        np.mean(within_normal)
                        if within_normal else np.nan,

                    "Between Groups":
                        np.mean(between)
                        if between else np.nan,

                    "Excess Within Addiction":
                        np.mean(excess_addiction)
                        if excess_addiction else np.nan,

                    "Excess Within Normal":
                        np.mean(excess_normal)
                        if excess_normal else np.nan,

                    "Excess Between Groups":
                        np.mean(excess_between)
                        if excess_between else np.nan,
                }

            )

            labels = [
                f"{s} ({groups[s][0]})"
                for s in subjects
            ]


            for relation, values in [

                (
                    "Within Addiction",
                    excess_addiction,
                ),

                (
                    "Within Normal",
                    excess_normal,
                ),

                (
                    "Between Groups",
                    excess_between,
                ),

            ]:

                w, p = wilcoxon_test(values)

                wilcoxon_records.append(

                    {
                        "Protocol": protocol,
                        "Band": band,
                        "Group Relationship": relation,
                        "N Pairs": len(values),
                        "Mean Excess JI":
                            np.mean(values),
                        "W stats": w,
                        "p-value": p,
                    }

                )

    similarity_df = pd.DataFrame(
        similarity_records
    )

    wilcoxon_df = pd.DataFrame(
        wilcoxon_records
    )

    wilcoxon_df = fdr_correction(
        wilcoxon_df,
        p_column="p-value",
        group_columns=[
            "Group Relationship",
        ],
    )

    return (
        similarity_df,
        wilcoxon_df,
        saved_values,
    )


# ======================================================
# Mann-Whitney U Test (Similarity)
# ======================================================

def run_similarity_statistics(
    saved_values,
):
    """
    Mann-Whitney U test for
    Within Addiction vs Within Normal.

    Parameters
    ----------
    saved_values : dict

    Returns
    -------
    pandas.DataFrame
    """

    records = []

    for protocol in PROTOCOLS:

        for band in FREQ_BANDS:

            addiction, normal, between = (
                saved_values[(protocol, band)]
            )

            u_stat, p_value = mann_whitney_test(
                addiction,
                normal,
            )

            records.append(
                {
                    "Protocol": protocol,
                    "Band": band,

                    "N Pairs Addiction":
                        len(addiction),

                    "N Pairs Normal":
                        len(normal),

                    "Mean Addiction":
                        np.mean(addiction)
                        if len(addiction) > 0
                        else np.nan,

                    "Mean Normal":
                        np.mean(normal)
                        if len(normal) > 0
                        else np.nan,

                    "U stats":
                        u_stat,

                    "p-value":
                        p_value,
                }
            )

    dataframe = pd.DataFrame(records)

    dataframe = fdr_correction(
        dataframe,
        p_column="p-value",
    )

    return dataframe


# ======================================================
# Mann-Whitney U Test (Global Metrics)
# ======================================================


# ======================================================
# Global Metrics
# ======================================================

GLOBAL_METRICS = [
    "Global Efficiency",
    "Clustering Coefficient",
    "Modularity",
]


def build_global_metrics_dataframe(
    subject_results,
    participants,
    protocol_bands,
):
    """
    Build subject-level global metrics dataframe.
    """

    records = []

    groups = {
        row.Subject: row.Group
        for _, row in participants.iterrows()
    }

    for subject, result in subject_results.items():

        for protocol, bands in protocol_bands.items():

            for band in bands:

                matrix = result["thresholded"][protocol][band]

                metrics = compute_weighted_metrics(matrix)

                records.append({
                    "Subject": subject,
                    "Group": groups[subject],
                    "Protocol": protocol,
                    "Band": band,
                    **metrics,
                })

    return pd.DataFrame(records)


def run_global_metric_statistics(
    subject_results,
    participants,
    protocol_bands,
):
    """
    Mann-Whitney U test for global metrics.
    """

    global_df = build_global_metrics_dataframe(
        subject_results,
        participants,
        protocol_bands,
    )

    records = []

    for metric in GLOBAL_METRICS:

        for protocol, bands in protocol_bands.items():

            for band in bands:

                subset = global_df[
                    (global_df["Protocol"] == protocol)
                    &
                    (global_df["Band"] == band)
                ]

                addiction = subset[
                    subset["Group"] == "Addiction"
                ][metric].values

                control = subset[
                    subset["Group"] == "Control"
                ][metric].values

                u_stat, p_value = mann_whitney_test(
                    addiction,
                    control,
                )

                records.append({

                    "Metric": metric,

                    "Protocol": protocol,

                    "Band": band,

                    "Mean Addiction":
                        np.mean(addiction)
                        if len(addiction)
                        else np.nan,

                    "Mean Control":
                        np.mean(control)
                        if len(control)
                        else np.nan,

                    "U stats": u_stat,

                    "p-value": p_value,

                })

    dataframe = pd.DataFrame(records)

    dataframe = fdr_correction(
        dataframe,
        p_column="p-value",
        group_columns=[
            "Metric",
            "Protocol",
        ],
    )

    return global_df, dataframe


# ======================================================
# Node Metrics
# ======================================================

NODE_METRICS = [
    "Out strength",
    "In strength",
    "Net flow",
]


def build_node_metrics_dataframe(
    subject_results,
    participants,
    protocol_bands,
):
    """
    Build subject-level node metrics dataframe.
    """

    records = []

    groups = {
        row.Subject: row.Group
        for _, row in participants.iterrows()
    }

    channel_names = next(
        iter(subject_results.values())
    )["channels"]

    for subject, result in subject_results.items():

        for protocol, bands in protocol_bands.items():

            for band in bands:

                matrix = result["thresholded"][protocol][band]

                node_metrics = compute_node_metrics(
                    matrix,
                    channel_names,
                )

                for node in node_metrics:

                    records.append({

                        "Subject": subject,

                        "Group": groups[subject],

                        "Protocol": protocol,

                        "Band": band,

                        **node,

                    })

    return pd.DataFrame(records)


def run_node_metric_statistics(
    subject_results,
    participants,
    protocol_bands,
):
    """
    Mann-Whitney U test for node metrics.
    """

    node_df = build_node_metrics_dataframe(
        subject_results,
        participants,
        protocol_bands,
    )

    records = []

    for metric in NODE_METRICS:

        for protocol, bands in protocol_bands.items():

            for band in bands:

                subset = node_df[
                    (node_df["Protocol"] == protocol)
                    &
                    (node_df["Band"] == band)
                ]

                for channel in subset["Channel"].unique():

                    channel_df = subset[
                        subset["Channel"] == channel
                    ]

                    addiction = channel_df[
                        channel_df["Group"] == "Addiction"
                    ][metric].values

                    control = channel_df[
                        channel_df["Group"] == "Control"
                    ][metric].values

                    u_stat, p_value = mann_whitney_test(
                        addiction,
                        control,
                    )

                    records.append({

                        "Metric": metric,

                        "Protocol": protocol,

                        "Band": band,

                        "Channel": channel,

                        "Mean Addiction":
                            np.mean(addiction)
                            if len(addiction)
                            else np.nan,

                        "Mean Control":
                            np.mean(control)
                            if len(control)
                            else np.nan,

                        "U stats": u_stat,

                        "p-value": p_value,

                    })

    dataframe = pd.DataFrame(records)

    dataframe = fdr_correction(
        dataframe,
        p_column="p-value",
        group_columns=[
            "Metric",
            "Protocol",
            "Band",
        ],
    )

    return node_df, dataframe