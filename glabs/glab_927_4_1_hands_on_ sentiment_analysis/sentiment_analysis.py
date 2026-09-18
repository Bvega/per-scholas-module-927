# ==========================================
# GLAB 927.4.1 - Hands-On Sentiment Analysis With Python
# ==========================================

# Task 1: Importing Libraries
# Ensure TextBlob is installed by running: pip install textblob
from textblob import TextBlob

# Sample text for checking TextBlob installation
sample_text_1 = "TextBlob is successfully installed and ready to use!"

# Print confirmation message
print("--- Task 1: Installation & Import ---")
print(f"TextBlob library successfully imported. Sample text: {sample_text_1}\n")


# ==========================================
# Task 2: Implementing Sentiment Analysis
# ==========================================
print("--- Task 2: Single Text Sentiment Analysis ---")
# Sample text for sentiment analysis
sample_text_2 = "I absolutely love this product! The quality is excellent and it arrived on time."

# Create a TextBlob object
blob = TextBlob(sample_text_2)

# Perform sentiment analysis
sentiment = blob.sentiment

# Print the original text and sentiment analysis results
print("Original Text:", sample_text_2)
print("Sentiment Analysis Result:")
print("Polarity:", sentiment.polarity)        # Range from -1 (negative) to 1 (positive)
print("Subjectivity:", sentiment.subjectivity)  # Range from 0 (objective) to 1 (subjective)
print()


# ==========================================
# Task 3: Analyzing Business Communication Data
# ==========================================
print("--- Task 3: Analyzing Multiple Feedback Comments ---")

# Sample customer feedback comments
feedback_comments = [
    "The service was fantastic and the staff was very helpful.",
    "I am unhappy with the product quality and delivery was delayed.",
    "The product is okay, but it could be improved.",
    "Amazing experience! I am very satisfied with my purchase."
]

# Function to analyze sentiment of each comment
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Analyze and print sentiment for each feedback comment
for comment in feedback_comments:
    sentiment_score = analyze_sentiment(comment)
    print(f"Feedback: {comment}")
    print(f"Sentiment Polarity: {sentiment_score}")
    print("-----")