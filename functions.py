# functions.py
import os
import time
import openai
from openai import OpenAI
from openai import OpenAIError
from env_setup import AUTH_HEADERS, OPENAI_API_BASE_URL
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage


# Set up OpenAI organization and client
openai.organization = os.getenv("LOVEHOLIDAYS_ORG_ID")
client = OpenAI(
    api_key=AUTH_HEADERS['Authorization'].split(' ')[1],
    organization=openai.organization,
)
assistant_id = os.getenv("ASSISTANT_ID")



load_dotenv(find_dotenv())

# Your new function using the OpenAI assistant
def openai_assistant_function(user_input, name="Michelangelo"):
    try:
        print("Starting openai_assistant_function...")

        # Call the function to perform OpenAI operations
        response = perform_openai_operations(user_input)

        print("Response from perform_openai_operations:", response)

        if "content" in response:
            # Extract content from the response
            content = response["content"]
            print("Content extracted:", content)
            return content
        elif "error" in response:
            # Handle the case where an error occurred during OpenAI operations
            print("Error response:", response["error"])
            return response["error"]
        else:
            # Handle other unexpected cases
            print("Unexpected error response.")
            return "An unexpected error occurred during OpenAI operations."

    except Exception as e:
        # Handle Exceptions
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"


def perform_openai_operations(user_input):
    try:
        # Create a Thread with an initial user message
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        # Create and retrieve Run in a single step
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions="Use max 20 words in your response.",
        )

        # Wait for the run to complete (simple polling mechanism)
        while True:
            updated_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id)
            if updated_run.status == 'completed':
                break
            time.sleep(1)  # Wait for 1 second before checking again

        # Retrieve Messages from the Thread after the run is completed
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(thread.id)

        # Process the messages as needed
        response_content = None
        for message in messages.data:
            print(f"Role: {message.role}, Content: {message.content[0].text.value}")
            if message.role == "assistant":
                response_content = message.content[0].text.value

        # Return the generated response as a dictionary
        return {"content": response_content} if response_content else {"error": "No assistant response"}

    except OpenAIError as e:
        # Handle any errors that occur during the API calls
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {e}"}



