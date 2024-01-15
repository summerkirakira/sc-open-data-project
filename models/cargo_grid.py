from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SItemPortContainerComponentParamsType
from .base_model import SHealthComponentParamsType, SDistortionParamsType, SCItemInventoryContainerComponentParamsType, HealthInfo, EntityComponentPowerConnection, EntityComponentHeatConnection
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .utils import get_item_by_ref
from utils.shop_info import ShopInfo, get_shop_info_by_ref
from .sub_cargo_grid import SubCargoGrid, InteriorDimensions



class Dimensions(BaseModel):
    __type: str
    x: float
    y: float
    z: float


class SCItemCargoGridParamsType(BaseModel):
    crateGenPercentageOnDestroy: float
    crateMaxOnDestroy: int
    damageConfiguration: str
    dimensions: Dimensions
    invisible: bool
    minVolatilePowerToExplode: float
    miningOnly: bool
    transformDependant: bool



class CargoGrid(UniversalData):

    sub_cargo_grid: Optional[SubCargoGrid]
    manufacturer: str = ""
    size: int


class CargoGridRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SCItemInventoryContainerComponentParams: Optional[SCItemInventoryContainerComponentParamsType] = None
        SCItemCargoGridParams: Optional[SCItemCargoGridParamsType] = None

    Components: Components

    def to_cargo_grid(self, sub_cargo_grids: list[SubCargoGrid]) -> CargoGrid:
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size
        grade = self.Components.SAttachableComponentParams.AttachDef.Grade

        sub_cargo_grid = None

        if self.Components.SCItemInventoryContainerComponentParams is not None:
            sub_cargo_grid = get_item_by_ref(sub_cargo_grids, self.Components.SCItemInventoryContainerComponentParams.containerParams)
        if self.Components.SCItemCargoGridParams is not None:
            sub_cargo_grid = SubCargoGrid(
                ref="",
                path="",
                type="",
                grid=InteriorDimensions(
                    x=self.Components.SCItemCargoGridParams.dimensions.x,
                    y=self.Components.SCItemCargoGridParams.dimensions.y,
                    z=self.Components.SCItemCargoGridParams.dimensions.z
                )
            )

        return CargoGrid(
            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,
            data=self.Components.SCItemInventoryContainerComponentParams,
            manufacturer=manufacturer,
            size=size,
            grade=grade,
            sub_cargo_grid=sub_cargo_grid,


            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            shop_info=get_shop_info_by_ref(self.ref)
        )


