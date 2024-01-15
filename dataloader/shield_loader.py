from utils.file_manager import sc, get_json_dir
from models.shield import ShieldRaw, Shield
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_shield_from_p4k() -> list[Shield]:
    """Load a shield from a P4K file"""
    shield_path = "libs/foundry/records/entities/scitem/ships/shieldgenerator/*"
    shield_files = sc.datacore.search_filename(shield_path)
    shield_list = []
    for shield_file in shield_files:
        shield_info = sc.datacore.record_to_dict(shield_file)
        try:
            shield_info = load_raw_data_from_dict(shield_info)
            shield_raw = ShieldRaw(**shield_info)
        except Exception as e:
            logger.error(f"Failed to load {shield_file}: {e}")
            continue

        shield = shield_raw.to_shield()
        shield_list.append(shield)

        logger.success(f"Loaded {shield.chinese_name} successfully")

    cache_data = [shield.model_dump(mode="json") for shield in shield_list]
    with open(json_dir / "shield.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return shield_list


def load_shield_from_cache() -> list[Shield]:
    """Load a shield from a json file"""
    shield_list = []
    with open(json_dir / "shield.json", "r") as f:
        shield_raw_list = json.load(f)
    for shield_raw in shield_raw_list:
        shield = Shield(**shield_raw)
        shield_list.append(shield)
        logger.success(f"Loaded {shield.chinese_name} successfully")
    return shield_list


def load_shield() -> list[Shield]:
    """Load a shield from cache if exists, otherwise load from P4K"""
    try:
        return load_shield_from_cache()
    except FileNotFoundError:
        return load_shield_from_p4k()


if __name__ == "__main__":
    load_shield()