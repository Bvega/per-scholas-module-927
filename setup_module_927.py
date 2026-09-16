import os
from pathlib import Path

# Define el directorio base del módulo
base_path = Path(r"C:\Users\boliv\Desktop\06_trainings\per_scholas\2026-cax-215\Module 927")

# Define la estructura completa de carpetas del Módulo 927
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

# Crea el directorio base si no existe
base_path.mkdir(parents=True, exist_ok=True)
print(f"Base directory ready: {base_path}")

# Crea todas las subcarpetas
for dir_path in directories:
    full_path = base_path / dir_path
    full_path.mkdir(parents=True, exist_ok=True)
    print(f"Created folder: {full_path}")

# Crea el archivo requirements.txt por defecto
requirements_path = base_path / "requirements.txt"
if not requirements_path.exists():
    requirements_content = """nltk>=3.8
spacy>=3.7
torch>=2.0
transformers>=4.0
langchain>=0.1.0
"""
    requirements_path.write_text(requirements_content, encoding="utf-8")
    print(f"Created file: {requirements_path}")

# Crea el archivo README.md inicial del módulo
readme_path = base_path / "README.md"
if not readme_path.exists():
    readme_content = """# Module 927: Natural Language Processing (NLP) & LangChain

Estructura completa del repositorio para el seguimiento de lecciones, laboratorios guiados (GLABs) y evaluaciones del Módulo 927.
"""
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"Created file: {readme_path}")

# Diccionario con las lecciones y sus títulos para automatizar la creación de notas
lessons_data = {
    "01_nlp_exploration": "Lesson 927.1 - Exploration of Natural Language Processing (NLP) in AI Applications",
    "02_tokenization_stemming_lemmatization": "Lesson 927.2 - Techniques Used for Tokenization, Stemming, and Lemmatization",
    "03_ner_and_pos_tagging": "Lesson 927.3 - An Exploration of Named Entity Recognition (NER) and Part-of-Speech (POS) Tagging",
    "04_sentiment_analysis": "Lesson 927.4 - Sentiment Analysis and Semantic Understanding",
    "05_pretrained_models_and_frameworks": "Lesson 927.5 - Utilization of Pre-Trained Language Models and Introduction to AI Frameworks",
    "06_introduction_to_langchain": "Lesson 927.6 - Introduction to LangChain",
    "07_prompts_in_langchain": "Lesson 927.7 - How Prompts Drive LangChain Functionality"
}

# Genera automáticamente el archivo notes.md para cada lección dentro del ciclo
for folder_name, lesson_title in lessons_data.items():
    note_path = base_path / "lessons" / folder_name / "notes.md"
    if not note_path.exists():
        template_content = f"""# Module 927 - {lesson_title}

### 🎯 Objetivos de Aprendizaje
* Comprender los conceptos fundamentales cubiertos en esta lección.
* Aplicar los conocimientos teóricos en los laboratorios prácticos asociados.

### 📚 Resumen Teórico y Conceptos Clave
* **Concepto Principal:** [Espacio para apuntes teóricos extraídos de Canvas]

### 💻 Laboratorios y Prácticas Asociadas
* Registro de avances y códigos desarrollados.

### 🛠️ Comandos de Respaldo Git
```bash
git add .
git commit -m "Actualización: {lesson_title}"
git push
    """
    note_path.write_text(template_content, encoding="utf-8")
    print(f"Created notes template: {note_path}")

print("\n¡Estructura completa y automatización del Módulo 927 finalizada con éxito!")