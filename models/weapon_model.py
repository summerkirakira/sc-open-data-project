from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import EntityComponentPowerConnection, SHealthComponentParamsType, HealthInfo, SDistortionParamsType, DistortionInfo, EntityComponentHeatConnection, HeatInfo
from .base_model import SAmmoContainerComponentParamsType
from .fps_weapon import FPSWeapon


from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .vehicle_ammo import VehicleAmmo
from utils.shop_info import ShopInfo, get_shop_info_by_ref
from .utils import get_item_by_ref


class VehicleWeapon(FPSWeapon):

    health_info: Optional[HealthInfo]
    ammo: Optional[VehicleAmmo]
    shop_info: list[ShopInfo]
    heat: HeatInfo
    distortion: Optional[DistortionInfo]
    magazine: int = 0


class VehicleWeaponRaw(BaseModel):
    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SCItemWeaponComponentParams: SCItemWeaponComponentParamsType
        SItemPortContainerComponentParams: SItemPortContainerComponentParamsType
        SAmmoContainerComponentParams: Optional[SAmmoContainerComponentParamsType] = None
        SCItemPurchasableParams: Annotated[Optional[SCItemPurchasableParamsType], Field(alias="SCItemPurchasableParams")] = None
        EntityComponentPowerConnection: EntityComponentPowerConnection
        SHealthComponentParams: SHealthComponentParamsType
        SDistortionParams: Optional[SDistortionParamsType] = None
        EntityComponentHeatConnection: EntityComponentHeatConnection

    Components: Components
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    def to_vehicle_weapon(self, ammos: list[VehicleAmmo]) -> VehicleWeapon:
        ammo = None
        if self.Components.SAmmoContainerComponentParams:
            ammo_ref = self.Components.SAmmoContainerComponentParams.ammoParamsRecord
            ammo = get_item_by_ref(ammos, ammo_ref)
        shop_info = get_shop_info_by_ref(self.ref)

        mass = self.Components.SEntityPhysicsControllerParams.PhysType.Mass
        micro_scu = self.Components.SAttachableComponentParams.AttachDef.inventoryOccupancyVolume.microSCU

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
            elif fire_action.SWeaponActionSequenceParams is not None:
                fire_modes.append(FPSWeapon.FireMode(
                    mode="sequence",
                    fireRate=fire_action.SWeaponActionSequenceParams.sequenceEntries[0].SWeaponSequenceEntryParams.weaponAction.fireRate,
                    ammoCost=fire_action.SWeaponActionSequenceParams.sequenceEntries[0].SWeaponSequenceEntryParams.weaponAction.launchParams.ammoCost
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

            return VehicleWeapon(
                ref=self.ref,
                path=self.path,
                type=self.Components.SAttachableComponentParams.AttachDef.Type,
                name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                ports=ports,
                mass=mass,
                micro_scu=micro_scu,
                ammo=ammo,
                shop_info=shop_info,
                size=self.Components.SAttachableComponentParams.AttachDef.Size,
                fire_modes=fire_modes,
                health_info=HealthInfo.from_params(self.Components.SHealthComponentParams),
                heat=HeatInfo.from_params(self.Components.EntityComponentHeatConnection),
                distortion=DistortionInfo.from_params(self.Components.SDistortionParams),
                manufacturer=self.Components.SAttachableComponentParams.AttachDef.Manufacturer,
                description=localizer_en.get(
                    self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
                chinese_description=localizer_cn.get(
                    self.Components.SAttachableComponentParams.AttachDef.Localization.Description)
            )









