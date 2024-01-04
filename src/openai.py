import requests
from openai import OpenAI

from .base import GLOBAL
from .prompts import system_msg

openai_client = OpenAI(api_key=GLOBAL['openai_token'])


def call_openai_api(input_prompt):
    generated_text = None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GLOBAL['openai_token']}"
    }
    body = {
        "model": GLOBAL['openai_model'],
        "prompt": input_prompt,
        "max_tokens": GLOBAL['openai_max_token'],
        "temperature": GLOBAL['openai_temperature']
    }
    
    out = requests.post(GLOBAL['openai_url'], json=body, headers=headers).json()
    if out.get('choices', None):
        generated_text = out['choices'][0]['text'].strip('\n')

    return generated_text


def call_openai_api_v2(input_context):
    completion = openai_client.chat.completions.create(
                                            model="gpt-3.5-turbo",
                                            #model="gpt-3.5-turbo-1106",
                                            #response_format={ "type": "json_object" },
                                            messages=[
                                                {"role": "system", "content": system_msg},
                                                {"role": "user", "content": input_context}
                                            ]
                                            )

    return completion.choices[0].message