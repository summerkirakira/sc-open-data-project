from utils.file_manager import sc, get_json_dir
from models.cooler import CoolerRaw, Cooler
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_cooler_from_p4k() -> list[Cooler]:
    """Load a cooler from a P4K file"""
    cooler_path = "libs/foundry/records/entities/scitem/ships/cooler/*"
    cooler_files = sc.datacore.search_filename(cooler_path)
    cooler_list = []
    for cooler_file in cooler_files:
        cooler_info = sc.datacore.record_to_dict(cooler_file)
        try:
            cooler_info = load_raw_data_from_dict(cooler_info)
            cooler_raw = CoolerRaw(**cooler_info)
        except Exception as e:
            logger.error(f"Failed to load {cooler_file}: {e}")
            continue

        cooler = cooler_raw.to_cooler()
        cooler_list.append(cooler)

        logger.success(f"Loaded {cooler.chinese_name} successfully")

    cache_data = [cooler.model_dump(mode="json") for cooler in cooler_list]
    with open(json_dir / "cooler.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return cooler_list


def load_cooler_from_cache() -> list[Cooler]:
    """Load a cooler from a json file"""
    cooler_list = []
    with open(json_dir / "cooler.json", "r") as f:
        cooler_raw_list = json.load(f)
    for cooler_raw in cooler_raw_list:
        cooler = Cooler(**cooler_raw)
        cooler_list.append(cooler)
        logger.success(f"Loaded {cooler.chinese_name} successfully")
    return cooler_list


def load_cooler() -> list[Cooler]:
    """Load a cooler from cache if exists, otherwise load from P4K"""
    try:
        return load_cooler_from_cache()
    except FileNotFoundError:
        return load_cooler_from_p4k()


if __name__ == "__main__":
    load_cooler()