from pydantic import BaseModel
from typing import Dict

from domain.pd.Response import Response


class Manifest(BaseModel):
    Response: Response
    ErrorCode: int
    ThrottleSeconds: int
    ErrorStatus: str
    Message: str
    MessageData: Dict