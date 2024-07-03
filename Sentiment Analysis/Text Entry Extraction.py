import pandas as pd
from textblob import TextBlob

# Load the Excel file
file_path = './carlos_data/objs_w_sentiment_analysis.xlsx'
df = pd.read_excel(file_path)

# Extract the target text column
target_texts = df['TextEntry'].astype(str).fillna('')

# Function to get sentiment and subjectivity
def get_sentiment_subjectivity(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

# Apply the function to the target texts
df[['Sentiment_TextBlob', 'Subjectivity_TextBlob']] = target_texts.apply(lambda text: pd.Series(get_sentiment_subjectivity(text)))

# Define criteria for worth analysis
# For example, let's consider texts with absolute sentiment polarity greater than 0.5 or subjectivity greater than 0.5
sentiment_threshold = 0.5
subjectivity_threshold = 0.5

# Filter texts worth analysis
worth_analysis = df[(df['Sentiment_TextBlob'].abs() > sentiment_threshold) | (df['Subjectivity_TextBlob'] > subjectivity_threshold)]

# Display the first few rows to confirm
print(worth_analysis.head())

# Save the filtered results to a new Excel file
output_file_path = './carlos_data/extracted_objs_w_sentiment_analysis.xlsx'
worth_analysis.to_excel(output_file_path, index=False)

print(f"Worth analysis text entries saved to {output_file_path}")
