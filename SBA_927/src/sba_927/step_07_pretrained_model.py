"""Apply a pretrained Hugging Face sentiment model to the SBA 927 dataset."""

from pathlib import Path
from typing import Any

from transformers import pipeline


EXPECTED_RECORD_COUNT = 12
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


def load_original_records(dataset_path: Path) -> list[str]:
    """Read the UTF-8 dataset and return its non-empty original records."""
    lines = dataset_path.read_text(encoding="utf-8").splitlines()
    records = [line for line in lines if line.strip()]

    if len(records) != EXPECTED_RECORD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_RECORD_COUNT} records, but found {len(records)}."
        )

    return records


def create_sentiment_pipeline() -> Any:
    """Load the selected pretrained model through a Transformers pipeline."""
    # A pretrained language model has already learned language patterns from a
    # large collection of text before it is used for this project.
    # The Transformers pipeline combines tokenization, model inference, and
    # readable output labels behind one convenient interface.
    return pipeline(
        task="sentiment-analysis",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
    )


def analyze_records(
    records: list[str], sentiment_pipeline: Any
) -> list[dict[str, str | float]]:
    """Run sentiment inference and capture text, labels, and confidence scores."""
    model_outputs = sentiment_pipeline(records, truncation=True)

    return [
        {
            "text": record,
            "label": str(model_output["label"]),
            "score": float(model_output["score"]),
        }
        for record, model_output in zip(records, model_outputs)
    ]


def print_results_preview(results: list[dict[str, str | float]]) -> None:
    """Print pretrained-model results for the first three records only."""
    for record_number, result in enumerate(results[:3], start=1):
        print(f"Record {record_number} original text: {result['text']}")
        print(f"Predicted sentiment label: {result['label']}")
        print(f"Confidence score: {result['score']:.4f}")
        print()


def save_model_results(
    output_path: Path, results: list[dict[str, str | float]]
) -> None:
    """Save all predictions followed by educational observations."""
    record_sections = []

    for record_number, result in enumerate(results, start=1):
        record_sections.append(
            "\n".join(
                [
                    f"Record {record_number}",
                    f"Original text: {result['text']}",
                    f"Predicted sentiment label: {result['label']}",
                    f"Confidence score: {result['score']:.4f}",
                ]
            )
        )

    observations = "\n".join(
        [
            "Educational Observations",
            "- This sentiment model is pretrained.",
            "- It uses learned language patterns rather than VADER's lexicon and rules.",
            "- Confidence scores indicate how strongly the model favors each prediction.",
            "- Pretrained models can still make mistakes or interpret context differently from VADER.",
            "- Model predictions should be evaluated rather than assumed to be correct.",
        ]
    )

    output_text = "\n\n".join(record_sections + [observations]) + "\n"
    output_path.write_text(output_text, encoding="utf-8")


def main() -> None:
    """Load the data, run the pretrained model, preview, and save results."""
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "SBA927.txt"
    output_path = project_root / "outputs" / "pretrained_model_results.txt"

    records = load_original_records(dataset_path)
    sentiment_pipeline = create_sentiment_pipeline()
    results = analyze_records(records, sentiment_pipeline)

    # Comparing this learned model with the earlier VADER baseline demonstrates
    # how model-based predictions may differ from lexicon- and rule-based scores.
    print_results_preview(results)
    save_model_results(output_path, results)


if __name__ == "__main__":
    main()
