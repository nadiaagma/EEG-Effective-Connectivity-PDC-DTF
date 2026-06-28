"""
High-level visualization pipeline.

Generate all figures produced by the EEG analysis.
"""

from config import (
    VISUALIZATION_OUTPUT_DIR,
)

from visualization import (
    plot_connectivity_matrix,
    plot_global_metrics,
)


# ======================================================
# Group Connectivity
# ======================================================

def visualize_group_connectivity(
    group_results,
):
    """
    Generate average connectivity matrix figures
    for every group, protocol, and frequency band.
    """

    for group, protocols in group_results.items():

        for protocol, bands in protocols.items():

            for band, summary in bands.items():

                output = (
                    VISUALIZATION_OUTPUT_DIR
                    / "Connectivity"
                    / group
                    / protocol
                    / f"{band}.png"
                )

                channel_names = [
                    node["Channel"]
                    for node in summary["node_metrics"]
                ]

                plot_connectivity_matrix(
                    summary["matrix"],
                    channel_names,
                    f"{group} | {protocol} | {band}",
                    output,
                )


# ======================================================
# Global Metrics
# ======================================================

def visualize_global_statistics(
    group_results,
):

    metrics = [

        "Global Efficiency",

        "Clustering Coefficient",

        "Modularity",

    ]

    for metric in metrics:

        output = (
            VISUALIZATION_OUTPUT_DIR
            / "Global Metrics"
            / f"{metric}.png"
        )

        plot_global_metrics(
            group_results,
            metric,
            output,
        )


def visualize_all(
    group_results,
):

    print("\nGenerating visualizations...")

    visualize_group_connectivity(
        group_results,
    )

    visualize_global_statistics(
        group_results,
    )

    print("Visualization completed.")


# ======================================================
# Complete Visualization
# ======================================================

def visualize_all(
    group_results,
):
    """
    Generate every visualization.
    """

    print("\nGenerating visualizations...")

    visualize_group_connectivity(
        group_results,
    )

    visualize_global_statistics(
        group_results,
    )

    print("Visualization completed.")