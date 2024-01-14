from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemClothingParams, SCItemPurchasableParamsType
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en


class Clothing(UniversalData):

    class PurchaseParams(BaseModel):
        name: str
        purchase_type: str

    class TemperatureResistance(BaseModel):
        min: float
        max: float

    purchase_params: Optional[PurchaseParams] = None
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
        if self.Components.SCItemPurchasableParams is None:
            return Clothing(
                ref=self.ref,
                path=self.path,
                type=self.type,
                name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
                purchase_params=None,
                temperature_resistance=Clothing.TemperatureResistance(
                    min=self.Components.SCItemClothingParams.TemperatureResistance.MinResistance,
                    max=self.Components.SCItemClothingParams.TemperatureResistance.MaxResistance
                ),
                weight=self.Components.SEntityPhysicsControllerParams.PhysType.Mass
            )
        return Clothing(
            ref=self.ref,
            path=self.path,
            type=self.type,
            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            purchase_params=Clothing.PurchaseParams(
                name=localizer_cn.get(self.Components.SCItemPurchasableParams.displayName),
                purchase_type=localizer_cn.get(self.Components.SCItemPurchasableParams.displayType)
            ),
            temperature_resistance=Clothing.TemperatureResistance(
                min=self.Components.SCItemClothingParams.TemperatureResistance.MinResistance,
                max=self.Components.SCItemClothingParams.TemperatureResistance.MaxResistance
            ),
            weight=self.Components.SEntityPhysicsControllerParams.PhysType.Mass
        )
