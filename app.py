import numpy as np
import pandas as pd
import requests
import json
#import plotly.express as px
#from st_aggrid import AgGrid
import streamlit as st
#from streamviz import gauge
import base64
from io import BytesIO
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide")

api_endpoint = "http://127.0.0.1:8002/get_answer_given_question/"
api_endpoint_content_recommend = "http://127.0.0.1:8002/get_content_based_recommendation/"

# Load the product data
products_df = pd.read_csv("sample_data/tanishq_product_structured_data.csv")
products_df.fillna('No Information', inplace=True)

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

# Create a TfidfVectorizer object and fit it to the product descriptions
vectorizer = TfidfVectorizer(stop_words="english")
vectorizer.fit(products_df["Product Details"])


def call_rest_api(data={}, api_endpoint=""):
    '''
    # Function to call the REST API
    '''
    headers = {'accept': 'application/json'}
    response = requests.post(api_endpoint, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

# Define a function to generate product recommendations
def generate_recommendations(query, other_filter):
    # Convert the query to a vector
    query_vector = vectorizer.transform([query])

    # Compute cosine similarities between the query vector and the product vectors
    cosine_similarities = cosine_similarity(query_vector, vectorizer.transform(products_df["Product Details"]))

    # Sort the products by cosine similarity
    sorted_products = products_df.iloc[cosine_similarities.argsort()[0, ::-1]]

    # sort the product with other meta data
    print('other filter: ',other_filter)
    tmp = {'gender':'Gender','product_category':'file_name'}
    new_df_list = []
    target_strings = dict()
    for key in tmp:
        if other_filter.get(key,None):
            #df[df[column].str.contains(partial_string, case=False, na=False)]
            #print(sorted_products.loc[sorted_products[tmp.get(key)].str.contains(other_filter.get(key), case=False, na=False)])
            #print("******")
            #new_df_list.append(sorted_products.loc[sorted_products[tmp.get(key)].str.contains(other_filter.get(key), case=False, na=False)])

            # Strings to check for in each column
            target_strings[tmp.get(key)] = other_filter.get(key)

    if len(target_strings) != 0:
        print(target_strings)
        # Check if all specified columns contain the target strings
        #mask = sorted_products.apply(lambda row: all(row[col].astype(str).contains(target, case=False) for col, target in target_strings.items()), axis=1)
        mask = sorted_products.apply(lambda row: all(row[col].lower().find(target.lower()) != -1 for col, target in target_strings.items()), axis=1)

        # Filter the DataFrame based on the mask
        final_df = sorted_products[mask]
        if target_strings.get('Gender',None):
            #final_df = final_df.loc[final_df['Gender'].lower()==target_strings.get('Gender').lower()]
            mask = final_df['Gender'].str.lower() == target_strings.get('Gender').lower()
            final_df = final_df[mask]
        if len(final_df) == 0:
            mask = sorted_products.apply(lambda row: all(row[col].lower().find(target.lower()) != -1 for col, target in target_strings.items()), axis=1)

            # Filter the DataFrame based on the mask
            final_df = sorted_products[mask]
    else:
        final_df = pd.DataFrame()
    print("filter df: ",final_df.shape)
    if len(final_df) == 0:
        new_df_list.append(sorted_products)
        final_df = pd.concat(new_df_list, ignore_index=True)
        final_df.drop_duplicates(inplace=True)


    # Return the top 10 products
    return final_df.head(10)#sorted_products.head(10)

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
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

# Create a Streamlit app
_ = set_bg_hack('light-bkg.jpg')

st.title("Jwellery Shopping Buddy")

# Add a text input field for the user to enter their mail-id
#user_mailid = st.text_input("Please Enter your mail-id:")
user_mailid = "ramesh@gmail.com"#st.selectbox("Please select a mail-id:", ["neha@gmail.com", "ramesh@gmail.com"])

# Add a text input field for the user to enter their query
query = st.text_input("Enter your query:")


# Generate product recommendations
if query:
    # chat_with_gemini
    chat_response = call_rest_api(data={"text":query}, api_endpoint=api_endpoint)
    st.write(chat_response.get('message','Sure.'))

    if chat_response.get('start_recommend',None):
        recommendations = generate_recommendations(query, chat_response.get('product_metadata_match',{}))
        product_category = chat_response.get('product_category','misc')

        # Create a row for each recommended product
        for product in recommendations.iterrows():
            with st.container():
                # Create a column for the product image
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(Image.open(r"{}".format(product[1]["image_url"])), width=200)

                # Create a column for the product information
                with col2:
                    st.write(f"**Product Name:** {product[1]['file_name']}")
                    st.write(f"**Product Description:** {product[1]['Product Details']}")
                    st.write(f"**Product Price:** {product[1]['Price']}")
                    st.button("View Details", key=product[1]['file_name'], on_click=lambda: st.experimental_set_query_params(product_link=product[1]["image_url"],product_name=product[1]["file_name"],product_category=product_category))
    
        def show_complementary_product_details(product):
            print(product)
            st.title(f"Complementary/Supplementary Details")
            st.write(f"**Product Name:** {product['product_name'][0]}")
            st.image(Image.open(r"{}".format(product["product_link"][0])), width=200)
            if product['product_category'][0]=='chain':
                for index,row in complementary_products_df[complementary_products_df['product_category']=='ring'].iterrows():
                    st.write(f"**Complementary Product :** {row['name']}")
                    st.image(Image.open(r"{}".format(row["image_url"])), width=200)
                    #st.write(f"**Supplementary Products:** {'supplementary-abc'}")
            elif product['product_category'][0]=='ring':
                for index,row in complementary_products_df[complementary_products_df['product_category']=='chain'].iterrows():
                    st.write(f"**Complementary Product :** {row['name']}")
                    st.image(Image.open(r"{}".format(row["image_url"])), width=200)
                    #st.write(f"**Supplementary Products:** {'supplementary-abc'}")
            else:
                for index,row in complementary_products_df[complementary_products_df['product_category'].isin(['chain','ring'])].iterrows():
                    st.write(f"**Complementary Product :** {row['name']}")
                    st.image(Image.open(r"{}".format(row["image_url"])), width=200)
                # Include additional details and complementary/supplementary product information
                # ...
        
        # Check if the details page is requested
        #with col2:
        print('st.experimental_get_query_params(): ',st.experimental_get_query_params())
        product_param = st.experimental_get_query_params().get("product_name", None)
        if product_param:
            show_complementary_product_details(st.experimental_get_query_params())
        
        # recommend based on user transations
        print("user_mailid: ",user_mailid)
        if user_mailid:
            prod_list_tobe_recommended = call_rest_api(data={"mail":user_mailid}, api_endpoint=api_endpoint_content_recommend)
            prod_tobe_recmd_df = new_products_df[new_products_df['product_id'].isin(prod_list_tobe_recommended)]
            st.title(f"**Based on transaction history, Below Products you may like :**")
            st.write(f"**User mail:** {user_mailid}")
            for index, row in prod_tobe_recmd_df.iterrows():
                st.write(f"**Product Name:** {row['name']}")
                st.write(f"**Product Description:** {row['description']}")
                st.write(f"**Product Price:** {row['price']}")
                st.image(Image.open(r"{}".format(row["image_url"])), width=200)


#i want to buy birthday gift for my daughter. something like gold chain