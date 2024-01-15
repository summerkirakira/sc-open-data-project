from utils.file_manager import sc, get_json_dir
from models.vehicle_ammo import VehicleAmmoRaw, VehicleAmmo
from loguru import logger
import json


json_dir = get_json_dir()


def load_fps_ammo_from_p4k() -> list[VehicleAmmo]:
    """Load a fps_ammo from a P4K file"""
    fps_ammo_path = "libs/foundry/records/ammoparams/vehicle/*"
    fps_ammo_files = sc.datacore.search_filename(fps_ammo_path)
    fps_ammo_list = []
    for fps_ammo_file in fps_ammo_files:
        fps_ammo_info = sc.datacore.record_to_dict(fps_ammo_file)
        try:
            fps_ammo_raw = VehicleAmmoRaw(**fps_ammo_info)
        except Exception as e:
            logger.error(f"Failed to load {fps_ammo_file}: {e}")
            continue

        fps_ammo = fps_ammo_raw.to_vehicle_ammo()
        fps_ammo_list.append(fps_ammo)

        logger.success(f"Loaded {fps_ammo.chinese_name} successfully")

    cache_data = [fps_ammo.model_dump(mode="json") for fps_ammo in fps_ammo_list]
    with open(json_dir / "vehicle_ammo.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return fps_ammo_list


def load_fps_ammo_from_cache() -> list[VehicleAmmo]:
    """Load a fps_ammo from a json file"""
    fps_ammo_list = []
    with open(json_dir / "vehicle_ammo.json", "r") as f:
        fps_ammo_raw_list = json.load(f)
    for fps_ammo_raw in fps_ammo_raw_list:
        fps_ammo = VehicleAmmo(**fps_ammo_raw)
        fps_ammo_list.append(fps_ammo)
        logger.success(f"Loaded {fps_ammo.chinese_name} successfully")
    return fps_ammo_list


def load_vehicle_ammo() -> list[VehicleAmmo]:
    """Load a fps_ammo from cache if exists, otherwise load from P4K"""
    try:
        return load_fps_ammo_from_cache()
    except FileNotFoundError:
        return load_fps_ammo_from_p4k()


if __name__ == "__main__":
    load_vehicle_ammo()