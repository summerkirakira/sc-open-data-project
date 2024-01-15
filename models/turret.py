from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import SHealthComponentParamsType, SDistortionParamsType, SCItemSeatParamsType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en


class Turret(UniversalData):

    class Port(BaseModel):
        name: str
        type: str
        min_size: int
        max_size: int

    mass: float
    micro_scu: int
    size: int
    ports: list[Port]
    is_personnel: bool = False
    manufacturer: str = ""


class TurretRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SItemPortContainerComponentParams: SItemPortContainerComponentParamsType
        SHealthComponentParams: SHealthComponentParamsType
        SDistortionParams: Optional[SDistortionParamsType] = None
        SCItemSeatParams: Optional[SCItemSeatParamsType] = None

    Components: Components

    def to_turret(self) -> Turret:

        ports = []

        for port in self.Components.SItemPortContainerComponentParams.Ports:
            ports.append(Turret.Port(
                name=port.SItemPortDef.Name,
                type=port.SItemPortDef.Name,
                min_size=port.SItemPortDef.MinSize,
                max_size=port.SItemPortDef.MaxSize
            ))

        is_personnel = self.Components.SCItemSeatParams is not None

        return Turret(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            mass=self.Components.SEntityPhysicsControllerParams.PhysType.Mass,

            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),

            manufacturer=self.Components.SAttachableComponentParams.AttachDef.Manufacturer,
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),

            micro_scu=self.Components.SAttachableComponentParams.AttachDef.inventoryOccupancyVolume.microSCU,
            size=self.Components.SAttachableComponentParams.AttachDef.Size,
            ports=ports,
            is_personnel=is_personnel
        )

