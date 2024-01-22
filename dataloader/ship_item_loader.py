from .cargo_grid_loader import load_cargo_grid
from .controller_loader import load_controller
from .cooler_loader import load_cooler
from .fuel_intake_loader import load_fuel_intake
from .fuel_tank_loader import load_fuel_tank
from .missile_rack_loader import load_missile_rack
from .manufacturer_loader import load_manufacture
from .armor_loader import load_armor
from .skin_loader import load_skin
from .power_plant_loader import load_power_plant
from .qd_loader import load_qd
from .personal_storage_loader import load_personal_storage
from .self_destruct_loader import load_self_destruct
from .shield_loader import load_shield
from .thruster_loader import load_thruster
from .vehicle_weapon_loader import load_vehicle_weapon
from .manufacturer_loader import load_manufacture
from .weapon_regen_pool_loader import load_weapon_regen_pool
from .turret_loader import load_turret
from models.base_model import UniversalData
from typing import Optional


class ShipItemLoader:
    def __init__(self):
        self.cargo_grid = load_cargo_grid()
        self.controller = load_controller()
        self.cooler = load_cooler()
        self.fuel_intake = load_fuel_intake()
        self.fuel_tank = load_fuel_tank()
        self.missile_rack = load_missile_rack()
        self.manufacturer = load_manufacture()
        self.armor = load_armor()
        self.skin = load_skin()
        self.power_plant = load_power_plant()
        self.qd = load_qd()
        self.personal_storage = load_personal_storage()
        self.self_destruct = load_self_destruct()
        self.shield = load_shield()
        self.thruster = load_thruster()
        self.vehicle_weapon = load_vehicle_weapon()
        self.manufacturer = load_manufacture()
        self.weapon_regen_pool = load_weapon_regen_pool()
        self.turret = load_turret()
        self.weapons = load_vehicle_weapon()

    def get_item_by_localname(self, localname: str):
        for member in self.__dict__.values():
            if isinstance(member, list):
                item = self._get_item_by_localname(member, localname)
                if item:
                    return item

    def get_item_by_ref(self, ref: str):
        for member in self.__dict__.values():
            if isinstance(member, list):
                item = self._get_item_by_ref(member, ref)
                if item:
                    return item

    @classmethod
    def _get_item_by_ref(cls, item_list: list[UniversalData], ref: str) -> Optional[UniversalData]:
        for item in item_list:
            if item.ref == ref:
                return item
        return None

    @classmethod
    def _get_item_by_localname(cls, item_list: list[UniversalData], localname: str) -> Optional[UniversalData]:
        for item in item_list:
            if item.path.split('/')[-1].split('.')[-2].lower() == localname.lower():
                return item
        return None


if __name__ == "__main__":
    ship_item_loader = ShipItemLoader()
    print(ship_item_loader.get_item_by_localname(''))
