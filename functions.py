from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage

load_dotenv(find_dotenv())

def draft_email(user_input, name="Michelangelo"):
    try:
        print("Starting draft_email function...")

        chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1, openai_api_key="OPENAI_API_KEY", openai_organization="LOVEHOLIDAYS_ORG_ID")

        # chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

        template = """
        
        You are a helpful assistant that drafts an email reply based on a new email.
        
        Your goal is to help the user quickly create a perfect email reply.
        
        Keep your reply short and to the point and mimic the style of the email so you reply in a similar manner to match the tone.
        
        Start your reply by saying: "Hi {name}, here's a draft for your reply:". And then proceed with the reply on a new line.
        
        Make sure to sign off with {signature}.
        
        """

        signature = f"Kind regards, \n\{name}"
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        human_template = "Here's the email to reply to, and consider any other comments from the user for a reply as well: {user_input}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        print("Before LLMChain initialization...")

        # Inspect Input Data
        print("user_input:", user_input)
        print("signature:", signature)
        print("name:", name)

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        response = chain.run(user_input=user_input, signature=signature, name=name)

        print("After LLMChain run...")

        return response
    except Exception as e:
        # Handle Exceptions
        print(f"An error occurred: {e}")


