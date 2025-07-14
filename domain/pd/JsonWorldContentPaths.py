from pydantic import BaseModel, Field

class JsonWorldContentPaths(BaseModel):
    en: str
    fr: str
    es: str
    es_mx: str = Field(alias="es-mx")
    de: str
    it: str
    ja: str
    pt_br: str = Field(alias="pt-br")
    ru: str
    pl: str
    ko: str
    zh_cht: str = Field(alias="zh-cht")
    zh_chs: str = Field(alias="zh-chs")