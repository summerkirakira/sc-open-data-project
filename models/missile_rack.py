from .base_model import UniversalData, SAttachableComponentParams, EntityComponentPowerConnection, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import SHealthComponentParamsType, SDistortionParamsType, SCItemMissileRackParamsType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class MissileRack(UniversalData):

    class Port(BaseModel):
        name: str
        type: str
        min_size: int
        max_size: int

    size: int
    ports: list[Port]
    manufacturer: str = ""
    shop_info: list[ShopInfo]
    power: EntityComponentPowerConnection
    loadout: list[str] = []


class MissileRackRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SItemPortContainerComponentParams: SItemPortContainerComponentParamsType
        EntityComponentPowerConnection: EntityComponentPowerConnection


    Components: Components


    def to_missile_rack(self) -> MissileRack:

            ports = []

            for port in self.Components.SItemPortContainerComponentParams.Ports:
                ports.append(MissileRack.Port(
                    name=port.SItemPortDef.Name,
                    type=port.SItemPortDef.Name,
                    min_size=port.SItemPortDef.MinSize,
                    max_size=port.SItemPortDef.MaxSize
                ))

            return MissileRack(
                ref=self.ref,
                path=self.path,
                type=self.Components.SAttachableComponentParams.AttachDef.Type,
                size=self.Components.SAttachableComponentParams.AttachDef.Size,
                ports=ports,
                manufacturer=self.Components.SAttachableComponentParams.AttachDef.Manufacturer,
                power=self.Components.EntityComponentPowerConnection,

                name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                description=localizer_en.get(
                    self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
                chinese_description=localizer_cn.get(
                    self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
                shop_info=get_shop_info_by_ref(self.ref)
            )