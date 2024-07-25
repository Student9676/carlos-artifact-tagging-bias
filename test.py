# # CALCULATE ACCURACY

# import pandas as pd
# import transformers, torch

# """
# Remove uneecessay new lines
# remove duplicates within one cell
# Remove links?
# use keywords to make sure that correct classification is done
# make validation set more class balanced, i.e. equal num of examples for each category
# """
# # load data and rename TextEntry column
# df = pd.read_excel("carlos_data/preprocessed_data_v2.xlsx")
# df = df.rename(columns={"TextEntry":"Description"})

# # convert data to dictionary
# data = df.to_dict("records")

# # Split the data into train and validation and test sets
# from sklearn.model_selection import train_test_split 
# train_dict, test_dict = train_test_split(data, test_size=0.20, random_state=42)
# test_dict, validation_dict = train_test_split(test_dict, test_size=0.50, random_state=42)

# # Create Dataset objects
# from datasets import Dataset
# train_dataset = Dataset.from_list(train_dict)
# test_dataset = Dataset.from_list(test_dict)
# validation_dataset = Dataset.from_list(validation_dict)

# # Create DatasetDict
# from datasets import DatasetDict
# dataset = DatasetDict({
# 	"train": train_dataset,
# 	"test": test_dataset,
# 	"validation": validation_dataset
# })

# print(dataset)

# from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
# import torch

# device = 0 if torch.cuda.is_available() else -1

# import glob

# for filepath in glob.iglob('bert/models/model_v2/model/checkpoint*'):
    
#     print(filepath)

#     model = AutoModelForSequenceClassification.from_pretrained(filepath)
#     tokenizer = AutoTokenizer.from_pretrained(filepath)

#     pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None, truncation=True, padding=True, device=device)

#     # Replace with your test dataset
#     test_descriptions = dataset["test"]["Description"]

#     # Get predictions
#     predictions = pipe(test_descriptions)

#     labels= ["Subjective", "Gender", "Jargon", "Social"]

#     print("\nPartial correct score: ")

#     score = 0
#     total = 0
#     for p in predictions:

#         for i in range(4):
#             if p[i]["score"] >=0.5:
#                 prediction=1
#             else:
#                 prediction=0
            
#             if dataset["test"][i][labels[i]] == prediction:
#                 score +=1
#             total+=1
#     print(f"{score} / {total}")
#     print(score/total)

#     print("\nAll correct score: ")

#     score = 0
#     total = 0
#     for p in predictions:
#         all_c=True
#         for i in range(4):
#             if p[i]["score"] >=0.5:
#                 prediction=1
#             else:
#                 prediction=0
            
#             if dataset["test"][i][labels[i]] != prediction:
#                 all_c = False
#             total+=1
#             if (all_c):
#                 score+=1

#     print(f"{score} / {total}")
#     print(score/total)
#     print("---------------------")\


import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'test.csv'
df = pd.read_csv(file_path)

# Sort the DataFrame alphabetically by the 'Checkpoint' column
df_sorted = df.sort_values(by='Checkpoint')

# Plotting the line graph
plt.figure(figsize=(12, 6))

# Plot Partial Correct Percentage
plt.plot(df_sorted['Checkpoint'], df_sorted['Partial Correct Percentage'], label='Partial Correct Percentage', marker='o')

# Plot All Correct Percentage
plt.plot(df_sorted['Checkpoint'], df_sorted['All Correct Percentage'], label='All Correct Percentage', marker='o')

# Adding titles and labels
plt.title('Performance Metrics by Checkpoint')
plt.xlabel('Checkpoint')
plt.ylabel('Percentage')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)

# Display the plot
plt.tight_layout()
plt.show()
