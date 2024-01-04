import google.generativeai as genai
import os
from google.generativeai import chat

from .base import GLOBAL
from .prompts import system_msg, transaction_based_prompt


GOOGLE_API_KEY = GLOBAL['gemini_token']
genai.configure(api_key=GOOGLE_API_KEY)



def initialize_chat_old(system_msg):
    chat_session = chat(model='models/chat-bison-001',
            context=system_msg,
            examples=[('i am looking for birthday gift for my daughter. can you show me good products for her ?','sure. but i need few info for better suggestions. could you please give me what gender belongs women/kids ? also what metal you would like to buy gold or diamond ?'),('she is kid. and i would like to buy gold.','that is great. could you tell me what product you would like to buy ? for example bangle/chain/rings/earring etc.'),('bangle','sure.')],
            messages=['hello. welcome!'])
    
    return chat_session

def initialize_chat(system_msg):
    gemini_model = genai.GenerativeModel('gemini-pro')
    gemini_chat = gemini_model.start_chat(history=[{'role':'user',
                                                    'parts': [system_msg]
                                                    },
                                                    {'role':'model',
                                                    'parts': ['okay.']
                                                    }])

    return gemini_chat

def chat_with_gemini(user_text="Hello!"):
    response = gemini_chat.send_message(user_text)
    print(response.text)
    return response.text

def chat_with_gemini_old(user_text="Hello!"):
    response = gemini_chat.reply(user_text)
    
    return response.last

def call_gemini_api(input_prompt):
    model = genai.GenerativeModel('gemini-pro')
    print(input_prompt)
    print("=============")
    try:
        response = model.generate_content(input_prompt)
        print(response.text)
    except Exception as err:
        print(err)
    
    return response.text

gemini_chat = initialize_chat(system_msg)
#gemini_chat.set_response_format("json")


if __name__=="__main__":
    text = "Hello"
    response = chat_with_gemini(text)
    print(response)