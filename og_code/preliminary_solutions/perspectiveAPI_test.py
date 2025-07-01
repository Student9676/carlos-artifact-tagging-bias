import os
from googleapiclient import discovery
import json
import pandas as pd
from datetime import datetime


def file_exists(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    return os.path.exists(file_path)


API_KEY = "see gdrive"

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

attribute_dict = {
    "TOXICITY": {},
    "SEVERE_TOXICITY": {},
    "IDENTITY_ATTACK": {},
    "INSULT": {},
    "PROFANITY": {},
    "THREAT": {},
    "AFFINITY_EXPERIMENTAL": {},
    "COMPASSION_EXPERIMENTAL": {},
    "CURIOSITY_EXPERIMENTAL": {},
    "NUANCE_EXPERIMENTAL": {},
    "PERSONAL_STORY_EXPERIMENTAL": {},
    "REASONING_EXPERIMENTAL": {},
    "RESPECT_EXPERIMENTAL": {},
}

text = "Smiling Little Girl Seated on a Table, Wearing a Pinafore"

analyze_request = {"comment": {"text": text}, "requestedAttributes": attribute_dict}

response = client.comments().analyze(body=analyze_request).execute()
dump = json.dumps(response, indent=2)

parsed_response = json.loads(dump)

response_dict = {"Text": text}

for attribute in attribute_dict:
    print(attribute)
    probability = parsed_response["attributeScores"][attribute]["summaryScore"]["value"]
    print(probability)
    print()
    response_dict.update({attribute: probability})

df = pd.DataFrame(response_dict, index=[datetime.now()])
if file_exists("perspectiveAPI_test_output.csv"):
    df.to_csv(
        "./bias_algos/perspectiveAPI_test_output.csv",
        mode="a",
        index=True,
        header=False,
        sep=",",
    )
else:
    df.to_csv(
        "./bias_algos/perspectiveAPI_test_output.csv",
        mode="w",
        index=True,
        index_label="Time",
        header=True,
        sep=",",
    )
