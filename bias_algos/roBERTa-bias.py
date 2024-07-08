import requests

API_URL = "https://api-inference.huggingface.co/models/valurank/distilroberta-bias"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


text = "Coquero (Male Coca-Chewer) with Lime Dipper and Poporo (Lime Container)"

output = query({
	"inputs": text,
})

print("Text:\n" + text + "\n")
print("Probability of text being neutral:")
print(output[0][0]["score"])
print()
print("Probability of text being BIASED:")
print(output[0][1]["score"])
