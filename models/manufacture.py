from __future__ import annotations

from pydantic import BaseModel, Field

from .base_model import UniversalData
from utils import localizer_cn, localizer_en
from utils.file_manager import get_cache_dir, get_data_dir, sc, extract_image
from utils.converter import convert_dds_to_png
from loguru import logger

cache_dir = get_cache_dir()
data_dir = get_data_dir("manufacture")

class LocationAudioPlayTrigger(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class LocationAudioStopTrigger(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class DisplayFeatures(BaseModel):
    Callout1: str
    Callout2: str
    Callout3: str
    FrontendBackground: str
    History: str
    LogoSimplifiedWhite: str
    UIPriority: int
    __type: str
    locationAudioPlayTrigger: LocationAudioPlayTrigger
    locationAudioStopTrigger: LocationAudioStopTrigger


class Localization(BaseModel):
    Description: str
    Name: str
    ShortName: str
    __type: str
    displayFeatures: DisplayFeatures


class ManufactureRaw(BaseModel):
    BuildingBlocksStyle: str
    Code: str
    DashboardCanvasConfig: str
    Localization: Localization
    Logo: str
    LogoFullColor: str
    LogoSimplifiedWhite: str
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')


    def to_manufacture(self) -> Manufacture:
        """Convert a raw manufacture to a manufacture"""

        if self.Logo != "":
            logo_path = data_dir / f"{self.ref}.logo.png"
            extract_image(self.Logo, logo_path)
        if self.LogoFullColor != "":
            logo_full_color_path = data_dir / f"{self.ref}.logo_full_color.png"
            extract_image(self.LogoFullColor, logo_full_color_path)
        if self.LogoSimplifiedWhite != "":
            logo_simplified_white_path = data_dir / f"{self.ref}.logo_simplified_white.png"
            extract_image(self.LogoSimplifiedWhite, logo_simplified_white_path)

        return Manufacture(
            logo=Manufacture.Logo(
                logo=str(f"{self.ref}.logo.png"),
                logo_full_color=str(f"{self.ref}.logo_full_color.png"),
                logo_simplified_raw=str(f"{self.ref}.logo_simplified_white.png")
            ),
            name=localizer_en.get(self.Localization.Name),
            chinese_name=localizer_cn.get(self.Localization.Name),
            description=localizer_en.get(self.Localization.Description),
            chinese_description=localizer_cn.get(self.Localization.Description),
            short_name=localizer_en.get(self.Localization.ShortName),
            chinese_short_name=localizer_cn.get(self.Localization.ShortName),
            type=self.type,
            path=self.path,
            ref=self.ref
        )


class Manufacture(UniversalData):
    class Logo(BaseModel):
        logo: str
        logo_full_color: str
        logo_simplified_raw: str

    logo: Logo
    short_name: str
    chinese_short_name: str
    path: str
    type: str = "SCItemManufacturer"
