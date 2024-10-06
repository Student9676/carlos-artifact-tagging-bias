# Input: annotated data
# Output: processed data for bert training called preprocessed_data.xlsx

import pandas as pd
import regex as re

# Get annotated data
annotated_data = pd.read_excel("carlos_data/annotated_data.xlsx")

# Replace all empty descriptions and titles with empty strings for internal processing (i.e. the step below)
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

# Replace empty strings with NaNs and convert strings, to list
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

# POSSIBLE OPTMIZATION by removing ids like "X.0427.004 B" and "1969.127.029" from the resulting lists
# Get segmenter
import pysbd
seg = pysbd.Segmenter(language="en", clean=False)

# segment each description into sentences
for i in range(len(descs)):
	descs[i] = seg.segment(descs[i])
	
	# strip all sentences
	for j in range(len(descs[i])):
		descs[i][j] = descs[i][j].strip()

new_descs = []

# Main loop
for sentences, subjective_labels, gender_labels, jargon_labels, social_labels in \
zip(descs, subjective_labels_array, gender_labels_array, jargon_labels_array, social_labels_array):
	new_desc = ""

	subjective_labels = [] if not hasattr(subjective_labels, '__len__') and pd.isna(subjective_labels) else subjective_labels
	gender_labels = [] if not hasattr(gender_labels, '__len__') and pd.isna(gender_labels) else gender_labels
	jargon_labels = [] if not hasattr(jargon_labels, '__len__') and pd.isna(jargon_labels) else jargon_labels
	social_labels = [] if not hasattr(social_labels, '__len__') and pd.isna(social_labels) else social_labels
	phrases = [*subjective_labels, *gender_labels, *jargon_labels, *social_labels]
	
	if len(phrases) == 0:
		for sentence in sentences:
			new_desc += sentence + " "
		new_descs.append(new_desc)
		continue
	
	for sentence in sentences:
		for phrase in phrases:
			if phrase.lower().replace('"', '') in sentence.lower().replace('"', ''):
				new_desc += sentence + " "
				# OPTIMIZATION if phrase size == sentence size then include n words surrounding it
				phrases.remove(phrase)
	
	if len(phrases) != 0:
		for phrase in phrases:
			new_desc += phrase + ". "

	new_descs.append(new_desc.strip())

annotated_data["TextEntry"] = new_descs

# Strip descriptions for clean data
for index, row in annotated_data.iterrows():
	annotated_data.at[index, "TextEntry"] = row["TextEntry"].strip()

# Fill na's in classification columns with zeros just incase an annotater left a cell empty
annotated_data["Subjective"] = annotated_data["Subjective"].fillna(0)
annotated_data["Gender"] = annotated_data["Gender"].fillna(0)
annotated_data["Jargon"] = annotated_data["Jargon"].fillna(0)
annotated_data["Social"] = annotated_data["Social"].fillna(0)

# Remove carriage returns
annotated_data = annotated_data.replace("_x000D_", "", regex=True)

print(annotated_data.head(20))
print(annotated_data.shape)
annotated_data.to_excel("carlos_data/preprocessed_data.xlsx", engine="xlsxwriter", index=False)