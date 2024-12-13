

# Input: annotated data
# Output: processed data for bert training called preprocessed_data.xlsx

import pandas as pd
import regex as re
import sys
import pysbd


num_annotated = ""

# Get annotated data
annotated_data = pd.read_csv("carlos_data/annotated_data.csv", encoding='latin1')

if num_annotated == "":
    annotated_data = annotated_data.iloc[0:1805-2]  # -2 cuz of 2 starting index
else:
    try:
        num_annotated = int(num_annotated)
        annotated_data = annotated_data.iloc[0:num_annotated-2]
    except ValueError:
        print("ERROR: Set num_annotated to a valid number or 'default'")
        sys.exit(1)

# Replace all empty descriptions and titles with empty strings for internal processing (i.e., the step below)
annotated_data["TextEntry"] = annotated_data["TextEntry"].fillna("")
annotated_data["Title"] = annotated_data["Title"].fillna("")

# Combine Title and TextEntry columns
annotated_data["TextEntry"] = annotated_data["Title"] + "\n\n" + annotated_data["TextEntry"]
annotated_data = annotated_data.drop(columns=["Title"])

# Now we want to convert the values in the label columns to arrays of phrases/words

# Function to convert strings to list of strings and the characters '""' to NA
def string_to_array(s):
    s = str(s)
    if pd.isna(s) or s == '""' or s == '':
        return pd.NA
    return [phrase.strip() for phrase in re.split(r',\s*|\s*,|\n', s) if phrase.strip()]

# Replace empty strings with NaNs and convert strings to lists
for column in ['Subjective Label', 'Gender Label', 'Jargon Label', 'Social Label']:
    annotated_data[column] = annotated_data[column].apply(string_to_array)

# Remove carriage returns
annotated_data = annotated_data.replace("_x000D_", "", regex=True)

# Now we will alter descriptions to only keep sentences where any of the phrases is present,
# making sure that there is only one sentence per phrase
descs = annotated_data['TextEntry'].values
jargon_labels_array = annotated_data['Jargon Label'].values
subjective_labels_array = annotated_data['Subjective Label'].values
social_labels_array = annotated_data['Social Label'].values
gender_labels_array = annotated_data['Gender Label'].values

# Get segmenter for sentence splitting
seg = pysbd.Segmenter(language="en", clean=False)

# Segment each description into sentences
for i in range(len(descs)):
    descs[i] = seg.segment(descs[i])

    # Strip all sentences
    for j in range(len(descs[i])):
        descs[i][j] = descs[i][j].strip()

# Sentence-level splitting and new row generation
new_rows = []

# Main loop for processing sentences and matching labels
for sentences, subjective_labels, gender_labels, jargon_labels, social_labels, object_id, subjective_score, gender_score, jargon_score, social_score in \
        zip(descs, subjective_labels_array, gender_labels_array, jargon_labels_array, social_labels_array,
            annotated_data["ObjectID"], annotated_data["Subjective"], annotated_data["Gender"],
            annotated_data["Jargon"], annotated_data["Social"]):

    # Handle label arrays
    subjective_labels = [] if not hasattr(subjective_labels, '__len__') and pd.isna(subjective_labels) else subjective_labels
    gender_labels = [] if not hasattr(gender_labels, '__len__') and pd.isna(gender_labels) else gender_labels
    jargon_labels = [] if not hasattr(jargon_labels, '__len__') and pd.isna(jargon_labels) else jargon_labels
    social_labels = [] if not hasattr(social_labels, '__len__') and pd.isna(social_labels) else social_labels

    # Process each sentence
    for sentence in sentences:
        # Initialize lists for matching labels
        matching_subjective = [lbl for lbl in subjective_labels if lbl.lower().replace('"', '') in sentence.lower()]
        matching_gender = [lbl for lbl in gender_labels if lbl.lower().replace('"', '') in sentence.lower()]
        matching_jargon = [lbl for lbl in jargon_labels if lbl.lower().replace('"', '') in sentence.lower()]
        matching_social = [lbl for lbl in social_labels if lbl.lower().replace('"', '') in sentence.lower()]

        # Set scores to 1 if corresponding labels are present, otherwise 0
        sentence_subjective_score = 1 if matching_subjective else 0
        sentence_gender_score = 1 if matching_gender else 0
        sentence_jargon_score = 1 if matching_jargon else 0
        sentence_social_score = 1 if matching_social else 0

        # Add the sentence as a new row to `new_rows`
        new_rows.append({
            "ObjectID": object_id,
            "TextEntry": sentence,
            'ANNOTATED?': 1,
            "Subjective": sentence_subjective_score,
            "Gender": sentence_gender_score,
            "Jargon": sentence_jargon_score,
            "Social": sentence_social_score,
            "Subjective Label": matching_subjective if matching_subjective else None,
            "Gender Label": matching_gender if matching_gender else None,
            "Jargon Label": matching_jargon if matching_jargon else None,
            "Social Label": matching_social if matching_social else None,
        })

# Create a new DataFrame from the `new_rows` list
sentence_level_data = pd.DataFrame(new_rows)

# Save the sentence-level data to a new CSV
sentence_level_data.to_csv("carlos_data/sentence_level_preprocessed_data.csv", index=False, encoding="utf-8")

# Print the first few rows for verification
print(sentence_level_data.head())