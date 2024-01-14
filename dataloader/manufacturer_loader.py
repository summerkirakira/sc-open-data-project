from utils.file_manager import get_zip_info_by_dir, sc
from models.manufacture import ManufactureRaw, Manufacture
from loguru import logger
import json
from utils.file_manager import get_json_dir

json_dir = get_json_dir()


def load_manufacture_from_p4k() -> list[Manufacture]:
    """Load a manufacture from a P4K file"""
    manufacture_path = "libs/foundry/records/scitemmanufacturer/*"
    manufacture_files = sc.datacore.search_filename(manufacture_path)
    manufacture_list = []
    for manufacture_file in manufacture_files:
        manufacture_zip_info = sc.datacore.record_to_dict(manufacture_file)
        try:
            manufacture_raw = ManufactureRaw(**manufacture_zip_info)
        except Exception as e:
            logger.error(f"Failed to load {manufacture_file}: {e}")
            continue
        manufacture = manufacture_raw.to_manufacture()
        manufacture_list.append(manufacture)
        logger.success(f"Loaded {manufacture.chinese_name} successfully")
    cache_data = [manufacture.model_dump(mode="json") for manufacture in manufacture_list]
    with open(json_dir / "manufacture.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return manufacture_list


def load_manufacture_from_cache() -> list[Manufacture]:
    """Load a manufacture from cache"""
    with open(json_dir / "manufacture.json", "r") as f:
        cache_data = json.load(f)
    manufacture_list = []
    for manufacture_data in cache_data:
        manufacture = Manufacture(**manufacture_data)
        manufacture_list.append(manufacture)
        logger.success(f"Loaded {manufacture.chinese_name} successfully")
    return manufacture_list


def load_manufacture() -> list[Manufacture]:
    """Load a manufacture from cache or P4K file"""
    try:
        return load_manufacture_from_cache()
    except:
        return load_manufacture_from_p4k()


if __name__ == "__main__":
    load_manufacture()