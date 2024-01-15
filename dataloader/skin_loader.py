from utils.file_manager import sc, get_json_dir
from models.skin import SkinRaw, Skin
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_skin_from_p4k() -> list[Skin]:
    """Load a skin from a P4K file"""
    skin_path = "libs/foundry/records/entities/scitem/ships/paints/*"
    skin_files = sc.datacore.search_filename(skin_path)
    skin_list = []
    for skin_file in skin_files:
        skin_info = sc.datacore.record_to_dict(skin_file)
        try:
            skin_info = load_raw_data_from_dict(skin_info)
            skin_raw = SkinRaw(**skin_info)
        except Exception as e:
            logger.error(f"Failed to load {skin_file}: {e}")
            continue

        skin = skin_raw.to_skin()
        skin_list.append(skin)

        logger.success(f"Loaded {skin.chinese_name} successfully")

    cache_data = [skin.model_dump(mode="json") for skin in skin_list]
    with open(json_dir / "skin.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return skin_list


def load_skin_from_cache() -> list[Skin]:
    """Load a skin from a json file"""
    skin_list = []
    with open(json_dir / "skin.json", "r") as f:
        skin_raw_list = json.load(f)
    for skin_raw in skin_raw_list:
        skin = Skin(**skin_raw)
        skin_list.append(skin)
        logger.success(f"Loaded {skin.chinese_name} successfully")
    return skin_list


def load_skin() -> list[Skin]:
    """Load a skin from cache if exists, otherwise load from P4K"""
    try:
        return load_skin_from_cache()
    except FileNotFoundError:
        return load_skin_from_p4k()


if __name__ == "__main__":
    load_skin()