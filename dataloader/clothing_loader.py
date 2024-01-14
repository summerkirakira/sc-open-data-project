from utils.file_manager import sc, load_raw_data_from_dict, get_json_dir
from models.clothing import ClothingRaw, Clothing
from loguru import logger
import json

json_dir = get_json_dir()


def load_clothing_from_p4k() -> list[Clothing]:
    """Load a clothing from a P4K file"""
    clothing_path = "libs/foundry/records/entities/scitem/characters/human/clothing/*"
    clothing_files = sc.datacore.search_filename(clothing_path)
    clothing_list = []
    for clothing_file in clothing_files:
        clothing_info = sc.datacore.record_to_dict(clothing_file)
        clothing_info = load_raw_data_from_dict(clothing_info)
        try:
            clothing_raw = ClothingRaw(**clothing_info)
        except Exception as e:
            logger.error(f"Failed to load {clothing_file}: {e}")
            continue

        clothing = clothing_raw.to_clothing()
        clothing_list.append(clothing)

        logger.success(f"Loaded {clothing.chinese_name} successfully")

    cache_data = [clothing.model_dump(mode="json") for clothing in clothing_list]
    with open(json_dir / "clothing.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return clothing_list


def load_clothing_from_cache() -> list[Clothing]:
    """Load a clothing from cache"""
    with open(json_dir / "clothing.json", "r") as f:
        cache_data = json.load(f)
    clothing_list = []
    for clothing_data in cache_data:
        clothing = Clothing(**clothing_data)
        clothing_list.append(clothing)
        logger.success(f"Loaded {clothing.chinese_name} successfully")
    return clothing_list


def load_clothing() -> list[Clothing]:
    """Load a clothing from cache or P4K file"""
    try:
        return load_clothing_from_cache()
    except:
        return load_clothing_from_p4k()


if __name__ == "__main__":
    load_clothing()
