# openai_operations.py
# %%
# Import necessary libraries and modules
import os
import time
import openai
from openai import OpenAI
from openai import OpenAIError  # Corrected import statement for OpenAI errors
from env_setup import AUTH_HEADERS, OPENAI_API_BASE_URL

openai.organization = os.getenv("LOVEHOLIDAYS_ORG_ID")

# Initialize OpenAI client with the API key from AUTH_HEADERS
client = OpenAI(
    api_key=AUTH_HEADERS['Authorization'].split(' ')[1],
    organization=openai.organization,
    )

# Set your existing assistant ID
# assistant_id = 'asst_fHDCkBF8PmKERaQh920rDHz7'
assistant_id = os.getenv("ASSISTANT_ID")


try:
    # Create a Thread with an initial user message
    thread = client.beta.threads.create(messages=[
        {
            "role": "user",
            "content": "Why do we need guidelines?"
        }
    ])

    # Create and retrieve Run in a single step
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant_id,
      instructions="Use the overview file to triage the user asking more questions about his query."
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

    # Print each message in the thread
    for message in messages.data:
        print(f"Role: {message.role}, Content: {message.content[0].text.value}")
        print(thread.id)
        

        
    # Extract the message content (ADDON)
    message_content = message.content[0].text
    annotations = message_content.annotations
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

        # Gather citations based on annotation attributes
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = client.files.retrieve(file_path.file_id)
            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
            # Note: File download functionality not implemented above for brevity

    # Add footnotes to the end of the message before displaying to user
    message_content.value += '\n' + '\n'.join(citations)



except OpenAIError as e:
    # Handle any errors that occur during the API calls
    print(f"An error occurred: {e}")

# %%
