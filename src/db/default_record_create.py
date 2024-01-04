from src.db.db import SessionLocal
from . import crud

def create_default_recommend_product():
    data = [{'product_type':'toothpaste','product_name':'Ayur toothpaste','ingradient_info':'Not Available'},
            {'product_type':'soap','product_name':'Ayur soap','ingradient_info':'Not Available'},
            {'product_type':'shampoo','product_name':'Ayur herbal','ingradient_info':'Not Available'}]
    
    for each_record in data:
        if not crud.get_recommend_product(SessionLocal(), each_record['product_type'],each_record['product_name']):
            _ = crud.create_recommend_product(SessionLocal(), each_record['product_type'],each_record['product_name'],each_record['ingradient_info'])