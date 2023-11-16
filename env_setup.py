# env_setup.py

#%%

import requests
import os
import hashlib
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Print the current working directory for debugging
print("Current Working Directory:", os.getcwd())

# Calculate the path to the .env file
current_dir = os.path.dirname(__file__)
project_root = os.path.join(current_dir, './')  # Adjust the path as necessary
env_path = os.path.join(project_root, '.env')

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# Retrieve the OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
# Define the OpenAI API URL
OPENAI_API_BASE_URL = 'https://api.openai.com/v1'

# Headers for Authorization
AUTH_HEADERS = {
    'Authorization': f'Bearer {OPENAI_API_KEY}',
    'OpenAI-Beta': 'assistants=v1'
}

# Make sure to add this at the end of env_setup.py
__all__ = ['load_dotenv', 'OPENAI_API_BASE_URL', 'AUTH_HEADERS']



# %%
# import requests

# def test_openai_api():
#     url = OPENAI_API_BASE_URL + "/engines/davinci/completions"
#     prompt = "Translate the following English text to French: 'Hello, world!'"
#     data = {
#         "prompt": prompt,
#         "max_tokens": 60
#     }

#     response = requests.post(url, json=data, headers=AUTH_HEADERS)
#     if response.status_code == 200:
#         print("Success! Response from OpenAI API:")
#         print(response.json())
#     else:
#         print("Failed to fetch data from OpenAI API")
#         print("Status Code:", response.status_code)
#         print("Response:", response.text)

# # Run the test function
# test_openai_api()
