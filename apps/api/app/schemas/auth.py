from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TrocarSenhaRequest(BaseModel):
    senha_atual: str
    senha_nova: str = Field(min_length=8)
