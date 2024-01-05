import numpy as np
import pandas as pd
import requests
import json
import yaml
import streamlit as st
import base64
from io import BytesIO
from PIL import Image

from app_util import read_config, call_rest_api

config_file_path = "./streamlit_config.yaml"
GLOBAL = read_config(config_file_path)

api_endpoint_chat_conversation = GLOBAL.get('api_endpoint_chat_conversation')
api_endpoint_content_recommend = GLOBAL.get('api_endpoint_content_recommend')
api_complementary_products = GLOBAL.get("api_complementary_products")
api_recommendations_based_preference = GLOBAL.get('api_recommendations_based_preference')



def set_bg_hack(main_bg):
    # set bg name
    main_bg_ext = "png"
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def show_complementary_product_details(product):
    st.title(f"Complementary/Supplementary Details")
    st.write(f"**Product Name:** {product['product_name'][0]}")
    st.image(Image.open(r"{}".format(product["product_link"][0])), width=200)
    comp_prod_category = list()
    if product['product_category'][0]=='chain':
        comp_prod_category.append('chain')
    elif product['product_category'][0]=='ring':
        comp_prod_category.append('ring')
    else:
        comp_prod_category.extend(['chain','ring'])
    prod_tobe_recmd = call_rest_api(data={"product_category":comp_prod_category}, api_endpoint=api_complementary_products)
    for row in prod_tobe_recmd:
        st.write(f"**Complementary Product :** {row['name']}")
        st.image(Image.open(r"{}".format(row["image_url"])), width=200)


# Create a Streamlit app
st.set_page_config(layout="wide")
_ = set_bg_hack('light-bkg.jpg')

st.title("Jwellery Shopping Assistant for Cross/Up Selling of Product.")

# Add a text input field for the user to enter their mail-id
user_mailid = "ramesh@gmail.com" # testing with dummy data

# Add a text input field for the user to enter their query
query = st.text_input("Enter your query :smiley:")


# Chat Conversation
if query:
    chat_response = call_rest_api(data={"text":query}, api_endpoint=api_endpoint_chat_conversation)
    st.write(f":rabbit: 661: {chat_response.get('message','Sure.')}")

    # Generate recommendations
    if chat_response.get('start_recommend',None):
        # preference based recommendations
        recommendations = call_rest_api(data=chat_response.get('product_metadata_match',{}), api_endpoint=api_recommendations_based_preference)
        product_category = chat_response.get('product_category','misc')
        st.header("*preference based recommendations.*")
        for product in recommendations:
            with st.container():
                # Create a column for the product image
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(Image.open(r"{}".format(product["image_url"])), width=200)

                # Create a column for the product information
                with col2:
                    st.write(f"**Product Name:** {product['file_name']}")
                    st.write(f"**Product Description:** {product['Product Details']}")
                    st.write(f"**Product Price:** {product['Price']}")
                    st.button("View Details", key=product['file_name'], on_click=lambda: st.experimental_set_query_params(product_link=product["image_url"],product_name=product["file_name"],product_category=product_category))
        
        # Complementary recommendations
        product_param = st.experimental_get_query_params().get("product_name", None)
        if product_param:
            show_complementary_product_details(st.experimental_get_query_params())
        
        # Content-based recommendations
        if user_mailid:
            prod_tobe_recmd = call_rest_api(data={"mail":user_mailid}, api_endpoint=api_endpoint_content_recommend)
            st.title(f"**Based on transaction history, Below Products you may like :**")
            st.write(f"**User mail:** {user_mailid}")
            for row in prod_tobe_recmd:
                st.write(f"**Product Name:** {row['name']}")
                st.write(f"**Product Description:** {row['description']}")
                st.write(f"**Product Price:** {row['price']}")
                st.image(Image.open(r"{}".format(row["image_url"])), width=200)


#i want to buy birthday gift for my daughter. something like gold chain