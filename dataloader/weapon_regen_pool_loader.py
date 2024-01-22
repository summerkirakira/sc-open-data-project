from utils.file_manager import sc, get_json_dir
from models.weapon_regen_pool import WeaponRegenPoolRaw, WeaponRegenPool
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_weapon_regen_pool_from_p4k() -> list[WeaponRegenPool]:
    """Load a weapon_regen_pool from a P4K file"""
    weapon_regen_pool_path = "libs/foundry/records/entities/scitem/weaponregenpools/*"
    weapon_regen_pool_files = sc.datacore.search_filename(weapon_regen_pool_path)
    weapon_regen_pool_list = []

    for weapon_regen_pool_file in weapon_regen_pool_files:

        weapon_regen_pool_info = sc.datacore.record_to_dict(weapon_regen_pool_file)
        try:
            weapon_regen_pool_info = load_raw_data_from_dict(weapon_regen_pool_info)
            weapon_regen_pool_raw = WeaponRegenPoolRaw(**weapon_regen_pool_info)
        except Exception as e:
            logger.error(f"Failed to load {weapon_regen_pool_file}: {e}")
            continue
        try:
            weapon_regen_pool = weapon_regen_pool_raw.to_weapon_regen_pool()
        except Exception as e:
            logger.error(f"Failed to load {weapon_regen_pool_file}: {e}")
            raise e
        weapon_regen_pool_list.append(weapon_regen_pool)

        logger.success(f"Loaded {weapon_regen_pool.chinese_name} successfully")

    cache_data = [weapon_regen_pool.model_dump() for weapon_regen_pool in weapon_regen_pool_list]
    with open(json_dir / "weapon_regen_pool.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return weapon_regen_pool_list


def load_weapon_regen_pool_from_cache() -> list[WeaponRegenPool]:
    """Load a weapon_regen_pool from a json file"""
    weapon_regen_pool_list = []
    with open(json_dir / "weapon_regen_pool.json", "r") as f:
        weapon_regen_pool_raw_list = json.load(f)
    for weapon_regen_pool_raw in weapon_regen_pool_raw_list:
        weapon_regen_pool = WeaponRegenPool(**weapon_regen_pool_raw)
        weapon_regen_pool_list.append(weapon_regen_pool)
        logger.success(f"Loaded {weapon_regen_pool.chinese_name} successfully")
    return weapon_regen_pool_list


def load_weapon_regen_pool() -> list[WeaponRegenPool]:
    """Load a weapon_regen_pool from cache if exists, otherwise load from P4K"""
    try:
        return load_weapon_regen_pool_from_cache()
    except FileNotFoundError:
        return load_weapon_regen_pool_from_p4k()


if __name__ == '__main__':
    load_weapon_regen_pool_from_p4k()