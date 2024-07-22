import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('bert/models/model_v2/bert_v2_epoch_stats_1.csv')

# Plot the data
plt.figure(figsize=(10, 6))

# Plot each column
for column in df.columns[1:]:
    plt.plot(df['Epoch'], df[column], label=column)

# Add labels and title
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.title('Training and Validation Metrics over Epochs')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()