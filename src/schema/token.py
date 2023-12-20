from pydantic import BaseModel


class JWT(BaseModel):
    type: str
    token: str