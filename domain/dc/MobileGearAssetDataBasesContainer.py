from dataclasses import dataclass
from typing import List

from domain.dc import MobileGearAssetDatabase


@dataclass
class MobileGearAssetDataBasesContainerDataClass:
    mobileGearAssetDataBases: List[MobileGearAssetDatabase]