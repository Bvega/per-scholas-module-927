"""Analyze SBA 927 text sentiment with NLTK VADER."""

from pathlib import Path

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


EXPECTED_RECORD_COUNT = 12


def ensure_vader_lexicon() -> None:
    """Download the NLTK VADER lexicon only when it is unavailable."""
    try:
        nltk.data.find("sentiment/vader_lexicon")
    except LookupError:
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon", quiet=True)


def load_original_records(dataset_path: Path) -> list[str]:
    """Read the UTF-8 dataset and return its non-empty original records."""
    lines = dataset_path.read_text(encoding="utf-8").splitlines()
    records = [line for line in lines if line.strip()]

    if len(records) != EXPECTED_RECORD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_RECORD_COUNT} records, but found {len(records)}."
        )

    return records


def create_sentiment_prompt(record: str) -> str:
    """Create an explicit prompt for later language-model comparison."""
    return (
        "Analyze the sentiment of the following text.\n"
        "Classify it as Positive, Negative, or Neutral.\n"
        "Briefly explain the reason for the classification.\n\n"
        f'Text: "{record}"'
    )


def classify_compound_score(compound_score: float) -> str:
    """Convert a VADER compound score into a sentiment classification."""
    # VADER's standard thresholds classify scores of at least 0.05 as Positive,
    # scores of at most -0.05 as Negative, and scores between them as Neutral.
    if compound_score >= 0.05:
        return "Positive"
    if compound_score <= -0.05:
        return "Negative"
    return "Neutral"


def analyze_record(
    record: str, analyzer: SentimentIntensityAnalyzer
) -> tuple[str, dict[str, float], str]:
    """Generate a prompt, calculate VADER scores, and classify one record."""
    prompt = create_sentiment_prompt(record)

    # Sentiment analysis estimates the emotional tone expressed by text. VADER
    # (Valence Aware Dictionary and sEntiment Reasoner) is a rule- and
    # lexicon-based sentiment tool designed to account for features such as
    # emphasis, punctuation, negation, and changes in word intensity.
    scores = analyzer.polarity_scores(record)

    # The positive, neutral, and negative scores describe the proportions of the
    # text associated with each tone. The compound score summarizes the overall
    # sentiment as a normalized value from -1 (most negative) to 1 (most positive).
    classification = classify_compound_score(scores["compound"])
    return prompt, scores, classification


def print_sentiment_preview(
    records: list[str],
    results: list[tuple[str, dict[str, float], str]],
) -> None:
    """Print detailed VADER results for the first three records only."""
    for record_number, (record, result) in enumerate(
        zip(records[:3], results[:3]), start=1
    ):
        prompt, scores, classification = result
        print(f"Record {record_number} original text: {record}")
        print("Generated prompt:")
        print(prompt)
        print(f"Positive score: {scores['pos']}")
        print(f"Neutral score: {scores['neu']}")
        print(f"Negative score: {scores['neg']}")
        print(f"Compound score: {scores['compound']}")
        print(f"Final sentiment classification: {classification}")
        print()


def save_sentiment_results(
    output_path: Path,
    records: list[str],
    results: list[tuple[str, dict[str, float], str]],
) -> None:
    """Save prompts and VADER results for every dataset record."""
    output_sections = []

    for record_number, (record, result) in enumerate(
        zip(records, results), start=1
    ):
        prompt, scores, classification = result
        output_sections.append(
            "\n".join(
                [
                    f"Record {record_number}",
                    f"Original text: {record}",
                    "Generated prompt:",
                    prompt,
                    f"Positive score: {scores['pos']}",
                    f"Neutral score: {scores['neu']}",
                    f"Negative score: {scores['neg']}",
                    f"Compound score: {scores['compound']}",
                    f"Final sentiment classification: {classification}",
                ]
            )
        )

    output_path.write_text("\n\n".join(output_sections) + "\n", encoding="utf-8")


def main() -> None:
    """Load, analyze, preview, and save sentiment results for all records."""
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "SBA927.txt"
    output_path = project_root / "outputs" / "sentiment_analysis.txt"

    ensure_vader_lexicon()
    records = load_original_records(dataset_path)
    analyzer = SentimentIntensityAnalyzer()
    results = [analyze_record(record, analyzer) for record in records]

    # These prompts and VADER classifications will be compared with a pretrained
    # language model in the next SBA step; no language model is used here.
    print_sentiment_preview(records, results)
    save_sentiment_results(output_path, records, results)


if __name__ == "__main__":
    main()
