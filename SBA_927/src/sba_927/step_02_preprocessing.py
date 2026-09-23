"""Tokenize and preprocess the SBA 927 dataset with NLTK."""

from pathlib import Path

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def ensure_nltk_resources() -> None:
    """Download required NLTK data files only when they are unavailable."""
    required_resources = {
        "punkt": "tokenizers/punkt",
        "punkt_tab": "tokenizers/punkt_tab",
        "stopwords": "corpora/stopwords",
    }

    for resource_name, resource_path in required_resources.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)


def load_text_records(dataset_path: Path) -> list[str]:
    """Read the UTF-8 dataset and return only its non-empty lines."""
    lines = dataset_path.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.strip()]


def preprocess_record(text: str, english_stop_words: set[str]) -> list[str]:
    """Convert one text record into normalized, meaningful word tokens."""
    # Tokenization divides the original text into individual word-like units.
    tokens = word_tokenize(text)

    # Normalization converts every token to lowercase so differently capitalized
    # forms of the same word are treated consistently.
    normalized_tokens = [token.lower() for token in tokens]

    # Keeping alphabetic tokens removes punctuation, numbers, and other noise.
    alphabetic_tokens = [token for token in normalized_tokens if token.isalpha()]

    # Stop-word removal excludes common English words that usually carry little
    # meaning for text analysis, such as "the", "and", and "is".
    return [
        token for token in alphabetic_tokens if token not in english_stop_words
    ]


def save_processed_records(
    processed_records: list[list[str]], output_path: Path
) -> None:
    """Save every processed record as a space-separated line of tokens."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_text = "\n".join(" ".join(tokens) for tokens in processed_records)
    output_path.write_text(f"{output_text}\n", encoding="utf-8")


def print_record_preview(
    original_records: list[str], processed_records: list[list[str]]
) -> None:
    """Print the original and processed forms of the first three records."""
    for record_number, (original, processed) in enumerate(
        zip(original_records[:3], processed_records[:3]), start=1
    ):
        print(f"Record {record_number} original: {original}")
        print(f"Record {record_number} processed tokens: {processed}")
        print()


def main() -> None:
    """Load, preprocess, preview, and save the SBA 927 text records."""
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "SBA927.txt"
    output_path = project_root / "outputs" / "preprocessed_text.txt"

    ensure_nltk_resources()
    records = load_text_records(dataset_path)
    english_stop_words = set(stopwords.words("english"))
    processed_records = [
        preprocess_record(record, english_stop_words) for record in records
    ]

    print_record_preview(records, processed_records)
    save_processed_records(processed_records, output_path)


if __name__ == "__main__":
    main()
