from utils.file_manager import sc, get_json_dir
from models.missile_rack import MissileRackRaw, MissileRack
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_missile_rack_from_p4k() -> list[MissileRack]:
    """Load a missile_rack from a P4K file"""
    missile_rack_path = "libs/foundry/records/entities/scitem/ships/missileracks/*"
    missile_rack_files = sc.datacore.search_filename(missile_rack_path)
    missile_rack_list = []
    for missile_rack_file in missile_rack_files:
        missile_rack_info = sc.datacore.record_to_dict(missile_rack_file)
        try:
            missile_rack_info = load_raw_data_from_dict(missile_rack_info)
            missile_rack_raw = MissileRackRaw(**missile_rack_info)
        except Exception as e:
            logger.error(f"Failed to load {missile_rack_file}: {e}")
            continue

        missile_rack = missile_rack_raw.to_missile_rack()
        missile_rack_list.append(missile_rack)

        logger.success(f"Loaded {missile_rack.chinese_name} successfully")

    cache_data = [missile_rack.model_dump(mode="json") for missile_rack in missile_rack_list]
    with open(json_dir / "missile_rack.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return missile_rack_list


def load_missile_rack_from_cache() -> list[MissileRack]:
    """Load a missile_rack from a json file"""
    missile_rack_list = []
    with open(json_dir / "missile_rack.json", "r") as f:
        missile_rack_raw_list = json.load(f)
    for missile_rack_raw in missile_rack_raw_list:
        missile_rack = MissileRack(**missile_rack_raw)
        missile_rack_list.append(missile_rack)
        logger.success(f"Loaded {missile_rack.chinese_name} successfully")
    return missile_rack_list


def load_missile_rack() -> list[MissileRack]:
    """Load a missile_rack from cache if exists, otherwise load from P4K"""
    try:
        return load_missile_rack_from_cache()
    except FileNotFoundError:
        return load_missile_rack_from_p4k()


if __name__ == "__main__":
    load_missile_rack()