from typing import Annotated
from sqlalchemy import and_, or_, not_

from . import models, schemas


def get_user(db, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db, user: schemas.UserCreate):
    db_user = models.User(email=user.email,password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_product(db, product_name: str):
    return db.query(models.Product).filter(models.Product.product_name == product_name).first()

def get_product_duplicate(db, product_type: str, product_name: str, product_category: str):
    return db.query(models.Product).filter(and_(models.Product.product_type == product_type, models.Product.product_name == product_name, models.Product.product_category == product_category)).first()

def get_products(db,skip: int=0, limit: int=100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_products_greater_score(db, product_score: float, skip: int=0, limit: int=100):
    return db.query(models.Product).filter(models.Product.product_score > product_score).offset(skip).limit(limit).all()

def create_product(db, product_type: str, product_category: str, product_name: str, product_score: float, extracted_data: str, ingradient_info: str, ingradient_llm_info: str, image_data):
    db_product = models.Product(product_type=product_type,
                            product_category=product_category,
                            product_name=product_name,
                            product_score=product_score,
                            extracted_data=extracted_data,
                            ingradient_info=ingradient_info,
                            ingradient_llm_info=ingradient_llm_info,
                            image=image_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_recommend_product(db, product_type: str, product_name: str):
    return db.query(models.RecommendProduct).filter(and_(models.RecommendProduct.product_type == product_type, models.RecommendProduct.product_name == product_name)).first()

def get_recommend_products(db, product_type: str, limit: int=5):
    return db.query(models.RecommendProduct).filter(models.RecommendProduct.product_type == product_type).limit(limit).all()

def create_recommend_product(db, product_type: str, product_category: str, product_name: str, product_score: float, extracted_data: str, ingradient_info: str, ingradient_llm_info: str, image_data):
    db_rec_product = models.RecommendProduct(product_type=product_type,
                            product_category=product_category,
                            product_name=product_name,
                            product_score=product_score,
                            extracted_data=extracted_data,
                            ingradient_info=ingradient_info,
                            ingradient_llm_info=ingradient_llm_info,
                            image=image_data)
    db.add(db_rec_product)
    db.commit()
    db.refresh(db_rec_product)
    return db_rec_product