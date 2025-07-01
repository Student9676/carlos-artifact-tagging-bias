import openai
import pandas as pd


def get_api_key():
    # Directly return the API key
    return "Enter your api key"


def chat_completions(api_key, messages, model_id):
    openai.api_key = api_key
    BASE_URL = "https://api.openai.com/v1"
    openai.api_base = BASE_URL

    try:
        response = openai.ChatCompletion.create(model=model_id, messages=messages)
        response_text = response.choices[0].message["content"]
        print(f"Response: {response_text}")  # Debug: Print the response for debugging
        return response_text
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, an error occurred while processing your request."


def convert_bias_labels(bias_labels):
    # Define the order of the biases
    biases = ["subjectivity bias", "gender bias", "jargon bias", "social bias"]

    # Create a dictionary to store the binary representation of each bias
    bias_dict = {bias: 0 for bias in biases}

    # Update the dictionary based on the provided bias labels
    for label in bias_labels:
        label = label.strip().lower()
        if label in bias_dict:
            bias_dict[label] = 1

    # Convert the dictionary values to the desired format
    result = " - ".join(str(bias_dict[bias]) for bias in biases)

    return result


def extract_bias_labels(response_text):
    # Initialize a list to hold detected bias types
    bias_labels = []

    # Add biases mentioned directly in the response text
    if "subjectivity bias" in response_text.lower():
        bias_labels.append("subjectivity bias")
    if "gender bias" in response_text.lower():
        bias_labels.append("gender bias")
    if "jargon bias" in response_text.lower():
        bias_labels.append("jargon bias")
    if "social bias" in response_text.lower():
        bias_labels.append("social bias")

    return bias_labels


def process_excel(file_path, api_key, model_id, row_numbers):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Check if the necessary columns are present
    required_columns = ["ObjectID", "Title", "TextEntry"]
    for col in required_columns:
        if col not in df.columns:
            print(f"Excel file must contain '{col}' column.")
            return

    # Filter the DataFrame based on provided row numbers
    if len(row_numbers) == 1:
        df = df.iloc[[row_numbers[0] - 1]]
    elif len(row_numbers) == 2:
        df = df.iloc[row_numbers[0] - 1 : row_numbers[1]]
    else:
        print("Invalid number of row numbers provided.")
        return

    # Initialize messages with system message
    system_message = [{"role": "system", "content": "You are a helpful assistant."}]

    # Process each row
    for index, row in df.iterrows():
        combined_text = f"detect any bias in the following text entry: Title: {row['Title']} TextEntry: {row['TextEntry']}"
        messages = system_message + [{"role": "user", "content": combined_text}]
        response_text = chat_completions(api_key, messages, model_id)

        # Extract bias labels from response
        bias_labels = extract_bias_labels(response_text)
        print(
            f"Extracted bias labels: {bias_labels}"
        )  # Debug: Print the extracted bias labels
        binary_result = convert_bias_labels(bias_labels)

        print(f"Processed row {index + 1}/{len(df)}: {binary_result}")
        print(
            f"Original API Response: {response_text}"
        )  # Print the response text from the API

        # Optionally, you can store the original API response and bias results in new DataFrame columns
        df.at[index, "API_Response"] = response_text
        df.at[index, "Bias_Labels"] = binary_result

    # Optionally, save the updated DataFrame to a new Excel file
    df.to_excel("processed_output.xlsx", index=False)


def main():
    api_key = get_api_key()
    if not api_key:
        print("API key not found.")
        return

    model_id = "ft:gpt-3.5-turbo-1106:emory-center-for-ai-learning:bd2300:9qmS1lyX"

    # Correct file path for the uploaded Excel file
    file_path = "/Users/liuchang/Downloads/clean_data_annotated_shuffled_v3.xlsx"

    while True:
        # Get user input for row number or range of row numbers
        input_row_numbers = input(
            "Enter row number or range of row numbers (e.g., '1' or '1-5') or 'exit' to stop: "
        ).strip()
        if input_row_numbers.lower() == "exit":
            print("Exiting program.")
            break

        if "-" in input_row_numbers:
            row_numbers = input_row_numbers.split("-")
            row_numbers = [
                int(num.strip()) for num in row_numbers if num.strip().isdigit()
            ]
        else:
            row_numbers = [int(input_row_numbers)]

        # Process the Excel file
        process_excel(file_path, api_key, model_id, row_numbers)


if __name__ == "__main__":
    main()
