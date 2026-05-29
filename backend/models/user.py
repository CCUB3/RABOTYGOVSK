from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True)

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: int | None = Field(default=None, primary_key=True)
    display_name: str

class UserRegister(UserBase):
    display_name: str | None = Field(default=None)
    password: str

class UserDB(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    display_name: str | None = Field(default=None)
    hashed_password: str
