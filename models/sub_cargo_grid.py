from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class InteriorDimensions(BaseModel):
    __type: str
    x: float
    y: float
    z: float


class GridCellSize(BaseModel):
    __polymorphicType: str
    __type: str
    centimeters: int


class GridPosOffset(BaseModel):
    __type: str
    x: float
    y: float
    z: float


class MaxPermittedItemSize(BaseModel):
    __type: str
    x: float
    y: float
    z: float


class MinPermittedItemSize(BaseModel):
    __type: str
    x: float
    y: float
    z: float


class InventoryType(BaseModel):
    __polymorphicType: str
    __type: str
    appliedForceOnParentDestruction: float
    gridCellSize: GridCellSize
    gridPosOffset: GridPosOffset
    isExternalContainer: bool
    maxPercentageErasedOnParentDestruction: int
    maxPermittedItemSize: MaxPermittedItemSize
    minPermittedItemSize: MinPermittedItemSize
    overrideStorableItemTypes: List
    randomDestructionDistributionExponent: float


class SubCargoGrid(BaseModel):

    ref: str
    path: str
    type: str
    grid: InteriorDimensions


class SubCargoGridRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')
    interiorDimensions: InteriorDimensions
    # inventoryType: InventoryType

    def to_sub_cargo_grid(self) -> SubCargoGrid:
        return SubCargoGrid(
            ref=self.ref,
            path=self.path,
            type=self.type,
            grid=self.interiorDimensions
        )