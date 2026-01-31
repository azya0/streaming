from ..base import User as UserBase
from ..base import Id, AllowFromAttribure


class User(Id, UserBase, AllowFromAttribure):
    is_active:      bool
    is_admin:       bool

