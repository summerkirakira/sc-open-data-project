from utils.file_manager import sc, get_json_dir
from models.ship import ShipRaw, Ship
from utils.file_manager import load_raw_data_from_dict
from .ship_item_loader import ShipItemLoader
from loguru import logger
import json


json_dir = get_json_dir()


def load_ship_from_p4k(ship_item_loader: ShipItemLoader) -> list[Ship]:
    """Load a ship from a P4K file"""
    ship_path = "libs/foundry/records/entities/spaceships/*"
    ship_files = sc.datacore.search_filename(ship_path)
    ship_list = []

    for ship_file in ship_files:

        ship_info = sc.datacore.record_to_dict(ship_file)
        try:
            ship_info = load_raw_data_from_dict(ship_info)
            ship_raw = ShipRaw(**ship_info)
        except Exception as e:
            logger.error(f"Failed to load {ship_file}: {e}")
            continue
        try:
            ship = ship_raw.to_ship(ship_item_loader)
        except Exception as e:
            logger.error(f"Failed to load {ship_file}: {e}")
            raise e
        ship_list.append(ship)

        logger.success(f"Loaded {ship.chinese_name} successfully")

    cache_data = [ship.to_dict() for ship in ship_list]
    with open(json_dir / "ship.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return ship_list


def load_ship_from_cache(item_loader: ShipItemLoader) -> list[Ship]:
    """Load a ship from a json file"""
    ship_list = []
    with open(json_dir / "ship.json", "r") as f:
        ship_raw_list = json.load(f)
    for ship_raw in ship_raw_list:
        ship = Ship.load_from_cache(loader=item_loader, data=ship_raw)
        ship_list.append(ship)
        logger.success(f"Loaded {ship.chinese_name} successfully")
    return ship_list


def load_ship(item_loader) -> list[Ship]:
    """Load a ship from cache if exists, otherwise load from P4K"""
    try:
        return load_ship_from_cache(item_loader)
    except FileNotFoundError:
        return load_ship_from_p4k(item_loader)


if __name__ == "__main__":
    item_loader = ShipItemLoader()
    load_ship(item_loader)