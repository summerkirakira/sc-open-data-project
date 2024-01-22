from .base_model import UniversalData, SAttachableComponentParams, SCItemPurchasableParamsType, SItemPortContainerComponentParamsType
from .base_model import SEntityComponentDefaultLoadoutParamsType, VehicleComponentParams, SGeometryResourceParams
from pydantic import BaseModel, Field
from typing import Optional
from utils.localizer import localizer_cn, localizer_en


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
from models.turret import Turret
from models.weapon_regen_pool import WeaponRegenPool
from models.weapon_model import VehicleWeapon
from dataloader.ship_item_loader import ShipItemLoader
from utils.shop_info import get_shop_info_by_ref, ShopInfo
from utils.ship_alias import ShipAlis, ShipNameBinding, get_ship_alias_by_id, get_ship_name_binding_by_name
from utils.vehicle import get_vehicle_definition
from loguru import logger


class ItemRef(BaseModel):
    ref: str


class Hull(BaseModel):
    name: str
    health: int


class Flare(BaseModel):
    number: int
    lifetime: float


class Ship(UniversalData):

    mass: float
    controllers: list[Controller]
    manufacturer: str = ""
    vehicle: VehicleComponentParams
    armor: Armor
    cargos: list[CargoGrid]
    coolers: list[Cooler]
    fuel_intakes: list[FuelIntake]
    fuel_tanks: list[FuelTank]
    missile_racks: list[MissileRack]
    paints: list[Skin]
    power_plants: list[PowerPlant]
    qd: Optional[QuantumDrive]
    personal_storage: Optional[PersonalStorage]
    self_destruct: Optional[SelfDestruct]
    shields: list[Shield]
    thrusts: list[Thruster]
    shop_info: list[ShopInfo]
    ship_alias: Optional[ShipAlis]
    ship_name_binding: Optional[ShipNameBinding]
    hulls: list[Hull]
    turrets: list[Turret]

    flare: Flare

    weapon_regen_pool: Optional[WeaponRegenPool]
    weapons: list[VehicleWeapon]
    is_real_ship: bool = True

    @classmethod
    def load_from_cache(cls, loader: ShipItemLoader, data: dict) -> 'Ship':
        new_data = data.copy()
        for key in data:
            if key in ['shop_info', 'vehicle', 'ship_alias', 'ship_name_binding', 'hulls', 'flare']:
                continue
            if isinstance(data[key], int):
                continue
            if isinstance(data[key], str):
                continue
            if isinstance(data[key], float):
                continue
            if isinstance(data[key], list):
                new_data[key] = []
                for ref in data[key]:
                    item = loader.get_item_by_ref(ref['ref'])
                    new_data[key].append(item)
            elif data[key] is not None:
                new_data[key] = loader.get_item_by_ref(data[key]['ref'])
        return Ship(**new_data)

    def to_dict(self) -> dict:
        data = self.model_dump()
        new_data = data.copy()
        for key in data:
            if key in ['shop_info', 'vehicle', 'ship_alias', 'ship_name_binding', 'hulls', 'flare']:
                continue
            if isinstance(data[key], int):
                continue
            if isinstance(data[key], str):
                continue
            if isinstance(data[key], float):
                continue
            if isinstance(data[key], list):
                new_data[key] = []
                for item in data[key]:
                    new_data[key].append(
                        {
                            'ref': item['ref'],
                        }
                    )
            elif data[key] is not None:
                new_data[key] = {
                    'ref': data[key]['ref'],
                }

        return new_data


