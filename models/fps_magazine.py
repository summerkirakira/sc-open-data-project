from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SAmmoContainerComponentParamsType, SCItemMissileParamsType, SCItemPurchasableParamsType, PurchaseInfo, MissileInfo
from .fps_ammo import FPSAmmo
from pydantic import BaseModel, Field
from typing import List, Optional
from utils.localizer import localizer_cn, localizer_en
from .utils import get_item_by_ref
from loguru import logger
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class FPSMagazine(UniversalData):

    purchase_params: Optional[PurchaseInfo] = None
    ammo: Optional[FPSAmmo] = None
    missile: Optional[MissileInfo] = None
    initial_ammo_count: int
    weight: float
    max_ammo_count: int
    max_restock_count: int
    micro_scu: int
    mass: float
    shop_info: list[ShopInfo]


class FPSMagazineRaw(BaseModel):

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SAmmoContainerComponentParams: Optional[SAmmoContainerComponentParamsType] = None
        SCItemMissileParams: Optional[SCItemMissileParamsType] = None
        SCItemPurchasableParams: Optional[SCItemPurchasableParamsType] = None

    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    Components: Components

    def to_magazine(self, ammos: list[FPSAmmo]) -> Optional[FPSMagazine]:
        if self.Components.SAmmoContainerComponentParams is None:
            logger.warning(f"Magazine {self.ref} has no ammo container component.")
            return None
        if get_item_by_ref(ammos, self.Components.SAmmoContainerComponentParams.ammoParamsRecord) is not None:
            return FPSMagazine(
                ref=self.ref,
                path=self.path,
                type=self.type,
                size=self.Components.SAttachableComponentParams.AttachDef.Size,
                name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                purchase_params=PurchaseInfo.from_purchase_params(self.Components.SCItemPurchasableParams),
                ammo=get_item_by_ref(ammos, self.Components.SAmmoContainerComponentParams.ammoParamsRecord),
                initial_ammo_count=self.Components.SAmmoContainerComponentParams.initialAmmoCount,
                weight=self.Components.SEntityPhysicsControllerParams.PhysType.Mass,
                max_ammo_count=self.Components.SAmmoContainerComponentParams.maxAmmoCount,
                max_restock_count=self.Components.SAmmoContainerComponentParams.maxRestockCount,
                description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
                chinese_description=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
                mass=self.Components.SEntityPhysicsControllerParams.PhysType.Mass,
                micro_scu=self.Components.SAttachableComponentParams.AttachDef.inventoryOccupancyVolume.microSCU,
                shop_info=get_shop_info_by_ref(self.ref)
            )
        elif self.Components.SCItemMissileParams is not None:
            return FPSMagazine(
                ref=self.ref,
                path=self.path,
                type=self.type,
                size=self.Components.SAttachableComponentParams.AttachDef.Size,
                name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                purchase_params=PurchaseInfo.from_purchase_params(self.Components.SCItemPurchasableParams),
                missile=self.Components.SCItemMissileParams.to_missile_info(),
                initial_ammo_count=self.Components.SAmmoContainerComponentParams.initialAmmoCount,
                weight=self.Components.SEntityPhysicsControllerParams.PhysType.Mass,
                max_ammo_count=self.Components.SAmmoContainerComponentParams.maxAmmoCount,
                max_restock_count=self.Components.SAmmoContainerComponentParams.maxRestockCount,
                description=localizer_en.get(
                    self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
                chinese_description=localizer_cn.get(
                    self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
                mass=self.Components.SEntityPhysicsControllerParams.PhysType.Mass,
                micro_scu=self.Components.SAttachableComponentParams.AttachDef.inventoryOccupancyVolume.microSCU,
                shop_info=get_shop_info_by_ref(self.ref)
            )



