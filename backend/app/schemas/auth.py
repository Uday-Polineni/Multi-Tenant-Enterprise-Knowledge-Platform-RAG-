from pydantic import BaseModel, EmailStr, Field, model_validator

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    organization_name: str | None = Field(default=None, min_length=1, max_length=255)
    invite_token: str | None = Field(default=None, min_length=1, max_length=64)

    @model_validator(mode="after")
    def validate_register_mode(self) -> "RegisterRequest":
        if self.invite_token:
            if self.organization_name:
                raise ValueError("Provide either invite_token or organization_name, not both")
        elif not self.organization_name:
            raise ValueError("organization_name is required without invite_token")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class InviteRequest(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.EMPLOYEE


class InviteResponse(BaseModel):
    id: str
    email: str
    role: str
    token: str
    expires_at: str
    organization_id: str
