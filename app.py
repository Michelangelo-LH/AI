# app.py
import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from functions import openai_assistant_function

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

# Load environment variables from .env file
load_dotenv(find_dotenv())


# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")


def my_function(text):
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    response = text.upper()
    return response


@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say("This is a test integartion with OpenAI, I'm processing your request...")
    # response = my_function(text)
    # response = draft_email(text)
    # response = openai_assistant_function(text)
    # say(response)

    # Call the openai_assistant_function and use say to send the response
    response = openai_assistant_function(text)
    say(response)

    # Call the openai_assistant_function with the say function
    # openai_assistant_function(text, say_func=say)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)


# Route for handling OpenAI assistant requests
@flask_app.route("/openai-assistant", methods=["POST"])
def openai_assistant_route():
    data = request.json
    user_input = data.get("user_input", "")
    
    # Call the openai_assistant_function with the user_input
    response = openai_assistant_function(user_input)

    return jsonify({"response": response})



# Run the Flask app
if __name__ == "__main__":
    flask_app.run(port=3000)  # Change the port to 3000 or any desired port