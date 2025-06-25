from datetime import datetime
from pydantic import BaseModel, StringConstraints
from typing import Annotated

Bookstr = Annotated[str, StringConstraints(min_length=1)]

class Recommendation(BaseModel):
    title: str
    explanation: str

class BookSchema(BaseModel):
    id: int
    title: str
    timestamp: datetime
    user_id: int

    model_config = {
            "from_attributes": True
        }

class BookCreateSchema(BaseModel):
    title: Bookstr
    user_id: int
