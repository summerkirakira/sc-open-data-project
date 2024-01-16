from utils.file_manager import sc, get_json_dir
from models.armor import ArmorRaw, Armor
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_armor_from_p4k() -> list[Armor]:
    """Load a armor from a P4K file"""
    armor_path = "libs/foundry/records/entities/scitem/ships/armor/*"
    armor_files = sc.datacore.search_filename(armor_path)
    armor_list = []
    for armor_file in armor_files:
        armor_info = sc.datacore.record_to_dict(armor_file)
        try:
            armor_info = load_raw_data_from_dict(armor_info)
            armor_raw = ArmorRaw(**armor_info)
        except Exception as e:
            logger.error(f"Failed to load {armor_file}: {e}")
            continue

        armor = armor_raw.to_armor()
        armor_list.append(armor)

        logger.success(f"Loaded {armor.chinese_name} successfully")

    cache_data = [armor.model_dump(mode="json") for armor in armor_list]
    with open(json_dir / "armor.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return armor_list


def load_armor_from_cache() -> list[Armor]:
    """Load a armor from a json file"""
    armor_list = []
    with open(json_dir / "armor.json", "r") as f:
        armor_raw_list = json.load(f)
    for armor_raw in armor_raw_list:
        armor = Armor(**armor_raw)
        armor_list.append(armor)
        logger.success(f"Loaded {armor.chinese_name} successfully")
    return armor_list


def load_armor() -> list[Armor]:
    """Load a armor from cache if exists, otherwise load from P4K"""
    try:
        return load_armor_from_cache()
    except FileNotFoundError:
        return load_armor_from_p4k()


if __name__ == "__main__":
    load_armor()
