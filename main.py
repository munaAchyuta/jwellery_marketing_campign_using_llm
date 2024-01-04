"""Main module."""
import warnings
warnings.filterwarnings('ignore')

from typing import Dict, List, Optional, Union, Annotated
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi import UploadFile, File, Form, Body, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette import status
import aiofiles
from sqlalchemy.orm import Session 
from PIL import Image
import base64
from io import BytesIO

from src.base import BaseClass
from src.logger import logger
from src.ocr import extract_text, perform_ocr
from src.gemini import chat_with_gemini, chat_with_gemini_old, call_gemini_api
from src.gemini import transaction_based_prompt
from src.restapi_models import (DocItem,
                              QuestionAnswerItem,
                              ProcessDocItem)

from src.db.db import get_db
from src.db import schemas, crud
from src.db import default_record_create

#default_record_create.create_default_recommend_product()

db_dependency = Annotated[Session, Depends(get_db)]

baseclass_obj = BaseClass()

app = FastAPI()


class Item(BaseModel):
    text: str

class UserItem(BaseModel):
    mail: str

# Load Complementary product data
complementary_products_df = pd.DataFrame([{'name':'Layered Beaded Necklace','product_category':'chain','description':'Layered Beaded Necklace','price':13000.0,'image_url':'sample_complementary_data\\layer_necklace.PNG'},
                {'name':'Gleaming Gold Necklace','product_category':'chain','description':'Gleaming Gold Necklace','price':49000.0,'image_url':'sample_complementary_data\\Gleaming Gold Necklace.PNG'},
                {'name':'Elegant Gold Finger Ring','product_category':'ring','description':'Elegant Gold Finger Ring','price':27000.0,'image_url':'sample_complementary_data\\Elegant Gold Finger Ring.PNG'},
                {'name':'Mesmerising Twisted Gold Ring','product_category':'ring','description':'Mesmerising Twisted Gold Ring','price':43000.0,'image_url':'sample_complementary_data\\Mesmerising Twisted Gold Ring.PNG'}])

# Load user transaction data
user_transaction_df = pd.DataFrame([{'name':'neha@gmail.com','gender':'Women','product_category':'chain','metal':'gold','description':'Layered Beaded Necklace','price':13000.0,'image_url':'sample_complementary_data\\layer_necklace.PNG'},
                {'name':'neha@gmail.com','gender':'Women','product_category':'chain','metal':'gold','description':'Gleaming Gold Necklace','price':49000.0,'image_url':'sample_complementary_data\\Gleaming Gold Necklace.PNG'},
                {'name':'neha@gmail.com','gender':'Women','product_category':'ring','metal':'diamond','description':'Elegant Gold Finger Ring','price':27000.0,'image_url':'sample_complementary_data\\Elegant Gold Finger Ring.PNG'},
                {'name':'ramesh@gmail.com','gender':'Men','product_category':'ring','metal':'gold','description':'Mesmerising Twisted Gold Ring','price':43000.0,'image_url':'sample_complementary_data\\Mesmerising Twisted Gold Ring.PNG'},
                {'name':'ramesh@gmail.com','gender':'Men','product_category':'Kada','metal':'gold','description':'Mesmerising Twisted Gold Ring','price':43000.0,'image_url':'sample_complementary_data\\Mesmerising Twisted Gold Ring.PNG'},
                {'name':'ramesh@gmail.com','gender':'Men','product_category':'chain','metal':'gold','description':'Mesmerising Twisted Gold Ring','price':43000.0,'image_url':'sample_complementary_data\\Mesmerising Twisted Gold Ring.PNG'},
                {'name':'ramesh@gmail.com','gender':'Men','product_category':'ring','metal':'gold','description':'Mesmerising Twisted Gold Ring','price':43000.0,'image_url':'sample_complementary_data\\Mesmerising Twisted Gold Ring.PNG'}])

# Load Complementary product data
new_products_df = pd.DataFrame([{'product_id':1,'name':'Layered Beaded Necklace','product_category':'chain','description':'Layered Beaded Necklace','price':13000.0,'image_url':'sample_complementary_data\\layer_necklace.PNG'},
                {'product_id':2,'name':'Gleaming Gold Necklace','product_category':'chain','description':'Gleaming Gold Necklace','price':49000.0,'image_url':'sample_complementary_data\\Gleaming Gold Necklace.PNG'},
                {'product_id':3,'name':'Elegant Gold Finger Ring','product_category':'ring','description':'Elegant Gold Finger Ring','price':27000.0,'image_url':'sample_complementary_data\\Elegant Gold Finger Ring.PNG'},
                {'product_id':4,'name':'Mesmerising Twisted Gold Ring','product_category':'ring','description':'Mesmerising Twisted Gold Ring','price':43000.0,'image_url':'sample_complementary_data\\Mesmerising Twisted Gold Ring.PNG'}])


@app.get("/")
def read_root():
    '''
    ROOT.
    '''
    logger.info(f"root API.")

    return {"Hello": "you made it."}


@app.post("/user/signup/", status_code=status.HTTP_201_CREATED, tags=["user singn-up/sign-in"])
async def create_user(db: db_dependency, user: schemas.UserCreate):
    db_user = crud.get_user(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    return crud.create_user(db,user=user)


@app.post("/get_answer_given_question/")
async def get_answer_given_question(item:Item):
    '''
    get_answer_given_question.
    '''
    response = chat_with_gemini(item.text)

    return json.loads(response)


@app.post("/get_content_based_recommendation/")
async def get_content_based_recommendation(item:UserItem):
    '''
    get_content_based_recommendation.
    '''
    user_filter_df = user_transaction_df[user_transaction_df['name']==item.mail]
    user_filter_list = user_filter_df.to_dict('records')
    new_products_list = new_products_df.to_dict('records')
    transaction_based_prompt_new = transaction_based_prompt.format(transaction_records=user_filter_list, new_products_records=new_products_list)
    response = call_gemini_api(transaction_based_prompt_new)

    return json.loads(response)