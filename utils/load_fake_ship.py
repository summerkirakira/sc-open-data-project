from pathlib import Path
from models.fake_ship import FakeShip
from dataloader.manufacturer_loader import load_manufacture
import json
import uuid
from ship_alias import ShipAlis, get_ship_alias_by_name

current_dir = Path(__file__).parent

fake_ship_path = current_dir / 'data' / 'fake_ship' / 'fake_ship.json'


name_map = {
    '德雷克行星系': '德雷克行星际',
    '罗伯特太空工业': '罗伯茨太空工业',
    '武藏星航': '武藏工业与星航株式会社',
}


def get_fake_ships() -> list[FakeShip]:
    with fake_ship_path.open('r', encoding='utf-8', errors='ignore') as f:
        data_list = json.loads(f.read())
    return [FakeShip(**data) for data in data_list]


def main():
    fake_ships = get_fake_ships()
    manufactures = load_manufacture()
    for fake_ship in fake_ships:

        if fake_ship.manufactory_chinese_name in name_map:
            fake_ship.manufactory_chinese_name = name_map[fake_ship.manufactory_chinese_name]

        for manufacture in manufactures:
            if fake_ship.manufactory_chinese_name in manufacture.chinese_name:
                fake_ship.manufactory_logo_path = manufacture.logo.logo_full_color
                fake_ship.manufactory_logo_path_2 = manufacture.logo.logo
                fake_ship.manufactory_chinese_name = manufacture.chinese_name
        # fake_ship.ref = str(uuid.uuid4())
        if fake_ship.ship_alias is None:
            fake_ship.ship_alias = get_ship_alias_by_name(fake_ship.name)
        if fake_ship.ship_alias is None:
            print(f'fake_ship {fake_ship.name} has no ship_alias')
            raise Exception

    with fake_ship_path.open('w', encoding='utf-8', errors='ignore') as f:
        f.write(json.dumps([fake_ship.model_dump() for fake_ship in fake_ships], indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()



