import os
from pathlib import Path

# Define the base path provided
base_path = Path(r"C:\Users\boliv\Desktop\06_trainings\per_scholas\2026-cax-215\Module 927")

# Define the folder structure to create
directories = [
    "lessons/01_nlp_exploration",
    "lessons/02_tokenization_stemming_lemmatization",
    "lessons/03_ner_and_pos_tagging",
    "lessons/04_sentiment_analysis",
    "lessons/05_pretrained_models_and_frameworks",
    "lessons/06_introduction_to_langchain",
    "lessons/07_prompts_in_langchain",
    "glabs/glab_927_1_1_installing_python",
    "glabs/glab_927_1_2_email_management_nlp",
    "glabs/glab_927_2_1_text_analysis",
    "glabs/glab_927_6_1_mastering_langchain",
    "assessments/sba_927_business_text_analytics",
    "assessments/kba_927_natural_language_processing",
]

# Create base directory if it doesn't exist
base_path.mkdir(parents=True, exist_ok=True)
print(f"Base directory ready: {base_path}")

# Create all subdirectories
for dir_path in directories:
    full_path = base_path / dir_path
    full_path.mkdir(parents=True, exist_ok=True)
    print(f"Created: {full_path}")

# Create a template requirements.txt
requirements_path = base_path / "requirements.txt"
if not requirements_path.exists():
    requirements_content = """nltk>=3.8
spacy>=3.7
torch>=2.0
transformers>=4.0
langchain>=0.1.0
"""
    requirements_path.write_text(requirements_content)
    print(f"Created: {requirements_path}")

# Create a starter README.md template
readme_path = base_path / "README.md"
if not readme_path.exists():
    readme_content = """# Module 927: Natural Language Processing (NLP) & LangChain

Repository structure for tracking lessons, guided labs (GLABs), and assessments for Module 927.

## Course Resources & Lessons
- [Lesson 927.1 - Exploration of Natural Language Processing (NLP) in AI Applications](https://perscholas.instructure.com/courses/3601/pages/lesson-927-dot-1-exploration-of-natural-language-processing-nlp-in-ai-applications)
- [GLAB 927.1.1 - Installing Python](https://perscholas.instructure.com/courses/3601/pages/glab-927-dot-1-dot-1-installing-python)
- [GLAB 927.1.2 - Hands-on Text Processing for Email Management with Python](https://perscholas.instructure.com/courses/3601/pages/glab-927-dot-1-dot-2-hands-on-text-processing-for-email-management-with-python)
- [ELINK 927.2.1 - NLTK Lemmatizer](https://perscholas.instructure.com/courses/3601/pages/elink-927-dot-2-dot-1-nltk-lemmatizer)
- [ELINK 927.3.2 - spaCy Documentation](https://perscholas.instructure.com/courses/3601/pages/elink-927-dot-3-dot-2-spacy-documentation)
- [ELINK 927.5.2 - Huggingface Transformers](https://perscholas.instructure.com/courses/3601/pages/elink-927-dot-5-dot-2-huggingface-transformers)
- [ELINK 927.5.3 - LangChain Documentation](https://perscholas.instructure.com/courses/3601/pages/elink-927-dot-5-dot-3-langchain-documentation)
- [SBA 927 - Business Text Analytics: Natural Language Processing Techniques](https://perscholas.instructure.com/courses/3601/pages/sba-927-business-text-analytics-natural-language-processing-techniques)
"""
    readme_path.write_text(readme_content)
    print(f"Created: {readme_path}")

print("\nModule 927 environment successfully structured!")