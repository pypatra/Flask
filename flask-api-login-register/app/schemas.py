from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True
