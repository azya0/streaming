from ..base import AllowFromAttribure


class AcessTokenWithType(AllowFromAttribure):
    # Swagger OAuth require lowercase field name
    access_token: str
    token_type: str


class Tokens(AllowFromAttribure):
    ACCESS_TOKEN:   str
    REFRESH_TOKEN:  str
