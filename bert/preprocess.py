# Input: clean data >=v2, annotated data >=v2
# Output: processed data for bert training called preprocessed_data.xlsx

import pandas as pd

def get_processed_data(with_labels):
	# Get annotations only
	annotations_raw = pd.read_excel("carlos_data/clean_data_annotated_v2_July_18.xlsx")
	annotations_raw = annotations_raw.filter(["Subjective", "Gender", "Jargon", "Social"])

	# Keep rows 0-600, 900-1000, 1500-1600
	annotations_clean = annotations_raw.iloc[0:601]
	annotations_clean = pd.concat([annotations_clean, annotations_raw.iloc[900:1001]])
	annotations_clean = pd.concat([annotations_clean, annotations_raw.iloc[1500:1601]])
	# filtered = filtered._append(raw.iloc[900:1001])
	# filtered = filtered._append(raw.iloc[1500:1601])
	
	# Get clean data w/ artifact info
	raw = pd.read_excel("carlos_data/clean_data_v2.xlsx")
	raw = raw.filter(["ObjectID", "Title", "TextEntry"])

	# Keep rows 0-600, 900-1000, 1500-1600
	clean = raw.iloc[0:601]
	clean = pd.concat([clean, raw.iloc[900:1001]])
	clean = pd.concat([clean, raw.iloc[1500:1601]])
	# filtered = filtered._append(raw.iloc[900:1001])
	# filtered = filtered._append(raw.iloc[1500:1601])

	# Join titles and labels with annotations
	annotated_data = clean.join(annotations_clean)

	# Remove rows with empty descriptions
	# annotated_data = annotated_data.dropna(subset=["TextEntry"])
	
	# Replace all empty descriptions and titles with empty strings for internal processing (i.e. the step below)
	annotated_data["TextEntry"] = annotated_data["TextEntry"].fillna("")
	annotated_data["Title"] = annotated_data["Title"].fillna("")

	# Combine Title and TextEntry columns
	annotated_data["TextEntry"] = annotated_data["Title"] + "\n\n" + annotated_data["TextEntry"]
	annotated_data = annotated_data.drop(columns=["Title"])

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
	return annotated_data


print("RUNNING clean_data.py")
with open("clean_data.py") as cleaner:
	exec(cleaner.read())
print("----------\nFINISHED RUNNING clean_data.py\n")

get_processed_data(with_labels=False).to_excel("carlos_data/preprocessed_data_v1.xlsx", engine="xlsxwriter", index=False)