class ShipRaw(BaseModel):

    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')

    class Components(BaseModel):
        SAttachableComponentParams: SAttachableComponentParams
        SCItemPurchasableParams: SCItemPurchasableParamsType
        VehicleComponentParams: VehicleComponentParams
        SEntityComponentDefaultLoadoutParams: Optional[SEntityComponentDefaultLoadoutParamsType] = None
        SItemPortContainerComponentParams: Optional[SItemPortContainerComponentParamsType] = None
        SGeometryResourceParams: SGeometryResourceParams

    Components: Components

    def to_ship(self, loader: ShipItemLoader) -> Ship:
        manufacturer = self.Components.SAttachableComponentParams.AttachDef.Manufacturer
        size = self.Components.SAttachableComponentParams.AttachDef.Size

        controllers = []
        armor = None
        cargos = []
        coolers = []
        fuel_intakes = []
        fuel_tanks = []
        missile_racks = []
        paints = []
        power_plants = []
        qd = None
        personal_storage = None
        self_destruct = None
        shields = []
        thrusts = []
        turrets = []
        weapons = []
        weapon_regen_pool = None

        hulls, mass = get_vehicle_definition(self.Components.VehicleComponentParams.vehicleDefinition)

        try:
            hulls = [Hull(**item) for item in hulls]
        except Exception as e:
            logger.error(f'get_vehicle_definition error: {e}')
            hulls = []

        if self.Components.VehicleComponentParams is not None:
            self.Components.VehicleComponentParams.vehicleCareer = localizer_cn.get(self.Components.VehicleComponentParams.vehicleCareer)
            self.Components.VehicleComponentParams.vehicleName = localizer_cn.get(self.Components.VehicleComponentParams.vehicleName)
            self.Components.VehicleComponentParams.vehicleDescription = localizer_cn.get(self.Components.VehicleComponentParams.vehicleDescription)
            self.Components.VehicleComponentParams.vehicleRole = localizer_cn.get(self.Components.VehicleComponentParams.vehicleRole)

        if self.Components.SEntityComponentDefaultLoadoutParams.loadout is not None:
            for item in self.Components.SEntityComponentDefaultLoadoutParams.loadout.entries:
                ship_item = loader.get_item_by_localname(item.SItemPortLoadoutEntryParams.entityClassName)
                if ship_item is None:
                    continue

                if isinstance(ship_item, Controller):
                    controllers.append(ship_item)
                elif isinstance(ship_item, Armor):
                    armor = ship_item
                elif isinstance(ship_item, CargoGrid):
                    cargos.append(ship_item)
                elif isinstance(ship_item, Cooler):
                    coolers.append(ship_item)
                elif isinstance(ship_item, FuelIntake):
                    fuel_intakes.append(ship_item)
                elif isinstance(ship_item, FuelTank):
                    fuel_tanks.append(ship_item)
                elif isinstance(ship_item, MissileRack):
                    missile_racks.append(ship_item)
                elif isinstance(ship_item, Skin):
                    paints.append(ship_item)
                elif isinstance(ship_item, PowerPlant):
                    power_plants.append(ship_item)
                elif isinstance(ship_item, QuantumDrive):
                    qd = ship_item
                elif isinstance(ship_item, PersonalStorage):
                    personal_storage = ship_item
                elif isinstance(ship_item, SelfDestruct):
                    self_destruct = ship_item
                elif isinstance(ship_item, Shield):
                    shields.append(ship_item)
                elif isinstance(ship_item, Thruster):
                    thrusts.append(ship_item)
                elif isinstance(ship_item, Turret):
                    turrets.append(ship_item)
                elif isinstance(ship_item, VehicleWeapon):
                    weapons.append(ship_item)
                elif isinstance(ship_item, WeaponRegenPool):
                    weapon_regen_pool = ship_item


        for geometry in self.Components.SGeometryResourceParams.Geometry.SubGeometry:
            paint = loader.get_item_by_localname(geometry.SGeometryNodeParams.Tags)
            if paint is not None and isinstance(paint, Skin):
                paints.append(paint)

        if armor is None:
            armor = loader.armor[1]

        ship_name_binding = get_ship_name_binding_by_name(localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name))

        ship_alias = None

        if ship_name_binding is not None:
            ship_alias = get_ship_alias_by_id(ship_name_binding.id)
        return Ship(

            ref=self.ref,
            path=self.path,
            type=self.Components.SAttachableComponentParams.AttachDef.Type,

            mass=mass,

            manufacturer=manufacturer,
            size=size,
            controllers=controllers,
            armor=armor,
            cargos=cargos,
            coolers=coolers,
            fuel_intakes=fuel_intakes,
            fuel_tanks=fuel_tanks,
            missile_racks=missile_racks,
            paints=paints,
            power_plants=power_plants,
            qd=qd,
            personal_storage=personal_storage,
            self_destruct=self_destruct,
            shields=shields,
            thrusts=thrusts,


            name=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            chinese_name=localizer_cn.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Name),
            description=localizer_en.get(self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            chinese_description=localizer_cn.get(
                self.Components.SAttachableComponentParams.AttachDef.Localization.Description),
            shop_info=get_shop_info_by_ref(self.ref),

            vehicle=self.Components.VehicleComponentParams,
            ship_alias=ship_alias,
            ship_name_binding=ship_name_binding,

            hulls=hulls,
            turrets=turrets,

            flare=Flare(
                number=0,
                lifetime=8.,
            ),

            weapons=weapons,
            weapon_regen_pool=weapon_regen_pool,
        )


