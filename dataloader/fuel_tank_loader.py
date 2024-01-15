from utils.file_manager import sc, get_json_dir
from models.fuel_tank import FuelTankRaw, FuelTank
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_fuel_tank_from_p4k() -> list[FuelTank]:
    """Load a fuel_tank from a P4K file"""
    fuel_tank_path = "libs/foundry/records/entities/scitem/ships/fueltanks/*"
    fuel_tank_files = sc.datacore.search_filename(fuel_tank_path)
    fuel_tank_list = []
    for fuel_tank_file in fuel_tank_files:
        fuel_tank_info = sc.datacore.record_to_dict(fuel_tank_file)
        try:
            fuel_tank_info = load_raw_data_from_dict(fuel_tank_info)
            fuel_tank_raw = FuelTankRaw(**fuel_tank_info)
        except Exception as e:
            logger.error(f"Failed to load {fuel_tank_file}: {e}")
            continue

        fuel_tank = fuel_tank_raw.to_fuel_tank()
        fuel_tank_list.append(fuel_tank)

        logger.success(f"Loaded {fuel_tank.chinese_name} successfully")

    cache_data = [fuel_tank.model_dump(mode="json") for fuel_tank in fuel_tank_list]
    with open(json_dir / "fuel_tank.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return fuel_tank_list


def load_fuel_tank_from_cache() -> list[FuelTank]:
    """Load a fuel_tank from a json file"""
    fuel_tank_list = []
    with open(json_dir / "fuel_tank.json", "r") as f:
        fuel_tank_raw_list = json.load(f)
    for fuel_tank_raw in fuel_tank_raw_list:
        fuel_tank = FuelTank(**fuel_tank_raw)
        fuel_tank_list.append(fuel_tank)
        logger.success(f"Loaded {fuel_tank.chinese_name} successfully")
    return fuel_tank_list


def load_fuel_tank() -> list[FuelTank]:
    """Load a fuel_tank from cache if exists, otherwise load from P4K"""
    try:
        return load_fuel_tank_from_cache()
    except FileNotFoundError:
        return load_fuel_tank_from_p4k()


if __name__ == "__main__":
    load_fuel_tank()