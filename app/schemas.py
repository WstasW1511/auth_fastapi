from pydantic import Field, BaseModel


class UserRegistration(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    name: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=3, max_length=20)


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str

    model_config = {
        'from_attributes': True
    }


class UserLogin(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=3, max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class GetUsers(UserResponse):
    inline: bool

