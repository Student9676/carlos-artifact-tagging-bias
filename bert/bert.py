import pandas as pd
import transformers, torch

df = pd.read_csv('carlos_data/clean_data_annotated_v2.csv', encoding='latin1')
df = df.head(101)

print(df.head(3))

descs = df['TextEntry'].tolist()
bias_clas = df[['Subjective', 'Gender', 'Jargon', 'Social']].values

print(descs[0])

tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize the texts
inputs = tokenizer(descs, padding=True, truncation=True, return_tensors="pt", max_length=512)

from torch.utils.data import Dataset, DataLoader

class BiasDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.inputs.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item

dataset = BiasDataset(inputs, bias_clas)

dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

model = transformers.BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=4)
model.train()

from torch.nn import BCEWithLogitsLoss

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
loss_fn = BCEWithLogitsLoss()

# Training loop
epochs = 3
for epoch in range(epochs):
    total_loss = 0
    for batch in dataloader:
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(input_ids=batch['input_ids'],
                        attention_mask=batch['attention_mask'],
                        labels=batch['labels'])
        
        loss = outputs.loss
        total_loss += loss.item()
        
        # Backward pass
        loss.backward()
        optimizer.step()
    
    print(f"Epoch {epoch + 1}, Loss: {total_loss / len(dataloader)}")

model.save_pretrained('/home/raasikhk/Coding/ai.xperience/carlos-artifact-tagging-bias/bert/model')
tokenizer.save_pretrained('/home/raasikhk/Coding/ai.xperience/carlos-artifact-tagging-bias/bert/model')

# import transformers
# model = transformers.BertForSequenceClassification.from_pretrained('bert/model')
# tokenizer = transformers.BertTokenizer.from_pretrained('path_to_save_model')

model.eval()

validation_texts = ["Harsh, uncomfortably brilliant, usually reflected light.  W. April 1993 descriptor moved.", "December 1992 lead-in term added. January 1991 alternate term added. Object fumigated in Orkin's Piedmont vault with Vikane in 1994"]
validation_labels = [[1, 0, 0, 0], [0, 0, 1, 0]]

# Tokenize validation texts
validation_inputs = tokenizer(validation_texts, padding=True, truncation=True, return_tensors="pt", max_length=512)

# Convert labels to tensor
validation_labels = torch.tensor(validation_labels, dtype=torch.float)

with torch.no_grad():
    outputs = model(**validation_inputs)
    logits = outputs.logits
    predictions = torch.sigmoid(logits)

# Print predictions
print(predictions)

