from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SCItemShieldGeneratorParams, SItemPortContainerComponentParamsType
from .base_model import SHealthComponentParamsType, SDistortionParamsType, HealthInfo, EntityComponentPowerConnection, EntityComponentHeatConnection
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .fps_magazine import FPSMagazine
from .utils import get_item_by_ref
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class Shield(UniversalData):

    health_info: HealthInfo
    manufacturer: str = ""
    size: int
    grade: int
    regen: float
    regen_delay: float
    down_regen_delay: float
    absorption_physical_min: float
    absorption_physical_max: float
    resistance_min: float
    resistance_max: float

    power: EntityComponentPowerConnection
    heat: EntityComponentHeatConnection
    distortion: Optional[SDistortionParamsType] = None
    ship_info: list[ShopInfo]


class ShieldRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SCItemPurchasableParams: SCItemPurchasableParamsType
        SCItemShieldGeneratorParams: SCItemShieldGeneratorParams
        SHealthComponentParams: SHealthComponentParamsType
        SDistortionParams: Optional[SDistortionParamsType] = None
        EntityComponentPowerConnection: EntityComponentPowerConnection
        EntityComponentHeatConnection: EntityComponentHeatConnection

    Components: Components

    def to_shield(self) -> Shield:
        ...
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size
        grade = self.Components.SAttachableComponentParams.AttachDef.Grade
        regen = self.Components.SCItemShieldGeneratorParams.MaxShieldRegen
        regen_delay = self.Components.SCItemShieldGeneratorParams.DamagedRegenDelay
        down_regen_delay = self.Components.SCItemShieldGeneratorParams.DownedRegenDelay
        absorption_physical_min = self.Components.SCItemShieldGeneratorParams.ShieldAbsorption[0].SShieldAbsorption.Min
        absorption_physical_max = self.Components.SCItemShieldGeneratorParams.ShieldAbsorption[0].SShieldAbsorption.Max
        resistance_min = self.Components.SCItemShieldGeneratorParams.ShieldResistance[0].SShieldResistance.Min
        resistance_max = self.Components.SCItemShieldGeneratorParams.ShieldResistance[0].SShieldResistance.Max

        power = self.Components.EntityComponentPowerConnection
        heat = self.Components.EntityComponentHeatConnection

        ship_info = get_shop_info_by_ref(self.ref)

        return Shield(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            manufacturer=manufacturer,
            size=size,
            grade=grade,
            regen=regen,
            regen_delay=regen_delay,
            down_regen_delay=down_regen_delay,
            absorption_physical_min=absorption_physical_min,
            absorption_physical_max=absorption_physical_max,
            resistance_min=resistance_min,
            resistance_max=resistance_max,
            power=power,
            heat=heat,
            distortion=self.Components.SDistortionParams,
            ship_info=ship_info,
            health_info=HealthInfo.from_params(self.Components.SHealthComponentParams),


            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description)
        )

