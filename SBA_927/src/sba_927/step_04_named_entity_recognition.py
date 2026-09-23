"""Perform named entity recognition on the original SBA 927 dataset."""

from pathlib import Path

import nltk
from nltk import ne_chunk, pos_tag, sent_tokenize, word_tokenize
from nltk.tree import Tree


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
        "maxent_ne_chunker": "chunkers/maxent_ne_chunker",
        "maxent_ne_chunker_tab": "chunkers/maxent_ne_chunker_tab",
        "words": "corpora/words",
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
    """Read the UTF-8 dataset and return all non-empty original records."""
    lines = dataset_path.read_text(encoding="utf-8").splitlines()
    records = [line for line in lines if line.strip()]

    if len(records) != EXPECTED_RECORD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_RECORD_COUNT} records, but found {len(records)}."
        )

    return records


def extract_named_entities(text: str) -> list[tuple[str, str]]:
    """Extract entity text and labels from one original text record."""
    entities: list[tuple[str, str]] = []

    # Named Entity Recognition (NER) identifies and classifies meaningful names
    # in text. Possible NLTK categories include PERSON, ORGANIZATION, GPE
    # (geopolitical entity), LOCATION, FACILITY, and GSP.
    for sentence in sent_tokenize(text):
        tokens = word_tokenize(sentence)

        # NLTK's NER chunker uses part-of-speech tags as grammatical evidence for
        # deciding which neighboring words form entities. These tags are used
        # only as an intermediate NER step, not as the separate SBA POS exercise.
        tagged_tokens = pos_tag(tokens)
        entity_tree = ne_chunk(tagged_tokens)

        for node in entity_tree:
            if isinstance(node, Tree):
                entity_text = " ".join(word for word, _ in node.leaves())
                entities.append((entity_text, node.label()))

    return entities


def print_ner_preview(
    records: list[str], entity_results: list[list[tuple[str, str]]]
) -> None:
    """Print named entities for the first three records only."""
    for record_number, (record, entities) in enumerate(
        zip(records[:3], entity_results[:3]), start=1
    ):
        print(f"Record {record_number}: {record}")
        if entities:
            for entity_text, entity_label in entities:
                print(f"  Entity: {entity_text} | Category: {entity_label}")
        else:
            print("  No named entities found.")
        print()


def save_named_entities(
    output_path: Path, entity_results: list[list[tuple[str, str]]]
) -> None:
    """Save named entity results for every dataset record."""
    output_sections = []

    for record_number, entities in enumerate(entity_results, start=1):
        lines = [f"Record {record_number}"]
        if entities:
            lines.extend(
                f"Entity: {entity_text} | Category: {entity_label}"
                for entity_text, entity_label in entities
            )
        else:
            lines.append("No named entities found.")
        output_sections.append("\n".join(lines))

    output_path.write_text("\n\n".join(output_sections) + "\n", encoding="utf-8")


def main() -> None:
    """Load original text, recognize entities, preview, and save results."""
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "SBA927.txt"
    output_path = project_root / "outputs" / "named_entities.txt"

    ensure_nltk_resources()
    records = load_original_records(dataset_path)

    # Original capitalization and complete sentence context help NER distinguish
    # proper names from ordinary words and interpret each name in its surroundings.
    entity_results = [extract_named_entities(record) for record in records]

    print_ner_preview(records, entity_results)
    save_named_entities(output_path, entity_results)


if __name__ == "__main__":
    main()
