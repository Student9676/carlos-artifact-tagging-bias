# import requests

# API_URL = "https://api-inference.huggingface.co/models/valurank/distilroberta-bias"
# headers = {"Authorization": "see gdrive"}

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()


# text = "Coquero (Male Coca-Chewer) with Lime Dipper and Poporo (Lime Container)"

# output = query({
# 	"inputs": text,
# })

# print("Text:\n" + text + "\n")
# print("Probability of text being neutral:")
# print(output[0][0]["score"])
# print()
# print("Probability of text being BIASED:")
# print(output[0][1]["score"])

# Use a pipeline as a high-level helper
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

# if tokenizer == None:
# tokenizer = AutoTokenizer.from_pretrained("raasikhk/carlos_bert_v2_2", revision="4f6590dd149a1cf31d0cc09fa6e2db13fdfc15f1")
# if model == None:
# model = AutoModelForSequenceClassification.from_pretrained("raasikhk/carlos_bert_v2_2", revision="4f6590dd149a1cf31d0cc09fa6e2db13fdfc15f1", output_attentions=True)

# pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None, truncation=True, padding=True, device=0)
pipe = pipeline("text-classification", model="valurank/distilroberta-bias") 
# print(pipe("Sinker\n\nNOTE: UPDATED in June 2021 with information from 1984 accession worksheet.\n\nA February 14, 1997 file memo from registrar Lori Iliff discussed how sources and provenance were determined for objects that were believed to have an Etowah or Etowah-related provenance.  This memo did not discuss the X.0600-X.0697 numbered objects, as the sources and provenance of those objects had been discussed in a March 1990 memo.  Information regarding the objects in the 1997 memo came from the Accession Log I (green-blue colored ledger) and old accession sheets. According to Lori's memo it was unclear when the accession log was started, but it was on or prior to 1984.  The accession worksheets had been created in 1984.\n\nAccording to Lori's memo, the designation of Etowah as provenance and Phillips Academy as source on the accession worksheets seemed arbitrary and not based on prior museum records.  Therefore the designation of Etowah or Phillips Academy based solely on an accession worksheet may be suspect. Below is a summary of what was found for this object.\n\nX.0232.024 - According to the memo, the accession log lists no source, but lists Etowah as provenance.  The memo does not mention an accession worksheet. There is a 1984 accession worksheet in the object file.  It notes the provenance as Georgia, Etowah Mounds and does not note a source.\n\nThe memos from the 1990s do not mention the \"Specimen Record\" worksheets housed in the blue fabric-covered binders. A few of these worksheets contain notes added by Lori Iliff in 1994.  It is unclear why these worksheets are not mentioned in the 1990s memos, but for completeness, their information is noted here.  It is however, unclear when these worksheets were created, by whom, and where the information in the worksheets came from.  Many have notes regarding packing objects for storage in 1982, so it can be assumed these were created in 1982 or earlier. There is one Specimen Record for X.0232.023, X.0232.024, X.0280.001, X.0280.002, X.0281 and X.0282.  The Specimen Record does not list a provenance, and W.H. Ferguson is listed as the source.\n\nThe catalog for the 1982 \"A Preview of the Collections\"exhibition in Schatten Gallery lists the credit line for X.0232.024 as \"Gift of W.H. Ferguson\", but there is no indication as to where this information came from.\n\nLuminescence induced by the absorption of infrared radiation, visible light, or ultraviolet radiation.  RHDEL2.\n\nIdentified as Jasper by William Size."))
print(pipe("According to Lori's memo, the designation of Etowah as provenance and Phillips Academy as source on the accession worksheets seemed arbitrary and not based on prior museum records.  Therefore the designation of Etowah or Phillips Academy based solely on an accession worksheet may be suspect. Below is a summary of what was found for this object."))