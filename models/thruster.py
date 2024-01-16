from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import SHealthComponentParamsType, SDistortionParamsType, HealthInfo, EntityComponentPowerConnection, EntityComponentHeatConnection
from .base_model import SCItemThrusterParamsType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .utils import get_item_by_ref
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class Thruster(UniversalData):

        data: SCItemThrusterParamsType
        health_info: HealthInfo
        power: EntityComponentPowerConnection
        heat: EntityComponentHeatConnection
        manufacturer: str = ""
        shop_info: list[ShopInfo]
        size: int


class ThrusterRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SCItemThrusterParams: SCItemThrusterParamsType
        SHealthComponentParams: SHealthComponentParamsType
        EntityComponentHeatConnection: EntityComponentHeatConnection
        EntityComponentPowerConnection: EntityComponentPowerConnection


    Components: Components


    def to_thruster(self) -> Thruster:
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size
        grade = self.Components.SAttachableComponentParams.AttachDef.Grade
        power = self.Components.EntityComponentPowerConnection
        heat = self.Components.EntityComponentHeatConnection

        return Thruster(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            data=self.Components.SCItemThrusterParams,
            manufacturer=manufacturer,
            size=size,
            grade=grade,
            health_info=HealthInfo.from_params(self.Components.SHealthComponentParams),
            power=power,
            heat=heat,

            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            shop_info=get_shop_info_by_ref(self.ref)
        )