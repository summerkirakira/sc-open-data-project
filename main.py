from dataloader.ship_item_loader import ShipItemLoader
from dataloader.ship_loader import load_ship
from utils.extract_ship_thumbnail import extract_ship_thumbnail
from utils.ship_manager import remove_duplicate_ship
import json


def main():
    ship_item_loader = ShipItemLoader()
    ships = load_ship(ship_item_loader)
    new_ships = remove_duplicate_ship(ships)
    ship_list = [ship.to_dict() for ship in new_ships]
    with open("ship.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(ship_list, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()

