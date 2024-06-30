from afinn import Afinn
import pandas as pd
import os
from datetime import datetime

def file_exists(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    return os.path.exists(file_path)

afinn = Afinn()

text = "I love the hate"

score = afinn.score(text)

df = pd.DataFrame({"Text": text,
				   "AFINN Score": score}, 
                   index=[datetime.now()])

if file_exists("AFINN_test_output.csv"):
	df.to_csv('./AFINN_test_output.csv', mode='a', index=True, header=False, sep=",")
else:
	df.to_csv('./AFINN_test_output.csv', mode='w', index=True, index_label="Time", header=True, sep=",")