
# GLAB 927.1.2
# Hands-On Text Processing for Email Management with Python

import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


# -------------------------------------------------
# Task 1: Importing Libraries
# -------------------------------------------------

# Checking NLTK version
nltk_version = nltk.__version__

# Print confirmation message and NLTK version
print(f"NLTK library successfully imported. NLTK version: {nltk_version}")


# -------------------------------------------------
# Task 2: Implementing Stemming
# -------------------------------------------------

# Download NLTK resources (tokenizers)
nltk.download("punkt")
nltk.download("punkt_tab")

# Sample email content for stemming
email_content = (
    "Our team will be working on the upcoming project deadlines. "
    "Please ensure that all deliverables are submitted before the end of the week."
)

# Create a Porter Stemmer instance
porter_stemmer = PorterStemmer()

# Apply stemming to each word in the email content
stemmed_words = [
    porter_stemmer.stem(word)
    for word in nltk.word_tokenize(email_content)
]

# Print the original and stemmed text
print("Original Email Content:", email_content)
print("Stemmed Email Content:", " ".join(stemmed_words))


# -------------------------------------------------
# Task 3: Applying Lemmatization
# -------------------------------------------------

# Sample email content for lemmatization
email_content_lemma = (
    "The team members are working on their tasks diligently. "
    "Please ensure that every report is submitted promptly."
)

# Download WordNet resource
nltk.download("wordnet")

# Create a WordNet Lemmatizer instance
lemmatizer = WordNetLemmatizer()

# Apply lemmatization to each word in the email content
lemmatized_words = [
    lemmatizer.lemmatize(word)
    for word in nltk.word_tokenize(email_content_lemma)
]

# Print the original and lemmatized text
print("Original Email Content:", email_content_lemma)
print("Lemmatized Email Content:", " ".join(lemmatized_words))