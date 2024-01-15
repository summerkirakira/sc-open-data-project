from utils.file_manager import sc, get_json_dir
from models.fuel_intake import FuelIntakeRaw, FuelIntake
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_fuel_intake_from_p4k() -> list[FuelIntake]:
    """Load a fuel_intake from a P4K file"""
    fuel_intake_path = "libs/foundry/records/entities/scitem/ships/fuel_intakes/*"
    fuel_intake_files = sc.datacore.search_filename(fuel_intake_path)
    fuel_intake_list = []
    for fuel_intake_file in fuel_intake_files:
        fuel_intake_info = sc.datacore.record_to_dict(fuel_intake_file)
        try:
            fuel_intake_info = load_raw_data_from_dict(fuel_intake_info)
            fuel_intake_raw = FuelIntakeRaw(**fuel_intake_info)
        except Exception as e:
            logger.error(f"Failed to load {fuel_intake_file}: {e}")
            continue

        fuel_intake = fuel_intake_raw.to_fuel_intake()
        fuel_intake_list.append(fuel_intake)

        logger.success(f"Loaded {fuel_intake.chinese_name} successfully")

    cache_data = [fuel_intake.model_dump(mode="json") for fuel_intake in fuel_intake_list]
    with open(json_dir / "fuel_intake.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return fuel_intake_list


def load_fuel_intake_from_cache() -> list[FuelIntake]:
    """Load a fuel_intake from a json file"""
    fuel_intake_list = []
    with open(json_dir / "fuel_intake.json", "r") as f:
        fuel_intake_raw_list = json.load(f)
    for fuel_intake_raw in fuel_intake_raw_list:
        fuel_intake = FuelIntake(**fuel_intake_raw)
        fuel_intake_list.append(fuel_intake)
        logger.success(f"Loaded {fuel_intake.chinese_name} successfully")
    return fuel_intake_list


def load_fuel_intake() -> list[FuelIntake]:
    """Load a fuel_intake from cache if exists, otherwise load from P4K"""
    try:
        return load_fuel_intake_from_cache()
    except FileNotFoundError:
        return load_fuel_intake_from_p4k()


if __name__ == "__main__":
    load_fuel_intake()