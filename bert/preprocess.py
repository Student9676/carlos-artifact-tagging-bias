# Input: annotated data
# Output: processed data for bert training called preprocessed_data.xlsx

import pandas as pd
import regex as re
import sys

num_annotated = "default"

# Get annotated data
annotated_data = pd.read_csv("carlos_data/annotated_data.csv", encoding='latin1')

if num_annotated == "default":
	annotated_data = annotated_data.iloc[0:1805-2] # -2 cuz of 2 starting index
else:
	try:
		num_annotated = int(num_annotated)
		annotated_data = annotated_data.iloc[0:num_annotated-2]
	except ValueError:
		print("ERROR: Set num_annotated to a valid number or 'default'")
		sys.exit(1)

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
	# splits sentence into array of words. Splits on commas followed by optional spaces, 
	# spaces followed by commas, and newlines 
	return [phrase.strip() for phrase in re.split(r" ,\s*  |  \s*,  |  \n ", s) if phrase.strip()]

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
new_subj_class_array = []
new_gend_class_array = []
new_jarg_class_array = []
new_soci_class_array = []
new_subj_labels_array = []
new_gend_labels_array = []
new_jarg_labels_array = []
new_soci_labels_array = []
idx = -1 # so that our indexing starts at 0
biases_found = []

# Main loop
for sentences, subjective_labels, gender_labels, jargon_labels, social_labels in \
zip(descs, subjective_labels_array, gender_labels_array, jargon_labels_array, social_labels_array):
	new_desc = ""

	# if the labels arr is not iterable and is na, it is replaced with an empty list
	subjective_labels = [] if not hasattr(subjective_labels, '__len__') and pd.isna(subjective_labels) else subjective_labels
	gender_labels = [] if not hasattr(gender_labels, '__len__') and pd.isna(gender_labels) else gender_labels
	jargon_labels = [] if not hasattr(jargon_labels, '__len__') and pd.isna(jargon_labels) else jargon_labels
	social_labels = [] if not hasattr(social_labels, '__len__') and pd.isna(social_labels) else social_labels

	# if there are any labels make the var equal an array of phrases
	subjective_labels = subjective_labels[0].split(", ") if len(subjective_labels) > 0 else subjective_labels
	gender_labels = gender_labels[0].split(", ") if len(gender_labels) > 0 else gender_labels
	jargon_labels = jargon_labels[0].split(", ") if len(jargon_labels) > 0 else jargon_labels
	social_labels = social_labels[0].split(", ") if len(social_labels) > 0 else social_labels

	# remove double quotes symbol
	subjective_labels = [label.replace('"', '') for label in subjective_labels]
	gender_labels = [label.replace('"', '') for label in gender_labels]
	jargon_labels = [label.replace('"', '') for label in jargon_labels]
	social_labels = [label.replace('"', '') for label in social_labels]

	# if there is no bias, i.e. no bias labels, then keep the description as is and mark as no bias
	phrases = [*subjective_labels, *gender_labels, *jargon_labels, *social_labels]
	if len(phrases) == 0:
		new_descs += sentences

		new_subj_class_array += [0] * len(sentences)
		new_gend_class_array += [0] * len(sentences)
		new_jarg_class_array += [0] * len(sentences)
		new_soci_class_array += [0] * len(sentences)
		new_subj_labels_array += [[]] * len(sentences)
		new_gend_labels_array += [[]] * len(sentences)
		new_jarg_labels_array += [[]] * len(sentences)
		new_soci_labels_array += [[]] * len(sentences)

		idx += len(sentences)
		continue

	# main loop
	for sentence in sentences:
		# init arrays and clean sentence/phrase
		sentence.replace('"', '')
		sentence = sentence.strip()
		idx += 1 # can use .tail() to avoid saving idx var
		new_descs.append(sentence)
		new_subj_class_array.append(0)
		new_gend_class_array.append(0)
		new_jarg_class_array.append(0)
		new_soci_class_array.append(0)
		new_subj_labels_array.append([])
		new_gend_labels_array.append([])
		new_jarg_labels_array.append([])
		new_soci_labels_array.append([])

		# check for bias label presence
		for label in subjective_labels:
			if label.lower().strip() in sentence.lower():
				biases_found.append(label) # record for logs
				new_subj_class_array[idx] = 1 # mark as found (binary classification)
				new_subj_labels_array[idx].append(label.strip()) # save label in new array
		
		for label in gender_labels:
			if label.lower().strip() in sentence.lower():
				biases_found.append(label)
				new_gend_class_array[idx] = 1
				new_gend_labels_array[idx].append(label.strip())
		
		for label in jargon_labels:
			if label.lower().strip() in sentence.lower():
				biases_found.append(label)
				new_jarg_class_array[idx] = 1
				new_jarg_labels_array[idx].append(label.strip())

		for label in social_labels:
			if label.lower().strip() in sentence.lower():
				biases_found.append(label)
				new_soci_class_array[idx] = 1
				new_soci_labels_array[idx].append(label.strip())

"""check if any biased labels were not found in the description"""
# # save logs
# leftover = []
# for phrase in phrases:
# 	if phrase in biases_found:
# 		biases_found.remove(phrase)
# 	else:
# 		leftover.append(phrase)
# with open("bert/logs.txt", "w") as file:
# 	file.write("missed labels\n")
# 	file.write("\n")
# 	for index, element in enumerate(leftover):
# 		file.write(f"{index}: {element}\n")

preprocessed_data = pd.DataFrame({
	"TextEntry": new_descs,
	"Subjective": new_subj_class_array,
	"Gender": new_gend_class_array,
	"Jargon": new_jarg_class_array,
	"Social": new_soci_class_array,
	"Subjective Label": new_subj_labels_array,
	"Gender Label": new_gend_labels_array,
	"Jargon Label": new_jarg_labels_array,
	"Social Label": new_soci_labels_array,
})

# Strip descriptions for clean data
for index, row in preprocessed_data.iterrows():
	preprocessed_data.at[index, "TextEntry"] = row["TextEntry"].strip()

# Fill na's in classification columns with zeros just incase an annotater left a cell empty
preprocessed_data["Subjective"] = preprocessed_data["Subjective"].fillna(0)
preprocessed_data["Gender"] = preprocessed_data["Gender"].fillna(0)
preprocessed_data["Jargon"] = preprocessed_data["Jargon"].fillna(0)
preprocessed_data["Social"] = preprocessed_data["Social"].fillna(0)

# remove any empty description rows from data
preprocessed_data = preprocessed_data.dropna(subset=["TextEntry"])

# Remove carriage returns & quotes
preprocessed_data = preprocessed_data.replace("_x000D_", "", regex=True)
preprocessed_data = preprocessed_data.replace("'", "", regex=True)
preprocessed_data = preprocessed_data.replace('"', "", regex=True)

# Sync index column with excel indices
preprocessed_data.index = range(2, 2 + len(preprocessed_data))

if "Unnamed: 0" in preprocessed_data.columns:
	preprocessed_data = preprocessed_data.drop(columns=["Unnamed: 0"])

print(preprocessed_data)
preprocessed_data.to_csv("carlos_data/sentences_preprocessed_data.csv", index=False, encoding="utf-8")