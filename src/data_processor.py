import os
import glob
import re
import json
import pandas as pd


def extract_structured_data(text):
    # Extracting Product Details
    product_details_match = re.search(r"Product Details:(.*?)(?:Price:|\n\n)", text, re.DOTALL)
    product_details = product_details_match.group(1).strip() if product_details_match else ""

    # Extracting Price
    price_match = re.search(r"Price: (.+)", text)
    price = price_match.group(1).strip() if price_match else ""

    # Extracting Specifications
    specifications_match = re.search(r"Specifications:(.*?)(?:Product Details:|\Z)", text, re.DOTALL)
    specifications = specifications_match.group(1).strip() if specifications_match else ""

    # Combine the extracted information into a structured JSON
    json_data = {
        "Product Details": product_details,
        "Price": price,
    }

    # Extract additional key-value pairs from Specifications
    specifications_lines = specifications.split("\n")
    for line in specifications_lines:
        if ":" in line:
            key, value = map(str.strip, line.split(":", 1))
            json_data[key] = value

    # Print the resulting JSON data
    #print(json.dumps(json_data, indent=2))
    return json_data


def file_processor_old(file_path):
    with open(file_path,'r') as f:
        data = f.read()
    image_url = '.'.join(file_path.split('.')[:-1]) + '.PNG'
    return {'file_name':file_path,'image_url':image_url,'data':data}


def file_processor(folder):
    # Create an empty list to store the dictionaries
    list_of_dict = []

    # Loop through all the .txt files in the folder
    for txt_file in glob.glob(os.path.join(folder, "*.txt")):
        # Get the file name without extension
        file_name = os.path.splitext(os.path.basename(txt_file))[0]
        # Get the corresponding image file name by replacing .txt with .PNG
        image_file = txt_file.replace(".txt", ".PNG")
        # Check if the image file exists
        if os.path.exists(image_file):
            # Read the data from the text file
            with open(txt_file, "r") as f:
                data = f.read()
            
            # get structured data
            structured_data = extract_structured_data(data)
            # Create a dictionary with the file name, image url and data
            dict = {"file_name": file_name, "image_url": image_file,'data':data, "structured_data": structured_data}
            # Append the dictionary to the list
            list_of_dict.append(dict)

    # Print the list of dictionaries
    return list_of_dict

def read_json_data(file_name):
    with open(file_name) as data_file:
        data_loaded = json.load(data_file)
    
    structured_data_keys = set()
    for rec in data_loaded:
        structured_data_keys.update(rec['structured_data'].keys())
    structured_data_keys.update(['file_name','image_url'])

    structured_data = list()
    for rec in data_loaded:
        structured_data_keys_dict = {i:None for i in structured_data_keys}
        for j in structured_data_keys:
            if rec.get(j,None):
                structured_data_keys_dict[j] = rec.get(j)
            elif rec.get('structured_data',None).get(j,None):
                structured_data_keys_dict[j] = rec.get('structured_data',None).get(j)
        
        structured_data.append(structured_data_keys_dict)

    
    return structured_data_keys, structured_data

def get_df(column_names, struct_data):
    # Column names
    #column_names = ["Name", "Age", "City"]
    column_names = list(column_names)

    # Create an empty DataFrame with column names
    df = pd.DataFrame(columns=column_names)

    # Function to add a row using a dictionary
    def add_row(df, data):
        #df_row = pd.DataFrame([data], columns=column_names)
        #df_global = df.append(df_row, ignore_index=True)
        #global df
        df = df._append(data, ignore_index=True)
        return df

    # Example usage
    #df = add_row({"Name": "John", "Age": 25, "City": "New York"})
    #df = add_row({"Name": "Alice", "Age": 30, "City": "Los Angeles"})
    for rec in struct_data:
        print(rec)
        df = add_row(df, rec)

    # Print the DataFrame
    print(df.head())

    return df



if __name__=="__main__":
    #'''
    data = file_processor("sample_data")
    #print(data)
    with open('sample_data/tanishq_product_strucutred_data.json','w') as f:
        json.dump(data,f)
    #'''
    columns, struct_data = read_json_data('sample_data/tanishq_product_strucutred_data.json')
    #print(columns)
    #print("-----")
    #print(struct_data)
    #df = pd.DataFrame(columns=columns)
    df_struct = get_df(columns, struct_data)
    df_struct.to_csv('sample_data/tanishq_product_structured_data.csv')

