from utils.file_manager import sc, get_json_dir
from models.cargo_grid import CargoGridRaw, CargoGrid
from sub_cargo_grid_loader import load_sub_cargo_grid
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_cargo_grid_from_p4k() -> list[CargoGrid]:
    """Load a cargo_grid from a P4K file"""

    sub_cargo_grids = load_sub_cargo_grid()

    cargo_grid_path = "libs/foundry/records/entities/scitem/ships/cargogrid/*"
    cargo_grid_files = sc.datacore.search_filename(cargo_grid_path)
    cargo_grid_list = []
    for cargo_grid_file in cargo_grid_files:
        cargo_grid_info = sc.datacore.record_to_dict(cargo_grid_file)
        try:
            cargo_grid_info = load_raw_data_from_dict(cargo_grid_info)
            cargo_grid_raw = CargoGridRaw(**cargo_grid_info)
        except Exception as e:
            logger.error(f"Failed to load {cargo_grid_file}: {e}")
            continue

        cargo_grid = cargo_grid_raw.to_cargo_grid(sub_cargo_grids)
        cargo_grid_list.append(cargo_grid)

        logger.success(f"Loaded {cargo_grid.chinese_name} successfully")

    cache_data = [cargo_grid.model_dump(mode="json") for cargo_grid in cargo_grid_list]
    with open(json_dir / "cargo_grid.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return cargo_grid_list


def load_cargo_grid_from_cache() -> list[CargoGrid]:
    """Load a cargo_grid from a json file"""
    cargo_grid_list = []
    with open(json_dir / "cargo_grid.json", "r") as f:
        cargo_grid_raw_list = json.load(f)
    for cargo_grid_raw in cargo_grid_raw_list:
        cargo_grid = CargoGrid(**cargo_grid_raw)
        cargo_grid_list.append(cargo_grid)
        logger.success(f"Loaded {cargo_grid.chinese_name} successfully")
    return cargo_grid_list


def load_cargo_grid() -> list[CargoGrid]:
    """Load a cargo_grid from cache if exists, otherwise load from P4K"""
    try:
        return load_cargo_grid_from_cache()
    except FileNotFoundError:
        return load_cargo_grid_from_p4k()


if __name__ == "__main__":
    load_cargo_grid()