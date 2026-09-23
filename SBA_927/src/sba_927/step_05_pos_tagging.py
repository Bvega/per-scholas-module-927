"""Perform part-of-speech tagging on the original SBA 927 dataset."""

from pathlib import Path

import nltk
from nltk import pos_tag, sent_tokenize, word_tokenize


EXPECTED_RECORD_COUNT = 12


def ensure_nltk_resources() -> None:
    """Download each required NLTK data resource only when it is missing."""
    required_resources = {
        "punkt": "tokenizers/punkt",
        "punkt_tab": "tokenizers/punkt_tab",
        "averaged_perceptron_tagger": "taggers/averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng": (
            "taggers/averaged_perceptron_tagger_eng"
        ),
    }

    for resource_name, resource_path in required_resources.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            try:
                nltk.data.find(f"{resource_path}.zip")
            except LookupError:
                nltk.download(resource_name, quiet=True)


def load_original_records(dataset_path: Path) -> list[str]:
    """Read the UTF-8 dataset and return its non-empty original records."""
    lines = dataset_path.read_text(encoding="utf-8").splitlines()
    records = [line for line in lines if line.strip()]

    if len(records) != EXPECTED_RECORD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_RECORD_COUNT} records, but found {len(records)}."
        )

    return records


def tag_record(text: str) -> list[tuple[str, str]]:
    """Tokenize one record by sentence and assign a POS tag to each token."""
    tagged_tokens: list[tuple[str, str]] = []

    # Part-of-speech (POS) tagging identifies each token's grammatical role in
    # its sentence. Common tags include NN = noun, NNP = proper noun, VB = verb,
    # JJ = adjective, and RB = adverb.
    for sentence in sent_tokenize(text):
        tokens = word_tokenize(sentence)
        tagged_tokens.extend(pos_tag(tokens))

    return tagged_tokens


def print_pos_preview(
    records: list[str], tagged_records: list[list[tuple[str, str]]]
) -> None:
    """Print original text and POS-tagged tokens for three records only."""
    for record_number, (original_text, tagged_tokens) in enumerate(
        zip(records[:3], tagged_records[:3]), start=1
    ):
        print(f"Record {record_number} original text: {original_text}")
        print(f"Record {record_number} POS-tagged tokens: {tagged_tokens}")
        print()


def save_pos_results(
    output_path: Path, tagged_records: list[list[tuple[str, str]]]
) -> None:
    """Save POS-tagged tokens for every dataset record."""
    output_sections = []

    for record_number, tagged_tokens in enumerate(tagged_records, start=1):
        formatted_tokens = " ".join(
            f"{token}/{tag}" for token, tag in tagged_tokens
        )
        output_sections.append(
            f"Record {record_number}\nPOS-tagged tokens: {formatted_tokens}"
        )

    output_path.write_text("\n\n".join(output_sections) + "\n", encoding="utf-8")


def main() -> None:
    """Load, POS-tag, preview, and save all original text records."""
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "SBA927.txt"
    output_path = project_root / "outputs" / "pos_tags.txt"

    ensure_nltk_resources()
    records = load_original_records(dataset_path)
    tagged_records = [tag_record(record) for record in records]

    print_pos_preview(records, tagged_records)
    save_pos_results(output_path, tagged_records)


if __name__ == "__main__":
    main()
