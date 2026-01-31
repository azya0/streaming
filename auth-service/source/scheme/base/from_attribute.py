from pydantic import BaseModel, ConfigDict


class AllowFromAttribure(BaseModel):
    model_config = ConfigDict(from_attributes=True)
