from typing import List
from pydantic import BaseModel

from domain.pd.JsonWorldContentPaths import JsonWorldContentPaths
from domain.pd.JsonWorldComponentContentPaths import JsonWorldComponentsContentPaths
from domain.pd.MobileGearAssetDatabase import MobileGearAssetDatabase
from domain.pd.MobileWorldContentPaths import MobileWorldContentPaths
from domain.pd.MobileGearCDN import MobileGearCDN


class Response(BaseModel):
    version: str
    mobileAssetContentPath: str
    mobileGearAssetDataBases: List[MobileGearAssetDatabase]
    mobileWorldContentPaths: MobileWorldContentPaths
    jsonWorldContentPaths: JsonWorldContentPaths
    jsonWorldComponentContentPaths: JsonWorldComponentsContentPaths
    mobileClanBannerDatabasePath: str
    mobileGearCDN: MobileGearCDN
    iconImagePyramidInfo: List