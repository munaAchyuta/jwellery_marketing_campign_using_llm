from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class DocItem(BaseModel):
    input_text: str
    other: Optional[str] = ""

class QuestionAnswerItem(BaseModel):
    question: Optional[str] = None
    context: str

class ProcessDocItem(BaseModel):
    file_path: List[str] = None