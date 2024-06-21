from pydantic import BaseModel, ConfigDict, EmailStr


class BaseUserChema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseUserChema):
    username: str
    email: EmailStr
    password: str


class UserGet(BaseUserChema):
    username: str
    email: EmailStr
    is_active: bool
    id: int


class UserGetWithPassword(UserGet):
    hashed_password: bytes


class UserUpdate(BaseUserChema):
    username: str | None
    email: EmailStr | None
    password: str | None
    # is_active: bool | None
    # is_admin: bool | None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
