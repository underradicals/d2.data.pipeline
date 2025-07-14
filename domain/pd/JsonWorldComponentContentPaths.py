from pydantic import BaseModel, Field

from domain.pd.DestinyDefinitions import DestinyDefinitions


class JsonWorldComponentsContentPaths(BaseModel):
    en: DestinyDefinitions
    fr: DestinyDefinitions
    es: DestinyDefinitions
    es_mx: DestinyDefinitions = Field(alias="es-mx")
    de: DestinyDefinitions
    it: DestinyDefinitions
    ja: DestinyDefinitions
    pt_br: DestinyDefinitions = Field(alias="pt-br")
    ru: DestinyDefinitions
    pl: DestinyDefinitions
    ko: DestinyDefinitions
    zh_cht: DestinyDefinitions = Field(alias="zh-cht")
    zh_chs: DestinyDefinitions = Field(alias="zh-chs")