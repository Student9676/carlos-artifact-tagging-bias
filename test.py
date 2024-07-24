import pandas as pd

annotations_raw_2 = pd.read_excel("carlos_data/clean_data_annotated_shuffled_v3.xlsx", index_col=0)
annotations_raw_2 = annotations_raw_2.filter(["ObjectID", "Subjective", "Gender", "Jargon", "Social"])

exclude_1 = range(300, 401)
exclude_2 = range(800, 901)

# Filter the DataFrame to remove lina's annotations
annotations_clean_2 = annotations_raw_2[~annotations_raw_2.index.isin(list(exclude_1) + list(exclude_2))]

# Keep rows 1-1000, excluding whats mentioned above
annotations_clean_2 = annotations_clean_2.loc[1:1000]

raw = pd.read_excel("carlos_data/clean_data_v2.xlsx")
raw = raw.filter(["ObjectID", "Title", "TextEntry"])

# keep only objects in raw that are present in annotated shuffled data using objectid
filtered_raw = raw[raw['ObjectID'].isin(annotations_clean_2['ObjectID'])]

# Reset index for both dataframes
filtered_raw.reset_index(drop=True, inplace=True)
annotations_clean_2.reset_index(drop=True, inplace=True)

# Merge both dataframes on 'ObjectID'
merged_df = pd.merge(filtered_raw, annotations_clean_2, on='ObjectID', how='inner')