from utils.file_manager import sc, get_json_dir
from models.thruster import ThrusterRaw, Thruster
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_thruster_from_p4k() -> list[Thruster]:
    """Load a thruster from a P4K file"""
    thruster_path = "libs/foundry/records/entities/scitem/ships/thrusters/*"
    thruster_files = sc.datacore.search_filename(thruster_path)
    thruster_list = []
    for thruster_file in thruster_files:
        thruster_info = sc.datacore.record_to_dict(thruster_file)
        try:
            thruster_info = load_raw_data_from_dict(thruster_info)
            thruster_raw = ThrusterRaw(**thruster_info)
        except Exception as e:
            logger.error(f"Failed to load {thruster_file}: {e}")
            continue

        thruster = thruster_raw.to_thruster()
        thruster_list.append(thruster)

        logger.success(f"Loaded {thruster.chinese_name} successfully")

    cache_data = [thruster.model_dump(mode="json") for thruster in thruster_list]
    with open(json_dir / "thruster.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return thruster_list


def load_thruster_from_cache() -> list[Thruster]:
    """Load a thruster from a json file"""
    thruster_list = []
    with open(json_dir / "thruster.json", "r") as f:
        thruster_raw_list = json.load(f)
    for thruster_raw in thruster_raw_list:
        thruster = Thruster(**thruster_raw)
        thruster_list.append(thruster)
        logger.success(f"Loaded {thruster.chinese_name} successfully")
    return thruster_list


def load_thruster() -> list[Thruster]:
    """Load a thruster from cache if exists, otherwise load from P4K"""
    try:
        return load_thruster_from_cache()
    except FileNotFoundError:
        return load_thruster_from_p4k()


if __name__ == "__main__":
    load_thruster()