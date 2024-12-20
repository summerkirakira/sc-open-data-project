from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import SCItemShieldEmitterParamsType
from .base_model import IFCSParamsType
from models.cap_assignment import CapAssignmentRaw, CapAssignment
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .utils import get_item_by_ref
from utils.shop_info import ShopInfo, get_shop_info_by_ref


class Controller(UniversalData):

    data: Optional[IFCSParamsType]
    shield: Optional[SCItemShieldEmitterParamsType]

    manufacturer: str = ""
    size: int
    path: str = ""


class ControllerRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        IFCSParams: Optional[IFCSParamsType] = None
        SCItemShieldEmitterParams: Optional[SCItemShieldEmitterParamsType] = None

    Components: Components

    def to_controller(self, cap_assignment: list[CapAssignment]) -> Controller:
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size
        grade = self.Components.SAttachableComponentParams.AttachDef.Grade

        if self.Components.SCItemShieldEmitterParams:
            self.Components.SCItemShieldEmitterParams.regenMapping = get_item_by_ref(cap_assignment, self.Components.SCItemShieldEmitterParams.capacitorAssignmentInputOutputRegen).inputOutputMapping
            self.Components.SCItemShieldEmitterParams.resistanceMapping = get_item_by_ref(cap_assignment, self.Components.SCItemShieldEmitterParams.capacitorAssignmentInputOutputResistance).inputOutputMapping

        return Controller(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            data=self.Components.IFCSParams,
            manufacturer=manufacturer,
            size=size,
            grade=grade,

            shield=self.Components.SCItemShieldEmitterParams,



            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
        )