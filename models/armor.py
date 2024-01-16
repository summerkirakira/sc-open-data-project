from .base_model import UniversalData, SAttachableComponentParams, SCItemVehicleArmorParamsType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .utils import get_item_by_ref


class Armor(UniversalData):
    data: SCItemVehicleArmorParamsType
    manufacturer: str = ""
    size: int


class ArmorRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SCItemVehicleArmorParams: SCItemVehicleArmorParamsType

    Components: Components

    def to_armor(self) -> Armor:
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size
        grade = self.Components.SAttachableComponentParams.AttachDef.Grade

        return Armor(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            data=self.Components.SCItemVehicleArmorParams,
            manufacturer=manufacturer,
            size=size,
            grade=grade,

            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
        )