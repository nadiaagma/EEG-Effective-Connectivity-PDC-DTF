"""
Graph metric utilities for effective connectivity analysis.
"""

import networkx as nx
import numpy as np
from networkx.algorithms import community as nx_community


def compute_binary_metrics(matrix):
    """
    Compute graph metrics from a binary adjacency matrix.

    Parameters
    ----------
    matrix : numpy.ndarray
        Binary adjacency matrix.

    Returns
    -------
    dict
        Graph metrics.
    """
    binary = (matrix > 0).astype(int)

    np.fill_diagonal(binary, 0)

    graph = nx.from_numpy_array(binary)

    metrics = {}

    metrics["Clustering Coefficient"] = (
        nx.average_clustering(graph)
        if graph.number_of_edges() > 0
        else 0.0
    )

    try:
        metrics["Global Efficiency"] = (
            nx.global_efficiency(graph)
        )

    except Exception:
        metrics["Global Efficiency"] = 0.0

    try:
        communities = (
            nx_community.greedy_modularity_communities(
                graph
            )
        )

        metrics["Modularity"] = (
            nx_community.modularity(
                graph,
                communities,
            )
        )

    except Exception:
        metrics["Modularity"] = 0.0

    return metrics


def compute_weighted_metrics(matrix):
    """
    Compute graph metrics from a weighted directed graph.

    Parameters
    ----------
    matrix : numpy.ndarray
        Weighted adjacency matrix.

    Returns
    -------
    dict
        Graph metrics.
    """
    weighted = matrix.copy()

    np.fill_diagonal(weighted, 0)

    graph = nx.from_numpy_array(
        weighted,
        create_using=nx.DiGraph,
    )

    metrics = {}

    metrics["Clustering Coefficient"] = (
        nx.average_clustering(
            graph,
            weight="weight",
        )
        if graph.number_of_edges() > 0
        else 0.0
    )

    try:

        n_nodes = len(graph)

        for _, _, edge in graph.edges(data=True):
            edge["distance"] = (
                1.0 / edge["weight"]
                if edge["weight"] > 0
                else float("inf")
            )

        efficiency_sum = 0.0

        if n_nodes > 1:

            lengths = dict(
                nx.all_pairs_dijkstra_path_length(
                    graph,
                    weight="distance",
                )
            )

            for source in graph:

                for target in graph:

                    if source == target:
                        continue

                    distance = lengths.get(
                        source,
                        {},
                    ).get(
                        target,
                        float("inf"),
                    )

                    if (
                        distance > 0
                        and distance != float("inf")
                    ):
                        efficiency_sum += (
                            1.0 / distance
                        )

            metrics["Global Efficiency"] = (
                efficiency_sum
                / (
                    n_nodes
                    * (n_nodes - 1)
                )
            )

        else:

            metrics["Global Efficiency"] = 0.0

    except Exception:

        metrics["Global Efficiency"] = 0.0

    try:

        communities = (
            nx_community.greedy_modularity_communities(
                graph,
                weight="weight",
            )
        )

        metrics["Modularity"] = (
            nx_community.modularity(
                graph,
                communities,
                weight="weight",
            )
        )

    except Exception:

        metrics["Modularity"] = 0.0

    return metrics