from dataclasses import dataclass
from typing import Dict

from domain.dc.Response import ResponseDataClass


@dataclass
class ManifestDataClass:
    Response: ResponseDataClass
    ErrorCode: int
    ThrottleSeconds: int
    ErrorStatus: str
    Message: str
    MessageData: Dict