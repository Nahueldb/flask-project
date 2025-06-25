from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

UsernameStr = Annotated[str, StringConstraints(min_length=1)]

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    username: str

    model_config = {
            "from_attributes": True
        }

class UserCreateSchema(BaseModel):
    email: EmailStr
    username: UsernameStr


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    username: UsernameStr | None = None

