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

We use **Python 3.11.9** but other recent versions most likely work (we have not tested them).

## Data Cleaning

Load data as csv files into a folder called `carlos_data` of the following format:  

* Objects: `carlos_data/ObjectTables/Objects.csv`
  * COLUMNS: `["ID", "TextEntry", "EnteredDate"]`
* Descriptions: `carlos_data/ObjectTables/TextEntries.csv`
  * COLUMNS: `["ObjectID", "Medium"]`
* Titles: `carlos_data/ObjectTables/ObjTitles.csv`
  * COLUMNS: `["ObjectID", "Title"]`

Run `clean_data.py`

```
python clean_data.py
```

This will create a csv file called `clean_data.csv` in the folder you created of the following format:

* COLUMNS: `["", """ObjectID", "Title", "TextEntry", "Subjective", "Gender", "Jargon", "Social", "Subjective Label", "Gender Label", "Jargon Label", "Social Label"]`

The unnamed column (the first one) has indices that match up with Excel's indices if the csv is opened there. This is to help keep track of annotations. 

The final step is to get annotated data of the same format as `clean_data.csv` into the `carlos_data` folder called annotated_data.csv i.e. an edited version with annotations of `clean_data.csv`.

## BERT Fine-tuning and Testing

All fine-tuning code is present in the `bert/model/bert.ipynb` Jupyter notebook.

### Data Preprocessing

Edit `bert/preprocess.py` and change the variable `num_annotated` to the number of rows you annotated (assuming the first n rows excluding the titles row are annotated data). **Project members:** set `annotated = "default"` if you have our annotated data. Then run this file to get preprocessed data called `preprocessed_data.csv`

```
# Assuming you have edited the script's num_annotated variable
python bert/preprocess.py
```
### Sentence-Level Preprocessing (Optional)

Additionally, we have introduced a deeper cleaning method to handle and preprocess text data effectively. The file name is in `bert/sentence_preprocess.py`:
- Text entries are split into individual sentences, allowing more granular analysis.
- Each sentence retains its associated labels and metadata (e.g., `ANNOTATED?`, `ObjectID`).
- Labels are standardized into consistent formats (e.g., lists for label fields) to ensure compatibility across downstream tasks.

To use the enhanced cleaning:
1. Ensure that your annotated data follows the same structure as provided in our sample dataset.
2. Run the preprocessing script as follows to generate `sentence_level_preprocessed_data.csv` with sentence-level granularity:
3. Make sure to change the file name in the BERT script as well if needed.
   
### Training

Preprocess the data, generate analytics, train the model, pull model from HuggingFace (skip if you fine-tuned yourself -- fine-tuned version is available on HuggingFace for quicker testing), test the model, and generate metrics by following the code blocks in order. Headings are present as dividers for organization.

#### Logs

Use tensorboard to see the notebook's produced logs and our (provided) logs.

```
tensorboard --logdir bert/logs
```

### Testing

Scroll to the end of the notebook to find the testing section where the model can be tested and metrics are calculated.

## ChatGPT Fine-tuning and Testing
For data processing, we used a similar cleaning process as when preparing training data for BERT. Both ChatGPT and BERT fine-tuning utilized the same dataset, with the data formatted into JSONL for GPT fine-tuning.

Due to limited resources, the GPT model was fine-tuned with a dataset of 288 entries. For more details on the training dataset, refer to the file "Training data."

To test the fine-tuned model, run the Python script "GPT_Chatbox_MI." If you want to try custom input or output formatting, use the following files:
- openai_chatbot(output with binary result)
- process_bias_detection_by_objectID.py
- process_bias_detection_by_rowNumber.py

For accuracy testing methods, see the code in the "accuracy" folder.


## Additional Information

Our paper is not yet published but can be found [here](https://drive.google.com/file/d/1BwXwciVGM6w-nuZKwceYzyzuNmEPcq1s/view?usp=sharing). Our HuggingFace model repository can be found [here](https://huggingface.co/raasikhk/carlos_bert_v2_2).

## Contributors

* **Raasikh Kanjiani**
* **Lina Li**
* **Chang Liu**
* **Jessie Ni**
* **Jaroy Wei**
* **Sophia Yoon**
