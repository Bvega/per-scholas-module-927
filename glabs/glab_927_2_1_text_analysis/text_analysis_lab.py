import nltk

# Downloading necessary NLTK data for NER and POS tagging
nltk.download('maxent_ne_chunker')
nltk.download('maxent_ne_chunker_tab')  # Added missing package
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

# Sample business document
business_document = """
The recent feedback from Acme Corp highlighted issues with the new model of the Omega widget.
Customers from New York and San Francisco have reported delays in shipping.
The CEO of Acme Corp, Jane Doe, mentioned plans to address these concerns by Q3.
"""

# Tokenizing the document
tokens = nltk.word_tokenize(business_document)

# Task 1 & 2: Applying NER and Printing Named Entities with Categories
ner_result = nltk.ne_chunk(nltk.pos_tag(tokens))

print("--- Task 1 & 2: Named Entities and Categories ---")
for entity in ner_result:
    if isinstance(entity, nltk.Tree):
        entity_name = " ".join([word for word, tag in entity.leaves()])
        entity_category = entity.label()
        print(f"{entity_name}: {entity_category}")

# Task 3: Applying POS Tagging and Printing Words with Tags
pos_tags = nltk.pos_tag(tokens)

print("\n--- Task 3: Words and POS Tags ---")
for word, tag in pos_tags:
    print(f"{word}: {tag}")
