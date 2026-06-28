"""
Main analysis pipeline.

This script performs:

1. Load participant metadata
2. Process every EEG subject
3. Store all subject-level results

Group analysis, visualization, and statistical analysis
are performed after subject processing.
"""

from data_io import load_participants

from aggregation import summarize_group
from pipeline import process_subject

from config import (
    PROTOCOLS,
    FREQ_BANDS,
)

from analysis_statistics import (
    run_similarity_analysis,
    run_similarity_statistics,
    run_global_metric_statistics,
    run_node_metric_statistics,
)

from analysis_export import (
    export_all,
)

from analysis_visualization import (
    visualize_all,
)

STAT_PROTOCOL_BANDS = {
    "EC": ["Alpha", "Beta"],
    "EO": ["Alpha", "Beta"],
    "M": ["Theta", "Gamma"],
    "ET": ["Beta", "Gamma"],
    "R": ["Theta", "Gamma"],
}

def run_subject_analysis():
    """
    Process every participant individually.

    Returns
    -------
    tuple
        (
            subject_results,
            failed_subjects,
        )
    """

    participants = load_participants()

    total_subjects = len(participants)

    subject_results = {}

    failed_subjects = []

    print("=" * 60)
    print("Subject-level EEG Analysis")
    print("=" * 60)

    for index, (_, row) in enumerate(
        participants.iterrows(),
        start=1,
    ):

        subject = row["Subject"]

        print(
            f"\n[{index}/{total_subjects}] Processing {subject}"
        )

        try:

            result = process_subject(subject)

            subject_results[subject] = result

            print("Done.")

        except Exception as error:

            failed_subjects.append(subject)

            print(f"Failed: {subject}")
            print(error)

    print("\n" + "=" * 60)
    print("Subject Analysis Finished")
    print("=" * 60)

    print(
        f"Successfully processed: "
        f"{len(subject_results)}/{total_subjects}"
    )

    if failed_subjects:

        print()

        print(
            "Failed subjects:"
        )

        for subject in failed_subjects:

            print(f" - {subject}")

    return (
        subject_results,
        failed_subjects,
    )


def run_group_analysis(subject_results):
    """
    Compute group-level connectivity matrices and graph metrics.

    Parameters
    ----------
    subject_results : dict

    Returns
    -------
    dict
    """

    print("\n" + "=" * 60)
    print("Group-level Analysis")
    print("=" * 60)

    participants = load_participants()

    groups = {}

    for _, row in participants.iterrows():

        group = row["Group"]
        subject = row["Subject"]

        groups.setdefault(group, []).append(subject)

    print()

    for group, members in groups.items():

        print(
            f"{group}: {len(members)} subjects"
        )

    channel_names = next(
        iter(subject_results.values())
    )["channels"]

    group_results = {}

    for group_name, members in groups.items():

        print(f"\nProcessing group: {group_name}")

        group_results[group_name] = {}

        for protocol in PROTOCOLS:

            group_results[group_name][protocol] = {}

            for band in FREQ_BANDS:

                summary = summarize_group(
                    subject_results,
                    members,
                    protocol,
                    band,
                    channel_names,
                )

                group_results[group_name][protocol][band] = summary

                print(
                    f"  {protocol:>2} | {band:<6} Done"
                )

    return group_results


def main():
    """
    Execute the complete analysis pipeline.
    """

    subject_results, failed_subjects = (
        run_subject_analysis()
    )

    print(subject_results.keys())

    group_results = run_group_analysis(
        subject_results
    )

    participants = load_participants()

    similarity_df, wilcoxon_df, saved_values = (
        run_similarity_analysis(
            subject_results,
            participants,
        )
    )

    similarity_statistics = (
        run_similarity_statistics(
            saved_values,
        )
    )

    global_metrics_df, global_statistics = (
        run_global_metric_statistics(
            subject_results,
            participants,
            STAT_PROTOCOL_BANDS,
        )
    )

    node_metrics_df, node_statistics = (
        run_node_metric_statistics(
            subject_results,
            participants,
            STAT_PROTOCOL_BANDS,
        )
    )

    print("\nExporting results...")

    export_all(
        subject_results=subject_results,
        group_results=group_results,
        similarity_df=similarity_df,
        wilcoxon_df=wilcoxon_df,
        similarity_statistics=similarity_statistics,
        global_statistics=global_statistics,
        node_statistics=node_statistics,
        global_metrics_df=global_metrics_df,
        node_metrics_df=node_metrics_df,
    )

    visualize_all(
        group_results,
    )

    return {
        "subjects": subject_results,
        "groups": group_results,
        "similarity": similarity_df,
        "wilcoxon": wilcoxon_df,
        "similarity_statistics": similarity_statistics,
        "global_statistics": global_statistics,
        "node_statistics": node_statistics,
        "global_metrics": global_metrics_df,
        "node_metrics": node_metrics_df,
    }

if __name__ == "__main__":

    main()