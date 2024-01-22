from utils.file_manager import sc, get_json_dir
from models.sub_cargo_grid import SubCargoGridRaw, SubCargoGrid
from loguru import logger
import json


json_dir = get_json_dir()


def load_sub_cargo_grid_from_p4k() -> list[SubCargoGrid]:
    """Load a sub_cargo_grid from a P4K file"""
    sub_cargo_grid_path = "libs/foundry/records/inventorycontainers/ships/*"
    sub_cargo_grid_files = sc.datacore.search_filename(sub_cargo_grid_path)
    sub_cargo_grid_list = []
    sub_cargo_grid_path_2 = "libs/foundry/records/inventorycontainers/cargogrid/*"
    sub_cargo_grid_files_2 = sc.datacore.search_filename(sub_cargo_grid_path_2)
    sub_cargo_grid_files.extend(sub_cargo_grid_files_2)
    for sub_cargo_grid_file in sub_cargo_grid_files:
        sub_cargo_grid_info = sc.datacore.record_to_dict(sub_cargo_grid_file)
        try:
            sub_cargo_grid_raw = SubCargoGridRaw(**sub_cargo_grid_info)
        except Exception as e:
            logger.error(f"Failed to load {sub_cargo_grid_file}: {e}")
            continue

        sub_cargo_grid = sub_cargo_grid_raw.to_sub_cargo_grid()
        sub_cargo_grid_list.append(sub_cargo_grid)

        logger.success(f"Loaded {sub_cargo_grid.ref} successfully")

    cache_data = [sub_cargo_grid.model_dump(mode="json") for sub_cargo_grid in sub_cargo_grid_list]
    with open(json_dir / "sub_cargo_grid.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return sub_cargo_grid_list


def load_sub_cargo_grid_from_cache() -> list[SubCargoGrid]:
    """Load a sub_cargo_grid from a json file"""
    sub_cargo_grid_list = []
    with open(json_dir / "sub_cargo_grid.json", "r") as f:
        sub_cargo_grid_raw_list = json.load(f)
    for sub_cargo_grid_raw in sub_cargo_grid_raw_list:
        sub_cargo_grid = SubCargoGrid(**sub_cargo_grid_raw)
        sub_cargo_grid_list.append(sub_cargo_grid)
        logger.success(f"Loaded {sub_cargo_grid.ref} successfully")
    return sub_cargo_grid_list


def load_sub_cargo_grid() -> list[SubCargoGrid]:
    """Load a sub_cargo_grid from cache if exists, otherwise load from P4K"""
    try:
        return load_sub_cargo_grid_from_cache()
    except FileNotFoundError:
        return load_sub_cargo_grid_from_p4k()


if __name__ == "__main__":
    load_sub_cargo_grid()