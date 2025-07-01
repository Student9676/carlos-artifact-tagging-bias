import os
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
from datetime import datetime


def file_exists(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    return os.path.exists(file_path)


# Load the Hurtlex lexicon
hurtlex_path = "/Users/raasikh/Documents/Coding/ai.xperience/packages/hurtlex/lexica/EN/1.2/hurtlex_EN.tsv"
hurtlex = pd.read_csv(hurtlex_path, sep="\t")

# Preprocess text data
nltk.download("punkt")
text = "Oriental art is very awesome; woman is depicted naked in the artwork."
tokens = word_tokenize(text.lower())

# Compare text data with Hurtlex
offensive_words = hurtlex["lemma"].tolist()
found_offensive_words = [word for word in tokens if word in offensive_words]

print("Offensive words found:", found_offensive_words)

if len(found_offensive_words) == 0:
    found_offensive_words.append("-")

df = pd.DataFrame(
    {"Text": text, "Offensive words found": found_offensive_words},
    index=[datetime.now()],
)

if file_exists("hurtlex_test_output.csv"):
    df.to_csv(
        "./bias_algos/hurtlex_test_output.csv",
        mode="a",
        index=True,
        header=False,
        sep=",",
    )
else:
    df.to_csv(
        "./bias_algos/hurtlex_test_output.csv",
        mode="w",
        index=True,
        index_label="Time",
        header=True,
        sep=",",
    )
