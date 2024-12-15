from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import MessagesPlaceholder
from data import _create_new_chat, _add_message, _get_messages
import json
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser 
from langchain_core.messages.ai import AIMessage
load_dotenv()

class Job_Search:
    def __init__(self,id:int|None=None):
        if id:
            self.chat_id = id
        else:
            self.chat_id = _create_new_chat("career_advice")
        self.chatbot = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
        )
        
        self.system_message = """You are an expert career counsellor help Your job is to ask questions give insights and talk to the user in a way that advances their career.
Maintian a converstaional tone with the user donot give lenghty responses emulate how a real Career counsellor might interact with a person
Offer self reflection exercises and ways for the user to better themselves
Provide Feedback on answers talk in an easy going and comforting manner 
Ask Only one questions donot over complicate the exchange ask simple well structured questions and provide insights to the answers in the same manner
Your job is to be as approachable and easy to talk to as possible"""
    def invoke(self, text:str):
        # add message to the database

        # retrive all the messages from the database
        raw_messages = _get_messages(self.chat_id)
        print(raw_messages)
        cleaned_messages = [
            ("system",self.system_message),
        ]
        for  m in raw_messages:
            if m[1] == 1:
                cleaned_messages.append(("ai",m[0]))
            else:
                cleaned_messages.append(("user",m[0]))
        print(cleaned_messages)

        prompt = ChatPromptTemplate.from_messages(
            cleaned_messages + [("user","{text}")],
        )
        prompt = prompt.invoke({"text": text})
        self.add_message(text,0)

        print(text)
        print("message added")
        response= self.chatbot.invoke(prompt)
        response  = self.chatbot.invoke(prompt)

        print(response.content)
        self.add_message(response.content,1)
        
        return response.content
        # create a prompt
        # invoke the prompt


    def add_message(self, message: str, system_message: int):
        _add_message(self.chat_id, message, system_message)
    def first_response(self):
        msg = """Let's dive in. What are you thinking about in terms of career? Are you exploring options, aiming for a shift, or maybe trying to grow where you are?"""
        _add_message(self.chat_id, msg, 1)
        return msg




