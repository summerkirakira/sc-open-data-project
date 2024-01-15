from utils.file_manager import sc, get_json_dir
from models.power_plant import PowerPlantRaw, PowerPlant
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_power_plant_from_p4k() -> list[PowerPlant]:
    """Load a power_plant from a P4K file"""
    power_plant_path = "libs/foundry/records/entities/scitem/ships/powerplant/*"
    power_plant_files = sc.datacore.search_filename(power_plant_path)
    power_plant_list = []
    for power_plant_file in power_plant_files:
        power_plant_info = sc.datacore.record_to_dict(power_plant_file)
        try:
            power_plant_info = load_raw_data_from_dict(power_plant_info)
            power_plant_raw = PowerPlantRaw(**power_plant_info)
        except Exception as e:
            logger.error(f"Failed to load {power_plant_file}: {e}")
            continue

        power_plant = power_plant_raw.to_power_plant()
        power_plant_list.append(power_plant)

        logger.success(f"Loaded {power_plant.chinese_name} successfully")

    cache_data = [power_plant.model_dump(mode="json") for power_plant in power_plant_list]
    with open(json_dir / "power_plant.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return power_plant_list


def load_power_plant_from_cache() -> list[PowerPlant]:
    """Load a power_plant from a json file"""
    power_plant_list = []
    with open(json_dir / "power_plant.json", "r") as f:
        power_plant_raw_list = json.load(f)
    for power_plant_raw in power_plant_raw_list:
        power_plant = PowerPlant(**power_plant_raw)
        power_plant_list.append(power_plant)
        logger.success(f"Loaded {power_plant.chinese_name} successfully")
    return power_plant_list


def load_power_plant() -> list[PowerPlant]:
    """Load a power_plant from cache if exists, otherwise load from P4K"""
    try:
        return load_power_plant_from_cache()
    except FileNotFoundError:
        return load_power_plant_from_p4k()


if __name__ == "__main__":
    load_power_plant()