from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemClothingParams, SCItemPurchasableParamsType
from .base_model import PurchaseInfo
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en


class Clothing(UniversalData):

    class TemperatureResistance(BaseModel):
        min: float
        max: float

    purchase_params: Optional[PurchaseInfo] = None
    temperature_resistance: TemperatureResistance
    weight: float

class ClothingRaw(BaseModel):

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SCItemClothingParams: SCItemClothingParams
        SCItemPurchasableParams: Annotated[Optional[SCItemPurchasableParamsType], Field(alias="SCItemPurchasableParams")] = None

    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    Components: Components

    def to_clothing(self) -> Clothing:
        return Clothing(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            purchase_params=PurchaseInfo.from_purchase_params(self.Components.SCItemPurchasableParams),
            temperature_resistance=Clothing.TemperatureResistance(
                min=self.Components.SCItemClothingParams.TemperatureResistance.MinResistance,
                max=self.Components.SCItemClothingParams.TemperatureResistance.MaxResistance
            ),
            weight=self.Components.SEntityPhysicsControllerParams.PhysType.Mass
        )
