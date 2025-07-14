from pydantic import BaseModel

class MobileGearAssetDatabase(BaseModel):
    version: int
    path: str