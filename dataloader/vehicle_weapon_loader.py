from utils.file_manager import sc, load_raw_data_from_dict, get_json_dir
from models.weapon_model import VehicleWeaponRaw, VehicleWeapon
from vehicle_ammo_loader import load_vehicle_ammo
from loguru import logger
import json


json_dir = get_json_dir()


def load_vehicle_weapon_from_p4k() -> list[VehicleWeapon]:
    """Load a vehicle_weapon from a P4K file"""
    vehicle_weapon_path = "libs/foundry/records/entities/scitem/ships/weapons/*.xml"
    vehicle_weapon_files = sc.datacore.search_filename(vehicle_weapon_path)
    vehicle_weapon_list = []

    ammos = load_vehicle_ammo()

    for vehicle_weapon_file in vehicle_weapon_files:

        if vehicle_weapon_file.filename.split("/")[-2] != "weapons":
            continue

        vehicle_weapon_info = sc.datacore.record_to_dict(vehicle_weapon_file)
        vehicle_weapon_info = load_raw_data_from_dict(vehicle_weapon_info)
        try:
            vehicle_weapon_raw = VehicleWeaponRaw(**vehicle_weapon_info)
        except Exception as e:
            logger.error(f"Failed to load {vehicle_weapon_file}: {e}")
            continue

        vehicle_weapon = vehicle_weapon_raw.to_vehicle_weapon(ammos)
        vehicle_weapon_list.append(vehicle_weapon)

        logger.success(f"Loaded {vehicle_weapon.chinese_name} successfully")

    cache_data = [vehicle_weapon.model_dump(mode="json") for vehicle_weapon in vehicle_weapon_list]
    with open(json_dir / "vehicle_weapon.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return vehicle_weapon_list


def load_vehicle_weapon_from_cache() -> list[VehicleWeapon]:
    """Load a vehicle_weapon from cache"""
    with open(json_dir / "vehicle_weapon.json", "r") as f:
        cache_data = json.load(f)
    vehicle_weapon_list = []
    for vehicle_weapon_data in cache_data:
        vehicle_weapon = VehicleWeapon(**vehicle_weapon_data)
        vehicle_weapon_list.append(vehicle_weapon)
        logger.success(f"Loaded {vehicle_weapon.chinese_name} successfully")
    return vehicle_weapon_list


def load_vehicle_weapon() -> list[VehicleWeapon]:
    """Load a vehicle_weapon from cache or P4K file"""
    try:
        return load_vehicle_weapon_from_cache()
    except:
        return load_vehicle_weapon_from_p4k()


if __name__ == "__main__":
    load_vehicle_weapon()