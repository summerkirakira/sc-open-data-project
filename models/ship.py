from __future__ import annotations

from typing import Any, Optional, List, Dict, Union

from pydantic import BaseModel


class LocationAudioPlayTrigger(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class LocationAudioStopTrigger(BaseModel):
    __polymorphicType: str
    __type: str
    audioTrigger: str


class DisplayFeatures(BaseModel):
    Callout1: str
    Callout2: str
    Callout3: str
    FrontendBackground: str
    History: str
    LogoSimplifiedWhite: str
    UIPriority: int
    __type: str
    locationAudioPlayTrigger: LocationAudioPlayTrigger
    locationAudioStopTrigger: LocationAudioStopTrigger


class Localization(BaseModel):
    Description: str
    Name: str
    ShortName: str
    __type: str
    displayFeatures: DisplayFeatures


class InventoryOccupancyDimensions(BaseModel):
    __type: str
    x: float
    y: float
    z: float


class InventoryOccupancyVolume(BaseModel):
    __polymorphicType: str
    __type: str
    microSCU: int


class MannequinTags(BaseModel):
    __type: str
    mannequinBaseTag: str
    mannequinClassTag: str
    mannequinTypeTag: str


class AttachDef(BaseModel):
    DisplayType: str
    Grade: int
    Localization: Localization
    Manufacturer: str
    RequiredTags: str
    Size: int
    SubType: str
    Tags: str
    Type: str
    __type: str
    ignoredAttachAxis: str
    inheritParentManufacturer: bool
    inventoryOccupancyDimensions: InventoryOccupancyDimensions
    inventoryOccupancyDimensionsUIOverride: Any
    inventoryOccupancyVolume: InventoryOccupancyVolume
    mannequinTags: MannequinTags


class SAttachableComponentParams(BaseModel):
    AttachDef: AttachDef
    __polymorphicType: str
    __type: str
    attachToTileItemPort: str
    entityAttachParams: Any


class SItemPortLoadoutEntryParams(BaseModel):
    __type: str
    entityClassName: str
    entityClassReference: str
    inventoryContainer: Any
    itemPortName: str
    loadout: Optional[Loadout]


class Entry(BaseModel):
    SItemPortLoadoutEntryParams: SItemPortLoadoutEntryParams


class Loadout(BaseModel):
    InventoryItems: List
    WearRange: Any
    __polymorphicType: str
    __type: str
    entries: List[Entry]


class SEntityComponentDefaultLoadoutParams(BaseModel):
    __polymorphicType: str
    __type: str
    loadout: Loadout


class Components(BaseModel):
    SAttachableComponentParams: SAttachableComponentParams
    SEntityComponentDefaultLoadoutParams: SEntityComponentDefaultLoadoutParams


class ShipRaw(BaseModel):
    Components: Components

