import pandas as pd
import re
from textblob import TextBlob

# Load the uploaded Excel file
file_path = 'Path to file clean_data_annotated_v1.xlsx on your computer'
data = pd.read_excel(file_path)

# Function to preprocess text
def preprocess_text(text):
    if isinstance(text, str):
        text = re.sub(r'[\n_x000D_]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    else:
        return ""

# Function to calculate sentiment score using TextBlob
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Apply preprocessing to TextEntry
data['CleanText'] = data['TextEntry'].apply(preprocess_text)

# Apply sentiment analysis to the cleaned text
data['Sentiment'] = data['CleanText'].apply(get_sentiment)

# Select only the required columns for the output file
output_data = data[['ObjectID', 'Title', 'Sentiment']]

# Display the first few rows to show the results
print(output_data.head())

# Save the results to a new CSV file
output_path = 'Path to your designated output file'
output_data.to_csv(output_path, index=False)
