from pydantic import BaseModel


class TokenData(BaseModel):
    token: str
    type: str = 'Bearer'


class UserSchema(BaseModel):
    email: str
