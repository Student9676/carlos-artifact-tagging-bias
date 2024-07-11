import pandas as pd
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer

# Load the uploaded Excel file
file_path = 'File path for csv clean_data_annotated_v1'
data = pd.read_excel(file_path)

# Function to preprocess text
def preprocess_text(text):
    if isinstance(text, str):
        text = re.sub(r'[\n_x000D_]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    else:
        return ""

# Apply preprocessing to TextEntry
data['CleanText'] = data['TextEntry'].apply(preprocess_text)

# Apply n-gram analysis (bi-grams and tri-grams)
vectorizer = CountVectorizer(ngram_range=(2, 3))
X = vectorizer.fit_transform(data['CleanText'])

# Convert the n-gram matrix to a DataFrame
ngram_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Combine the original data with the n-gram features
data_with_ngrams = pd.concat([data, ngram_df], axis=1)

# Function to calculate sentiment score using TextBlob
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Apply sentiment analysis to the cleaned text
data_with_ngrams['Sentiment'] = data_with_ngrams['CleanText'].apply(get_sentiment)

# Function to assign bias based on sentiment score
def assign_bias(sentiment_score):
    return 1 if sentiment_score != 0 else 0

# Assign bias based on sentiment score
data_with_ngrams['DetectedBias'] = data_with_ngrams['Sentiment'].apply(assign_bias)

# Display the first few rows to show the results
print(data_with_ngrams[['CleanText', 'Sentiment', 'DetectedBias'] + ngram_df.columns.tolist()].head())

# Save the results to a new CSV file
output_path = 'Place results to your selected folder'
data_with_ngrams.to_csv(output_path, index=False)
