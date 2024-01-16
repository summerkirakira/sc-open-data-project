from .base_model import UniversalData, SAttachableComponentParams, SEntityPhysicsControllerParams, SCItemPurchasableParamsType, SCItemWeaponComponentParamsType, SCItemShieldGeneratorParams, SItemPortContainerComponentParamsType
from .base_model import SHealthComponentParamsType, SDistortionParamsType, HealthInfo, EntityComponentPowerConnection, EntityComponentHeatConnection
from .base_model import SEntityComponentDefaultLoadoutParamsType, VehicleComponentParams
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from utils.localizer import localizer_cn, localizer_en
from .fps_magazine import FPSMagazine
from .utils import get_item_by_ref
from utils.shop_info import ShopInfo, get_shop_info_by_ref


from models.controller import Controller
from models.armor import Armor
from models.cargo_grid import CargoGrid
from models.cooler import Cooler
from models.fuel_intake import FuelIntake
from models.fuel_tank import FuelTank
from models.missile_rack import MissileRack
from models.skin import Skin
from models.power_plant import PowerPlant
from models.qd import QuantumDrive
from models.personal_storage import PersonalStorage
from models.self_destruct import SelfDestruct
from models.shield import Shield
from models.thruster import Thruster


class Ship(UniversalData):

    controller: Controller
    manufacturer: str = ""
    vehicle: VehicleComponentParams
    armor: Armor
    cargo: list[CargoGrid]
    coolers: list[Cooler]
    fuel_intakes: list[FuelIntake]
    fuel_tanks: list[FuelTank]
    missile_racks: list[MissileRack]
    paints: list[Skin]
    power_plants: list[PowerPlant]
    qd: QuantumDrive
    personal_storage: PersonalStorage
    self_destruct: SelfDestruct
    shields: list[Shield]
    thrusts: list[Thruster]


class ShipRaw(BaseModel):

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SCItemPurchasableParams: SCItemPurchasableParamsType
        VehicleComponentParams: VehicleComponentParams
        SEntityComponentDefaultLoadoutParams: Optional[SEntityComponentDefaultLoadoutParamsType] = None
        SItemPortContainerComponentParams: Optional[SItemPortContainerComponentParamsType] = None


