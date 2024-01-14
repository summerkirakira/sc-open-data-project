from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParams
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated


class FPSWeapon(UniversalData):
    mass: float


class FPSWeaponRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SEntityPhysicsControllerParams: SEntityPhysicsControllerParams
        SCItemWeaponComponentParams: SCItemWeaponComponentParams
        SCItemPurchasableParams: Annotated[Optional[SCItemPurchasableParamsType], Field(alias="SCItemPurchasableParams")] = None

    Components: Components

    def to_weapon(self) -> FPSWeapon:
        ...


