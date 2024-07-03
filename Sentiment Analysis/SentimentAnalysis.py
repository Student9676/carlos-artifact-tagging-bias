import pandas as pd
from textblob import TextBlob

# Read the Excel file
file_path = './carlos_data/objs_w_title_n_desc.xlsx'
df = pd.read_excel(file_path)

# Extract the target text column
target_texts = df['TextEntry'].astype(str).fillna('')

# Function to get sentiment and subjectivity
def get_sentiment_subjectivity(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

# Apply the function to the target texts
df[['Sentiment_TextBlob', 'Subjectivity_TextBlob']] = target_texts.apply(lambda text: pd.Series(get_sentiment_subjectivity(text)))

# Display the first few rows to confirm
print(df.head())

# Save the results to a new Excel file
output_file_path = './carlos_data/objs_w_sentiment_analysis.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Sentiment analysis results saved to {output_file_path}")
