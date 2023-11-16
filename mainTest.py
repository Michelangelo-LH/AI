import openai
from openai import OpenAI
import os
import json
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv

# --------------------------------------------------------------
# Load OpenAI API Token From the .env File
# --------------------------------------------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("LOVEHOLIDAYS_ORG_ID")

client = OpenAI(
  organization=openai.organization,
)
client.models.list()

# Uploade file
file = client.files.create(
  file=open("data/overview.txt", "rb"),
  purpose='assistants'
)

# Create Assistant
my_assistant = openai.beta.assistants.create(
    description="Brand Platform Assistant",
    instructions="You are a Brand and Design System Guru representing loveholidays. Answer questions based on the informations  in the uploaded files. Answer in max 20 words.",
    name="loveholidays Design Assistant",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[file.id]
)
print(my_assistant)


# Extract and Store the Assistant ID
assistant_id = my_assistant.id

# Store the Assistant ID in the .env file
with open(".env", "a") as env_file:
    env_file.write(f"\nASSISTANT_ID={assistant_id}")

# Print the Assistant Details
print(my_assistant)

# Retrieve the Assistant using the stored ID
my_assistant = openai.beta.assistants.retrieve(assistant_id)
print(my_assistant)



thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is our Primary color?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=my_assistant.id,
  model="gpt-4-1106-preview",
  instructions="Use the overview file to triage the user asking more questions about his query.",
  tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
)


run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)




# Retrieve the message object
message = client.beta.threads.messages.retrieve(
  thread_id=thread.id,
  message_id="..."
)

# Extract the message content
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