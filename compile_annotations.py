import pandas as pd

print("Loading Data...")
v2 = pd.read_excel("carlos_data/clean_data_annotated_v2.xlsx")
v3 = pd.read_excel("carlos_data/clean_data_annotated_shuffled_v3.xlsx")
clean_data = pd.read_excel("carlos_data/clean_data_v2.xlsx")

print("Processing...")

# Keep rows 0-600, 900-1000, 1500-1600 from v2 and 0-1000 from v3
all_annotations = v2.iloc[0:601]
all_annotations = pd.concat([all_annotations, v2.iloc[900:1001]], ignore_index=False)
all_annotations = pd.concat([all_annotations, v2.iloc[1500:1601]], ignore_index=False)
all_annotations = pd.concat([all_annotations, v3.iloc[0:1001]], ignore_index=False)
all_annotations.reset_index(drop = True)

# Keep rows that are not present in the df of annotations
not_annotated = clean_data[~clean_data["ObjectID"].isin(all_annotations["ObjectID"])]

# Concatenate annotated data and the unannotated data
df_for_annotations = pd.concat([all_annotations, not_annotated], ignore_index=True)

# Remove old index columns and hexadecimal codes from windows machines (idk how these appeared)
df_for_annotations = df_for_annotations.drop(columns=["Unnamed: 0"])
df_for_annotations.replace(r"_x[0-9A-Fa-f]{4}_", "", regex=True, inplace=True)

print("Saving Data...")

# Sync index column with excel indices
df_for_annotations.index = range(2, 2 + len(df_for_annotations))

# Columns to change values to 0
columns_to_zero = ["Subjective", "Gender", "Jargon", "Social"]

# Columns to change values to an empty string
columns_to_empty_string = ["Subjective Label", "Gender Label", "Jargon Label", "Social Label"]

# Add default values for rows after index 1805
df_for_annotations.loc[df_for_annotations.index > 1805, columns_to_zero] = 0
df_for_annotations.loc[df_for_annotations.index > 1805, columns_to_empty_string] = '""'

# Add a column called annotated? and set default values
df_for_annotations.insert(df_for_annotations.columns.get_loc('Subjective'), 'ANNOTATED?', "", allow_duplicates=False)
df_for_annotations.loc[df_for_annotations.index <= 1805, 'ANNOTATED?'] = 1
df_for_annotations.loc[df_for_annotations.index > 1805, 'ANNOTATED?'] = 0

df_for_annotations.to_excel("carlos_data/annotated_data.xlsx", engine="xlsxwriter")