from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


class UserSchema(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
