"""
High-level export utilities.

This module exports all analysis results to disk.
"""

from pathlib import Path

from config import (
    SUBJECT_OUTPUT_DIR,
    GROUP_OUTPUT_DIR,
    SIMILARITY_OUTPUT_DIR,
    STATISTICS_OUTPUT_DIR,
)

from export import (
    save_csv,
    save_matrix,
    save_bnv,
)


# ======================================================
# Subject Results
# ======================================================

def export_subject_results(subject_results):
    """
    Export every subject connectivity matrix.

    Parameters
    ----------
    subject_results : dict
    """

    for subject, result in subject_results.items():

        subject_dir = SUBJECT_OUTPUT_DIR / subject

        channel_names = result["channels"]

        for protocol, bands in result["connectivity"].items():

            protocol_dir = subject_dir / protocol

            for band, matrix in bands.items():

                save_matrix(
                    matrix,
                    protocol_dir /
                    f"{band}_connectivity.csv",
                )

                thresholded = (
                    result["thresholded"]
                    [protocol][band]
                )

                save_matrix(
                    thresholded,
                    protocol_dir /
                    f"{band}_thresholded.csv",
                )

                save_bnv(
                    thresholded,
                    channel_names,
                    protocol_dir,
                    f"{band}",
                )


# ======================================================
# Group Results
# ======================================================

def export_group_results(group_results):
    """
    Export averaged group matrices.

    Parameters
    ----------
    group_results : dict
    """

    for group, protocols in group_results.items():

        group_dir = GROUP_OUTPUT_DIR / group

        for protocol, bands in protocols.items():

            protocol_dir = group_dir / protocol

            for band, summary in bands.items():

                matrix = summary["matrix"]

                save_matrix(
                    matrix,
                    protocol_dir /
                    f"{band}.csv",
                )

                channel_names = [
                    node["Channel"]
                    for node in summary["node_metrics"]
                ]

                save_bnv(
                    matrix,
                    channel_names,
                    protocol_dir,
                    band,
                )


# ======================================================
# Similarity
# ======================================================

def export_similarity(
    similarity_df,
    wilcoxon_df,
):
    """
    Export similarity analysis.

    Parameters
    ----------
    similarity_df : pandas.DataFrame

    wilcoxon_df : pandas.DataFrame
    """

    save_csv(
        similarity_df.to_dict("records"),
        SIMILARITY_OUTPUT_DIR /
        "Similarity Analysis.csv",
    )

    save_csv(
        wilcoxon_df.to_dict("records"),
        SIMILARITY_OUTPUT_DIR /
        "Wilcoxon Excess Similarity.csv",
    )


# ======================================================
# Statistics
# ======================================================

def export_statistics(
    similarity_statistics,
    global_statistics,
    node_statistics,
    global_metrics_df,
    node_metrics_df,
):
    """
    Export statistical analysis.

    Parameters
    ----------
    similarity_statistics : pandas.DataFrame

    global_statistics : pandas.DataFrame

    node_statistics : pandas.DataFrame

    global_metrics_df : pandas.DataFrame

    node_metrics_df : pandas.DataFrame
    """

    save_csv(
        similarity_statistics.to_dict("records"),
        STATISTICS_OUTPUT_DIR /
        "MWU Similarity.csv",
    )

    save_csv(
        global_statistics.to_dict("records"),
        STATISTICS_OUTPUT_DIR /
        "MWU Global Metrics.csv",
    )

    save_csv(
        node_statistics.to_dict("records"),
        STATISTICS_OUTPUT_DIR /
        "MWU Node Metrics.csv",
    )

    save_csv(
        global_metrics_df.to_dict("records"),
        STATISTICS_OUTPUT_DIR / "Global Metrics.csv",
    )

    save_csv(
        node_metrics_df.to_dict("records"),
        STATISTICS_OUTPUT_DIR / "Node Metrics.csv",
    )

# ======================================================
# Complete Export
# ======================================================

def export_all(
    subject_results,
    group_results,
    similarity_df,
    wilcoxon_df,
    similarity_statistics,
    global_statistics,
    node_statistics,
    global_metrics_df,
    node_metrics_df,
):
    """
    Export every analysis output.

    Parameters
    ----------
    subject_results : dict

    group_results : dict

    similarity_df : pandas.DataFrame

    wilcoxon_df : pandas.DataFrame

    similarity_statistics : pandas.DataFrame

    global_statistics : pandas.DataFrame

    node_statistics : pandas.DataFrame
    """

    print("\nExporting subject results...")

    export_subject_results(
        subject_results,
    )

    print("Exporting group results...")

    export_group_results(
        group_results,
    )

    print("Exporting similarity results...")

    export_similarity(
        similarity_df,
        wilcoxon_df,
    )

    print("Exporting statistical results...")

    export_statistics(
        similarity_statistics,
        global_statistics,
        node_statistics,
        global_metrics_df,
        node_metrics_df,
    )

    print("Export completed.")