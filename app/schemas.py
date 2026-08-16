from pydantic import BaseModel, EmailStr, Field


class RequestCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    customer_email: EmailStr
    input_text: str = Field(..., min_length=10)