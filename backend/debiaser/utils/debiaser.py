from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import torch
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


tokenizer = None
model = None
pipe = None
device = None

def load_model():
    global tokenizer, model, pipe, device
    device = 0 if torch.cuda.is_available() else -1
    if pipe is not None:
        return
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

    print(f"Classification: {classification}")
    return classification

def debias(text: str, classification: dict) -> str:
    biases = []
    if classification.get("jargon", 0) > 0.5:
        biases.append("jargon terms")
    if classification.get("subjective", 0) > 0.5:
        biases.append("subjective language")
    if classification.get("gender", 0) > 0.5:
        biases.append("gender bias")
    if classification.get("social", 0) > 0.5:
        biases.append("social bias")

    biases_str = ""
    if len(biases) == 2:
        biases_str = f"{biases[0]} and {biases[1]}."
    if len(biases) > 2:
        for i, bias in enumerate(biases):
            if i == len(biases) - 1:
                biases_str += f"and {bias}."
            else:
                biases_str += f"{bias}, "

    if not biases:
        return text

    if os.getenv("TEST") == "t":
        return "DEBIASED --> "  + text

    role_prompt = f"""
    You are an expert artifact curator. You are tasked with removing specific 
    biases and issues from a given text. The issues include {biases_str}.
    Your goal is to rewrite the text to eliminate these issues with minimal changes
    and preserve the original meaning.
    """
    prompt = f"""
    The following text in quotes contains {biases_str}.
    Please rewrite the text to remove these issues by 
    making minimal changes and preserving the original meaning.

    "{text}"
    """

    response = openai.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": prompt}
        ],
    )

    debiased_text = response.choices[0].message.content.strip()

    return debiased_text