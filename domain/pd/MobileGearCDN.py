from pydantic import BaseModel

class MobileGearCDN(BaseModel):
    Geometry: str
    Texture: str
    PlateRegion: str
    Gear: str
    Shader: str
