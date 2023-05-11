import openai
import dotenv
import os
from typing import List
from messages import MessageHandler

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


class Bot:
    def __init__(self, conversation: str, message_handler:MessageHandler, model:str="gpt-3.5-turbo", 
                 temperature:float=0.7, max_tokens:int=150, delay:int=2) -> None:
        self.conversation = conversation
        self.message_handler = message_handler
        self.context = message_handler.fetch_context(conversation)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.delay = delay

    def respond(self)->str:
        messages = self.context
        messages += self.message_handler.fetch_messages(self.conversation)
        print(messages)
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return completion.choices[0].message.content
