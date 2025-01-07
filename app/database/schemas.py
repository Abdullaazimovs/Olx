from typing import Optional

from pydantic import BaseModel, EmailStr, validator, Field

from utils import hashing


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str = Field("default_username", description="The user's username")
    email: EmailStr = Field("default@example.com", description="The user's email address")

    class Config:
        str_min_length = 1
        str_strip_whitespace = True


# Model for user creation, extends UserBase and adds validation
class UserCreate(UserBase):
    password: str = Field("default_password123", description="The user's password")
    first_name: str = Field("John", description="The user's first name")
    last_name: str = Field("Doe", description="The user's last name")
    phone_number: str = Field("123-456-7890", description="The user's phone number")

    # Combined password validation and hashing in one validator
    @validator('password')
    def password_strength_and_hash(cls, value):
        # Password strength check
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one number')

        # Hash the password
        return hashing.hash_password(value)

    # Validator for phone number format (if provided)
    @validator('phone_number')
    def phone_number_format(cls, value):
        if value and len(value) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return value


# Model for user response, excludes sensitive information like password
class UserResponse(UserBase):
    id: int
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True  # Automatically maps attributes for ORM compatibility
