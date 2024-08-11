from pydantic import BaseModel, EmailStr


class UserRegistrationSchema(BaseModel):
    email_address: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email_address: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    email_address: EmailStr
    is_admin: bool


class UserPreferenceSchema(BaseModel):
    preferred_location: str
    min_rooms: int
    max_rent: int
