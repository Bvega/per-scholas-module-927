"""Apply stemming and lemmatization to the preprocessed SBA 927 text."""

from pathlib import Path

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer


EXPECTED_RECORD_COUNT = 12


def ensure_wordnet_resource() -> None:
    """Download the NLTK WordNet data only when it is unavailable."""
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        try:
            nltk.data.find("corpora/wordnet.zip")
        except LookupError:
            nltk.download("wordnet", quiet=True)


def load_processed_records(input_path: Path) -> list[list[str]]:
    """Safely parse each line as a whitespace-separated token record."""
    lines = input_path.read_text(encoding="utf-8").splitlines()
    records = [line.split() for line in lines]

    if len(records) != EXPECTED_RECORD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_RECORD_COUNT} records, but found {len(records)}."
        )

    return records


def transform_tokens(
    tokens: list[str],
    stemmer: PorterStemmer,
    lemmatizer: WordNetLemmatizer,
) -> tuple[list[str], list[str]]:
    """Return stemmed and lemmatized versions of one token record."""
    # Stemming applies rules that shorten words to a common base. The resulting
    # stem is useful for grouping related forms, but it may not be a real word.
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    # Lemmatization uses WordNet vocabulary to return a valid dictionary base
    # form, called a lemma, while preserving more linguistic meaning.
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # In practice, stemming is more aggressive and mechanical, whereas
    # lemmatization is more conservative and produces more readable results.
    return stemmed_tokens, lemmatized_tokens


def print_results_preview(
    processed_records: list[list[str]],
    stemmed_records: list[list[str]],
    lemmatized_records: list[list[str]],
) -> None:
    """Print the three token forms for the first three records only."""
    for index in range(min(3, len(processed_records))):
        print(f"Record {index + 1} original processed tokens: {processed_records[index]}")
        print(f"Record {index + 1} stemmed tokens: {stemmed_records[index]}")
        print(f"Record {index + 1} lemmatized tokens: {lemmatized_records[index]}")
        print()


def save_transformed_records(
    output_path: Path,
    processed_records: list[list[str]],
    stemmed_records: list[list[str]],
    lemmatized_records: list[list[str]],
) -> None:
    """Save processed, stemmed, and lemmatized tokens for every record."""
    output_sections = []

    for index, (processed, stemmed, lemmatized) in enumerate(
        zip(processed_records, stemmed_records, lemmatized_records), start=1
    ):
        output_sections.append(
            "\n".join(
                [
                    f"Record {index}",
                    f"Processed: {' '.join(processed)}",
                    f"Stemmed: {' '.join(stemmed)}",
                    f"Lemmatized: {' '.join(lemmatized)}",
                ]
            )
        )

    output_path.write_text("\n\n".join(output_sections) + "\n", encoding="utf-8")


def main() -> None:
    """Load all records, transform their tokens, preview, and save results."""
    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "outputs" / "preprocessed_text.txt"
    output_path = project_root / "outputs" / "stemming_lemmatization.txt"

    ensure_wordnet_resource()
    processed_records = load_processed_records(input_path)

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    transformed_records = [
        transform_tokens(tokens, stemmer, lemmatizer)
        for tokens in processed_records
    ]
    stemmed_records = [result[0] for result in transformed_records]
    lemmatized_records = [result[1] for result in transformed_records]

    print_results_preview(
        processed_records, stemmed_records, lemmatized_records
    )
    save_transformed_records(
        output_path, processed_records, stemmed_records, lemmatized_records
    )


if __name__ == "__main__":
    main()
