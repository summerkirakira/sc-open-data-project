from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import SInventoryParams
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .utils import get_item_by_ref
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class PersonalStorage(UniversalData):

        data: SInventoryParams
        manufacturer: str = ""
        size: int


class PersonalStorageRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SInventoryParams: SInventoryParams

    Components: Components

    def to_personal_storage(self) -> PersonalStorage:
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size
        grade = self.Components.SAttachableComponentParams.AttachDef.Grade

        return PersonalStorage(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            data=self.Components.SInventoryParams,
            manufacturer=manufacturer,
            size=size,
            grade=grade,

            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
        )