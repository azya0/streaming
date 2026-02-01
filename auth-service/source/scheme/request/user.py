from ..base import User as UserBase


class UserAuth(UserBase):
    password: str


class User(UserAuth):
    pass
