from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import torch

tokenizer = None
model = None
pipe = None

def load_model():
    device = 0 if torch.cuda.is_available() else -1
    global tokenizer, model, pipe
    tokenizer = AutoTokenizer.from_pretrained("raasikhk/carlos_bert_v2_2", revision="4f6590dd149a1cf31d0cc09fa6e2db13fdfc15f1")
    model = AutoModelForSequenceClassification.from_pretrained("raasikhk/carlos_bert_v2_2", revision="4f6590dd149a1cf31d0cc09fa6e2db13fdfc15f1", output_attentions=True)
    pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None, truncation=True, padding=True, device=device)

def classify(text: str) -> dict:
    predictions = pipe(text)
    
    classification = {}
    for prediction in predictions[0]:
        if prediction["label"] == "Jargon":
            classification["jargon"] = prediction["score"]
        elif prediction["label"] == "Subjective":
            classification["subjective"] = prediction["score"]
        elif prediction["label"] == "Gender":
            classification["gender"] = prediction["score"]
        elif prediction["label"] == "Social":
            classification["social"] = prediction["score"]

    return classification

def debias(text: str, classification: dict) -> str:
    biases = []
    if classification.get("jargon", 0) > 0.5:
        biases.append("jargon")
    if classification.get("subjective", 0) > 0.5:
        biases.append("subjective")
    if classification.get("gender", 0) > 0.5:
        biases.append("gender")
    if classification.get("social", 0) > 0.5:
        biases.append("social")
    
    # Placeholder for debiasing logic
    return "DEBIASED --> " + text

    return text