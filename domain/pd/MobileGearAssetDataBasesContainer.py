from pydantic import BaseModel
from typing import List

from domain.pd.MobileGearAssetDatabase import MobileGearAssetDatabase



class MobileGearAssetDataBasesContainer(BaseModel):
    mobileGearAssetDataBases: List[MobileGearAssetDatabase]