from datetime import datetime
import sqlalchemy
import base64
from sqlalchemy import Column, Boolean, Integer, Float, Text, String, DateTime, ForeignKey, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from .db import Base, engine


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer,primary_key=True,index=True)
    created_at = Column(DateTime,default=datetime.now)
    product_type = Column(String,nullable=False,unique=False,index=True)
    product_category = Column(String,nullable=False,unique=False,index=True)
    product_name = Column(String,nullable=False,unique=False,index=True)
    product_score = Column(Float,nullable=True)
    extracted_data = Column(Text,nullable=True)
    ingradient_info = Column(Text,nullable=False)
    ingradient_llm_info = Column(Text,nullable=True)
    image = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)

class RecommendProduct(Base):
    __tablename__ = "recommendproduct"

    id = Column(Integer,primary_key=True,index=True)
    created_at = Column(DateTime,default=datetime.now)
    product_type = Column(String,nullable=False,unique=False,index=True)
    product_category = Column(String,nullable=False,unique=False,index=True)
    product_name = Column(String,nullable=False,unique=False,index=True)
    product_score = Column(Float,nullable=True)
    extracted_data = Column(Text,nullable=True)
    ingradient_info = Column(Text,nullable=True)
    ingradient_llm_info = Column(Text,nullable=True)
    image = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    created_at = Column(DateTime,default=datetime.now)
    email = Column(String,nullable=False,unique=False,index=True)
    password = Column(String,nullable=False)


Base.metadata.create_all(bind=engine)
