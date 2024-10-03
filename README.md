# Carlos Artifact Tagging Bias

This repository contains code for our bias detection and mitigation pipeline. This code is designed for the Michael C. Carlos Museum’s artifact description database. Our BERT model is fine-tuned for multi-label text classification. Given an artifact description, it returns the categories of bias present. These results, along with the description, is then fed to our GPT-4o chatbot which returns an unbiased description.

## Overview

The goal of the project is to explore potential cultural, historical, or systemic biases in artifact descriptions and tagging. Using a combination of data management techniques and bias analysis algorithms, we aim to provide more equitable and accurate metadata for the museum's collection.

## Installation

To set up the project on your local machine:

Clone the repository:

```
git clone https://github.com/Student9676/carlos-artifact-tagging-bias
```

Install the required dependencies:

```
pip install -r requirements.txt
```

## Data Cleaning

Load data as csv files into a folder called `carlos_data` of the following format:  

*   Objects: `carlos_data/ObjectTables/Objects.csv`
    *   COLUMNS: `["ID", "TextEntry", "EnteredDate"]`
*   Descriptions: `carlos_data/ObjectTables/TextEntries.csv`
    *   COLUMNS: `["ObjectID", "Medium"]`
*   Titles: `carlos_data/ObjectTables/ObjTitles.csv`
    *   COLUMNS: `["ObjectID", "Title"]`

Run `prepare_for_annotation.py`

```
python prepare_for_annotation.py
```

This will create a csv file called `clean_data.csv` in the folder you created of the following format:

*   COLUMNS: `["ObjectID", "Title", "TextEntry", "Subjective", "Gender", "Jargon", "Social", "Subjective Label", "Gender Label", "Jargon Label", "Social Label"]`

Final step is to get annotated data of the same format as `clean_data.csv` into the `carlos_data` folder called `annotated_data.csv`

## BERT Fine-tuning and Testing

All code is present in the `bert/model/bert.ipynb Jupyter notebook.`

### Training

Preprocess the data, generate analytics, train the model, pull model from HuggingFace (skip if you fine-tuned yourself -- fine-tuned version is available on HuggingFace for easier testing), test the model, and generate metrics by following the code blocks in order.

### Testing

Scroll to the end of the notebook to find the testing code where the model is pulled directly from a HuggingFace repository.

## Additional Information

Our paper is not yet published and can be found [here](https://drive.google.com/file/d/1BwXwciVGM6w-nuZKwceYzyzuNmEPcq1s/view?usp=sharing). Our HuggingFace model repository can be found [here](https://huggingface.co/raasikhk/carlos_bert_v2_2).

## Contributors

*   **Raasikh Kanjiani**
*   **Lina Li**
*   **Chang Liu**
*   **Jessie Ni**
*   **Jaroy Wei**
*   **Sophia Yoon**