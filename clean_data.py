import pandas as pd

# Read from excel files
objects = pd.read_csv("./carlos_data/ObjectTables/Objects.csv")
descriptions = pd.read_csv("./carlos_data/ObjectTables/TextEntries.csv")
titles = pd.read_csv("./carlos_data/ObjectTables/ObjTitles.csv")

# Remove unwanted rows 
descriptions = descriptions.filter(["ID", "TextEntry", "EnteredDate"])
objects = objects.filter(["ObjectID", "Medium"])
titles = titles.filter(["ObjectID", "Title"])

# Merge dfs
obj_w_desc = objects.join(descriptions.set_index("ID"), on="ObjectID")
obj_w_desc = obj_w_desc.join(titles.set_index("ObjectID"), on="ObjectID")

# Replace NA's and empty time slots in Time col with placeholder
obj_w_desc["EnteredDate"] = obj_w_desc["EnteredDate"].fillna("2050-01-01 00:00:00.000")
obj_w_desc["EnteredDate"] = obj_w_desc["EnteredDate"].replace("", "2050-01-01 00:00:00.000")

# Convert times to datetime
obj_w_desc["EnteredDate"] = pd.to_datetime(obj_w_desc["EnteredDate"], errors='raise')

# Group by ID
grouped = obj_w_desc.groupby("ObjectID")

descriptions = []

# Get merged description
for index, group in grouped:
	
	comp_desc = ""

	# for each row in the group of same object rows
	for index, row in group.iterrows():
		# compile string with all descriptions in chronological order
		comp_desc = comp_desc + "\n\n" + str(row.iloc[2])
		comp_desc = comp_desc.strip()

	# Store the compiled description in order, in an array
	descriptions.append(comp_desc)

# Keep last row (latest update) of each group
final = grouped.nth(-1)

# Update the descriptions with the compiled ones in the df (data frame)
final["TextEntry"] = descriptions

# Get relevant rows in order
final = final[["ObjectID", "Title", "TextEntry"]]

print(final.head(20))

final.to_excel("./carlos_data/objs_w_title_n_desc.xlsx", engine="xlsxwriter")

"""
print(obj_w_desc.head())

# Convert back to normal DataFrame type (cant find better way for DataFrameGroupBy[Scalar] -> DataFrame)

# beautify
grouped = grouped[["Title", "TextEntry"]] # removed medium
# Write to excel file
grouped.to_excel("obj_w_desc.xlsx", engine="xlsxwriter")
"""