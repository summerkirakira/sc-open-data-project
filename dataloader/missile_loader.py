from utils.file_manager import sc, get_json_dir
from models.missile import MissileRaw, Missile
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_missile_from_p4k() -> list[Missile]:
    """Load a missile from a P4K file"""
    missile_path = "libs/foundry/records/entities/scitem/ships/weapons/missiles/*"
    missile_files = sc.datacore.search_filename(missile_path)
    missile_list = []
    for missile_file in missile_files:
        missile_info = sc.datacore.record_to_dict(missile_file)
        missile_info = load_raw_data_from_dict(missile_info)
        try:
            missile_raw = MissileRaw(**missile_info)
        except Exception as e:
            logger.error(f"Failed to load {missile_file}: {e}")
            continue

        missile = missile_raw.to_missile()
        missile_list.append(missile)

        logger.success(f"Loaded {missile.chinese_name} successfully")

    cache_data = [missile.model_dump(mode="json") for missile in missile_list]
    with open(json_dir / "missile.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return missile_list


def load_missile_from_cache() -> list[Missile]:
    """Load a missile from a json file"""
    missile_list = []
    with open(json_dir / "missile.json", "r") as f:
        missile_raw_list = json.load(f)
    for missile_raw in missile_raw_list:
        missile = Missile(**missile_raw)
        missile_list.append(missile)
        logger.success(f"Loaded {missile.chinese_name} successfully")
    return missile_list


def load_missile() -> list[Missile]:
    """Load a missile from cache if exists, otherwise load from P4K"""
    try:
        return load_missile_from_cache()
    except FileNotFoundError:
        return load_missile_from_p4k()


if __name__ == "__main__":
    load_missile()