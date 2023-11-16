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
# %%
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



# Extract and Store the Assistant ID
assistant_id = my_assistant.id

# Store the Assistant ID in the .env file
with open(".env", "a") as env_file:
    env_file.write(f"\nASSISTANT_ID={assistant_id}")



# Retrieve the Assistant using the stored ID
my_assistant = openai.beta.assistants.retrieve(assistant_id)


# Print the Assistant Details
print(my_assistant)


thread = client.beta.threads.create()

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Why do we need guidelines?",
      "file_ids": [file.id]
    }
  ]
)


run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=my_assistant.id,
  instructions="Use the overview file to triage the user asking more questions about his query.",
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages)
# %%

