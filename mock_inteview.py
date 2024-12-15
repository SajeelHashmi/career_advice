# simple function to maintain history for every user and provide career advice
# user a simple json file to store previous messages limit to 100 messages and destroy messages after 2 hours of being inactive


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import MessagesPlaceholder
from data import _create_new_chat, _add_message, _get_messages
import json
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser 
from langchain_core.messages.ai import AIMessage

load_dotenv()

class Interviewer:
    def __init__(self,id:int|None=None):
        if id:
            self.chat_id = id
        else:
            self.chat_id = _create_new_chat("mock_interview")
        self.chatbot = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
        )
        
        self.system_message = """You are an expert interviewer Your job is to stage a mock interview for the user.
Ask questions technical and all and at the end of the interview give response on what the user can do to interview or what the interview should not be very long
Ask technical and soft questions You have to prepare the user for any situation that they might fall upon 
Return Plain text without any markdown formating please"""
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



    def add_message(self, message: str, system_message: int):
        _add_message(self.chat_id, message, system_message)
    def first_response(self):
        msg = """Lets start your mock interview. Breifly Descibe the position your apply for so we can start the interview"""
        _add_message(self.chat_id, msg, 1)
        return msg




