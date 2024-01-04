from pydantic import BaseModel


class ProductBase(BaseModel):
    product_type: str
    product_category: str
    product_name: str
    product_score: str
    ingradient_info: str
    ingradient_llm_info: str

    class Config:
        orm_model = True


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

    class Config:
        orm_model = True