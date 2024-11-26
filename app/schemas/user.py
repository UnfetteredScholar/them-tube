from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from schemas.base import PyObjectId


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class SignInType(str, Enum):
    GOOGLE_SIGN_IN = "GOOGLE_SIGN_IN"
    NORMAL = "NORMAL"
    FACEBOOK_SIGN_IN = "FACEBOOK_SIGN_IN"


class UserStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    id: PyObjectId = Field(validation_alias="_id")
    username: str
    email: str
    password: str
    role: Role
    status: UserStatus = UserStatus.ENABLED
    sign_in_type: SignInType = "NORMAL"
    verified: bool
    date_created: datetime
    date_modified: datetime


class UserOut(BaseModel):
    id: PyObjectId
    username: str
    email: str
    role: Role
    status: UserStatus = UserStatus.ENABLED
    sign_in_type: SignInType = "NORMAL"
    verified: bool
    date_created: datetime
    date_modified: datetime
