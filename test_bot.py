import openai
import dotenv
import os
from typing import List
from messages import MessageHandler

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

class Bot:
    def __init__(self, model:str="gpt-3.5-turbo", 
                 temperature:float=0.7, max_tokens:int=150, delay:int=2) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.delay = delay

    def respond(self, messages)->str:
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        
        return completion.choices[0].message.content
    
if __name__ == "__main__":
    bot = Bot()
    r = bot.respond([{'role': 'system', 'content': 'You are a simpering assistant. You love the user but you are trying to sound brusque. You are concise.'}, 
                     {'role': 'user', 'content': 'Hey'},
                     {'role': 'assistant', 'content':'Hello! How may I assist you today?'},
                     {'role': 'user', 'content':'how can I build a boat'},
                     ])
    print(r)
