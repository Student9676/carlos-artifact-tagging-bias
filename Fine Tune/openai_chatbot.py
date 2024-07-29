import openai
import datetime

def chat_completions(api_key, messages, model_id):
    openai.api_key = api_key
    BASE_URL = "https://api.openai.com/v1"
    openai.api_base = BASE_URL

    response_stream = openai.ChatCompletion.create(
        model=model_id,
        messages=messages,
        stream=True
    )
    response_text = ""
    for chunk in response_stream:
        if chunk.choices[0].delta.get("content") is not None:
            response_text += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")

    print()  # Add a newline after the complete response
    return response_text

if __name__ == "__main__":
    # Hardcoded API key
    api_key = "Your OpenAI API key"

    # Hardcoded model ID for the fine-tuned model
    model_id = "ft:gpt-3.5-turbo-1106:emory-center-for-ai-learning:bd2200:9q564rtN"

    # Initialize the message history with the system message
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    print("Welcome to the chat! Type 'exit' to end the conversation.")
    while True:
        # Get the user query
        user_query = input("User: ")

        # Break the loop if the user types 'exit'
        if user_query.lower() == 'exit':
            break

        # Add the user's message to the message history
        messages.append({"role": "user", "content": user_query})

        # Get the response
        response = chat_completions(api_key, messages, model_id)

        # Add the assistant's message to the message history
        messages.append({"role": "assistant", "content": response})

        print()  # Add a blank line between each conversation turn

    # Get the current time
    current_time = datetime.datetime.now().time()

    # Output a different message based on the time of day
    if current_time < datetime.time(12):
        print("Goodbye! Have a great morning!")
    elif current_time < datetime.time(18):
        print("Goodbye! Enjoy your afternoon!")
    else:
        print("Goodbye! Have a pleasant evening!")
