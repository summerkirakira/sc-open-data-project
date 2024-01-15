from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .fps_magazine import FPSMagazine
from .utils import get_item_by_ref


class FPSWeapon(UniversalData):

    class FireMode(BaseModel):
        mode: str
        fireRate: int = 0
        chargeTime: int = 0
        ammoCost: int = 1

    class Port(BaseModel):
        name: str
        type: str
        min_size: int
        max_size: int

    mass: float
    micro_scu: int
    magazine: Optional[FPSMagazine]
    size: int
    magazine: Optional[FPSMagazine]
    fire_modes: List[FireMode]
    ports: list[Port]
    manufacturer: str = ""


class FPSWeaponRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SCItemWeaponComponentParams: SCItemWeaponComponentParamsType
        SItemPortContainerComponentParams: SItemPortContainerComponentParamsType
        SCItemPurchasableParams: Annotated[Optional[SCItemPurchasableParamsType], Field(alias="SCItemPurchasableParams")] = None

    Components: Components

    def to_fps_weapon(self, magazines: list[FPSMagazine]) -> FPSWeapon:
        mass = self.Components.SEntityPhysicsControllerParams.PhysType.Mass
        micro_scu = self.Components.SAttachableComponentParams.AttachDef.inventoryOccupancyVolume.microSCU
        magazine = get_item_by_ref(magazines, self.Components.SCItemWeaponComponentParams.ammoContainerRecord)

        fire_modes = []
        for fire_action in self.Components.SCItemWeaponComponentParams.fireActions:
            if fire_action.SWeaponActionFireSingleParams is not None:
                fire_modes.append(FPSWeapon.FireMode(
                    mode="single",
                    fireRate=fire_action.SWeaponActionFireSingleParams.fireRate,
                    ammoCost=fire_action.SWeaponActionFireSingleParams.launchParams.ammoCost
                ))
            elif fire_action.SWeaponActionFireBurstParams is not None:
                fire_modes.append(FPSWeapon.FireMode(
                    mode="burst",
                    fireRate=fire_action.SWeaponActionFireBurstParams.fireRate,
                    ammoCost=fire_action.SWeaponActionFireBurstParams.launchParams.ammoCost
                ))
            elif fire_action.SWeaponActionFireRapidParams is not None:
                fire_modes.append(FPSWeapon.FireMode(
                    mode="rapid",
                    fireRate=fire_action.SWeaponActionFireRapidParams.fireRate,
                    ammoCost=fire_action.SWeaponActionFireRapidParams.launchParams.ammoCost
                ))
            elif fire_action.SWeaponActionFireChargedParams is not None:
                fire_modes.append(FPSWeapon.FireMode(
                    mode="charge",
                    cooldownTime=fire_action.SWeaponActionFireChargedParams.chargeTime
                ))

        ports = []

        for port in self.Components.SItemPortContainerComponentParams.Ports:
            if port.SItemPortDef.Name == "item_grab":
                continue
            ports.append(FPSWeapon.Port(
                name=port.SItemPortDef.Name,
                type=port.SItemPortDef.Name,
                min_size=port.SItemPortDef.MinSize,
                max_size=port.SItemPortDef.MaxSize
            ))

        return FPSWeapon(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            ports=ports,
            mass=mass,
            micro_scu=micro_scu,
            magazine=magazine,
            size=self.Components.SAttachableComponentParams.AttachDef.Size,
            fire_modes=fire_modes,
            manufacturer=self.Components.SAttachableComponentParams.AttachDef.Manufacturer,
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description)
        )




