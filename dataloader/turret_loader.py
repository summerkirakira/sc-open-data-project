from utils.file_manager import sc, get_json_dir
from models.turret import TurretRaw, Turret
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_turret_from_p4k() -> list[Turret]:
    """Load a turret from a P4K file"""
    turret_path = "libs/foundry/records/entities/scitem/ships/turret/*"
    turret_files = sc.datacore.search_filename(turret_path)
    turret_list = []
    for turret_file in turret_files:
        turret_info = sc.datacore.record_to_dict(turret_file)
        try:
            turret_info = load_raw_data_from_dict(turret_info)
            turret_raw = TurretRaw(**turret_info)
        except Exception as e:
            logger.error(f"Failed to load {turret_file}: {e}")
            continue

        turret = turret_raw.to_turret()
        turret_list.append(turret)

        logger.success(f"Loaded {turret.chinese_name} successfully")

    cache_data = [turret.model_dump(mode="json") for turret in turret_list]
    with open(json_dir / "turret.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return turret_list


def load_turret_from_cache() -> list[Turret]:
    """Load a turret from a json file"""
    turret_list = []
    with open(json_dir / "turret.json", "r") as f:
        turret_raw_list = json.load(f)
    for turret_raw in turret_raw_list:
        turret = Turret(**turret_raw)
        turret_list.append(turret)
        logger.success(f"Loaded {turret.chinese_name} successfully")
    return turret_list


def load_turret() -> list[Turret]:
    """Load a turret from cache if exists, otherwise load from P4K"""
    try:
        return load_turret_from_cache()
    except FileNotFoundError:
        return load_turret_from_p4k()


if __name__ == "__main__":
    load_turret()