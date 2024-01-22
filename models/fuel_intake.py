from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import SHealthComponentParamsType, SDistortionParamsType, SCItemFuelIntakeParamsType, HealthInfo, EntityComponentPowerConnection, EntityComponentHeatConnection
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .utils import get_item_by_ref
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class FuelIntake(UniversalData):

    data: Optional[SCItemFuelIntakeParamsType] = None
    manufacturer: str = ""
    power: EntityComponentPowerConnection
    size: int


class FuelIntakeRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SCItemFuelIntakeParams: Optional[SCItemFuelIntakeParamsType] = None
        EntityComponentPowerConnection: EntityComponentPowerConnection

    Components: Components

    def to_fuel_intake(self) -> FuelIntake:
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size
        grade = self.Components.SAttachableComponentParams.AttachDef.Grade
        power = self.Components.EntityComponentPowerConnection

        return FuelIntake(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            data=self.Components.SCItemFuelIntakeParams,
            manufacturer=manufacturer,
            size=size,
            grade=grade,
            power=power,

            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            shop_info=get_shop_info_by_ref(self.ref)
        )