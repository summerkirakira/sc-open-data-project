from utils.file_manager import sc, load_raw_data_from_dict, get_json_dir
from models.fps_weapon import FPSWeaponRaw, FPSWeapon
from fps_magazine_loader import load_fps_magazine
from loguru import logger
import json


json_dir = get_json_dir()


def load_fps_weapon_from_p4k() -> list[FPSWeapon]:
    """Load a fps_weapon from a P4K file"""
    magazines = load_fps_magazine()
    fps_weapon_path = "libs/foundry/records/entities/scitem/weapons/fps_weapons/*"
    fps_weapon_files = sc.datacore.search_filename(fps_weapon_path)
    fps_weapon_list = []
    for fps_weapon_file in fps_weapon_files:
        fps_weapon_info = sc.datacore.record_to_dict(fps_weapon_file)
        fps_weapon_info = load_raw_data_from_dict(fps_weapon_info)
        try:
            fps_weapon_raw = FPSWeaponRaw(**fps_weapon_info)
        except Exception as e:
            logger.error(f"Failed to load {fps_weapon_file}: {e}")
            continue

        fps_weapon = fps_weapon_raw.to_fps_weapon(magazines=magazines)
        fps_weapon_list.append(fps_weapon)

        logger.success(f"Loaded {fps_weapon.chinese_name} successfully")

    cache_data = [fps_weapon.model_dump(mode="json") for fps_weapon in fps_weapon_list]
    with open(json_dir / "fps_weapon.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return fps_weapon_list


def load_fps_weapon_from_cache() -> list[FPSWeapon]:
    """Load a fps_weapon from cache"""
    with open(json_dir / "fps_weapon.json", "r") as f:
        cache_data = json.load(f)
    fps_weapon_list = []
    for fps_weapon_data in cache_data:
        fps_weapon = FPSWeapon(**fps_weapon_data)
        fps_weapon_list.append(fps_weapon)
        logger.success(f"Loaded {fps_weapon.chinese_name} successfully")
    return fps_weapon_list


def load_fps_weapon() -> list[FPSWeapon]:
    """Load a fps_weapon from cache or P4K file"""
    try:
        return load_fps_weapon_from_cache()
    except:
        return load_fps_weapon_from_p4k()


if __name__ == "__main__":
    load_fps_weapon()