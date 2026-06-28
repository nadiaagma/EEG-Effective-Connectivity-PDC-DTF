"""
Visualization utilities for EEG Effective Connectivity Analysis.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_connectivity_matrix(
    matrix,
    channel_names,
    title,
    output_file,
):
    """
    Plot a connectivity matrix.

    Parameters
    ----------
    matrix : numpy.ndarray

    channel_names : list[str]

    title : str

    output_file : pathlib.Path
    """
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(8, 7),
    )

    image = ax.imshow(
        matrix,
        cmap="viridis",
        vmin=0,
        vmax=1,
        origin="upper",
    )

    plt.colorbar(
        image,
        ax=ax,
        label="Connectivity Strength",
    )

    ax.set_xticks(
        range(len(channel_names))
    )
    ax.set_xticklabels(
        channel_names,
        rotation=45,
        ha="right",
    )

    ax.set_yticks(
        range(len(channel_names))
    )
    ax.set_yticklabels(
        channel_names,
    )

    ax.set_xlabel("Source")
    ax.set_ylabel("Target")
    ax.set_title(
        title,
        fontweight="bold",
    )

    for row in range(len(channel_names)):
        for col in range(len(channel_names)):

            value = matrix[row, col]

            ax.text(
                col,
                row,
                f"{value:.2f}",
                ha="center",
                va="center",
                fontsize=8,
                color="white"
                if value < 0.6
                else "black",
            )

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)


def plot_similarity_heatmap(
    similarity_matrix,
    labels,
    title,
    output_file,
):
    """
    Plot Jaccard similarity heatmap.

    Parameters
    ----------
    similarity_matrix : numpy.ndarray

    labels : list[str]

    title : str

    output_file : pathlib.Path
    """
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig, ax = plt.subplots(
        figsize=(10, 8),
    )

    image = ax.imshow(
        similarity_matrix,
        cmap="jet",
        vmin=0,
        vmax=0.6,
        origin="upper",
        aspect="auto",
    )

    plt.colorbar(
        image,
        ax=ax,
        label="Jaccard Similarity",
    )

    ax.set_xticks(
        range(len(labels))
    )

    ax.set_xticklabels(
        labels,
        rotation=45,
        ha="right",
        fontsize=9,
    )

    ax.set_yticks(
        range(len(labels))
    )

    ax.set_yticklabels(
        labels,
        fontsize=9,
    )

    for i in range(len(labels)):
        for j in range(len(labels)):

            value = similarity_matrix[i, j]

            ax.text(
                j,
                i,
                f"{value:.2f}",
                ha="center",
                va="center",
                fontsize=8,
                color="white"
                if value > 0.3
                else "black",
            )

    ax.set_xlabel("Subject")
    ax.set_ylabel("Subject")
    ax.set_title(
        title,
        fontweight="bold",
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)


def plot_global_metrics(
    group_results,
    metric,
    output_file,
):

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    protocols = ["EC", "EO", "M", "ET", "R"]
    bands = ["Theta", "Alpha", "Beta", "Gamma"]

    labels = []
    addiction = []
    control = []

    for protocol in protocols:

        for band in bands:

            labels.append(f"{protocol}-{band}")

            addiction.append(
                group_results["Addiction"][protocol][band]
                ["global_metrics"][metric]
            )

            control.append(
                group_results["Control"][protocol][band]
                ["global_metrics"][metric]
            )

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(
        x - width / 2,
        addiction,
        width,
        color="#ff7f0e",
        label="Addiction",
        edgecolor="black",
        linewidth=0,
        alpha=0.85,
    )

    ax.bar(
        x + width / 2,
        control,
        width,
        color="#1f77b4",
        label="Control",
        edgecolor="black",
        linewidth=0,
        alpha=0.85,
    )

    ax.set_title(
        metric,
        fontsize=14,
        fontweight="bold",
    )

    ax.set_ylabel(metric)

    ax.set_xlabel("Protocol - Band")

    ax.grid(
        axis="y",
        alpha=0.3,
        linestyle="--",
    )

    ax.legend()

    ax.set_xticks(x)

    ax.set_xticklabels(
        labels,
        rotation=45,
        ha="right",
        fontsize=9,
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)