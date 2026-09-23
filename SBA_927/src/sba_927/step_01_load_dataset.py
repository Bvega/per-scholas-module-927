"""Load the SBA 927 text dataset and display a basic inspection."""

from pathlib import Path


def main() -> None:
    """Load the dataset, count its records, and show the first three."""
    # This file is inside src/sba_927, so moving up two parent directories
    # locates the project root without relying on a computer-specific path.
    project_root = Path(__file__).resolve().parents[2]

    # Build a portable path to the dataset from the project root.
    dataset_path = project_root / "data" / "SBA927.txt"

    # Read the complete text as UTF-8, then split it into individual lines.
    lines = dataset_path.read_text(encoding="utf-8").splitlines()

    # Keep non-empty records while preserving the original text of each line.
    records = [line for line in lines if line.strip()]

    # Display the source path and a small sample for an initial inspection.
    print(f"Dataset file path: {dataset_path}")
    print(f"Number of text records: {len(records)}")
    print("First three records:")
    for record in records[:3]:
        print(record)


if __name__ == "__main__":
    main()
