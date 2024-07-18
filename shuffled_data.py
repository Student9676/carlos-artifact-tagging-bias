# Returns shuffled version of our cleaned dataset without recorded, annotated 
# rows as of July 18, 2024. Since there are more annotated rows, that are not recorded,
# they are placed at the top and the rest of the shuffled rows are below.
# 
# Input: V2 Annotated Data as of July 18
# Output: Shuffled data with remaining annotated rows on top. V3 Annotations.

import pandas as pd

# Read the Excel file
annotated_data_raw = pd.read_excel("carlos_data/clean_data_annotated_v2_July_18.xlsx")\

# Drop rows 0-600, 900-1000, 1500-1600
drop_indices = list(range(0, 601)) + list(range(900, 1001)) + list(range(1500, 1601))
non_annotated_data = annotated_data_raw.drop(drop_indices)

# Randomly shuffle the order of all rows without changing the index
shuffled_data = non_annotated_data.sample(frac=1, random_state=1)

annotated_data = pd.DataFrame()

# Get all annotated rows
for index, row in shuffled_data.iterrows():
	if row["Subjective"]==1 or row["Gender"]==1 or row["Jargon"]==1 or row["Social"]==1:
		annotated_data = pd.concat([annotated_data, pd.DataFrame([row])])
		shuffled_data.drop(index, inplace = True)

# Put annotated rows on top
final = pd.concat([annotated_data, shuffled_data])

# Reset the index
final = final.reset_index(drop=True)

# Remove carriage returns
final = final.replace('_x000D_', '', regex=True)

# Show the resulting df
print(final.head(20))
final.to_excel("carlos_data/clean_data_annotated_shuffled_v3.xlsx", engine="xlsxwriter")



