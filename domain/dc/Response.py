from dataclasses import dataclass
from typing import List

from domain.dc.JsonWorldContentPaths import JsonWorldContentPathsDataClass
from domain.dc.JsonWorldComponentContentPaths import JsonWorldComponentsContentPathsDataClass
from domain.dc.MobileGearAssetDatabase import MobileGearAssetDatabaseDataClass
from domain.dc.MobileWorldContentPaths import MobileWorldContentPathsDataClass
from domain.dc.MobileGearCDN import MobileGearCDNDataClass


@dataclass
class ResponseDataClass:
    version: str
    mobileAssetContentPath: str
    mobileGearAssetDataBases: List[MobileGearAssetDatabaseDataClass]
    mobileWorldContentPaths: MobileWorldContentPathsDataClass
    jsonWorldContentPaths: JsonWorldContentPathsDataClass
    jsonWorldComponentContentPaths: JsonWorldComponentsContentPathsDataClass
    mobileClanBannerDatabasePath: str
    mobileGearCDN: MobileGearCDNDataClass
    iconImagePyramidInfo: List