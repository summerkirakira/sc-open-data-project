from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import WeaponRegenPoolType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en


class WeaponRegenPool(UniversalData):
    ammo_load: int
    regen_fill_rate: int


class WeaponRegenPoolRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SCItemWeaponRegenPoolComponentParams: WeaponRegenPoolType

    Components: Components

    def to_weapon_regen_pool(self) -> WeaponRegenPool:
        return WeaponRegenPool(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            ammo_load=self.Components.SCItemWeaponRegenPoolComponentParams.ammoLoad,
            regen_fill_rate=self.Components.SCItemWeaponRegenPoolComponentParams.regenFillRate,

            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),

            manufacturer=self.Components.SAttachableComponentParams.AttachDef.Manufacturer,
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description)
        )
