from pydantic import BaseModel
from pathlib import Path
from typing import Optional
import json
from pathlib import Path

current_dir = Path(__file__).parent

global_path_data = current_dir / 'data' / 'ship_alias'


class ShipAlis(BaseModel):

    class Sku(BaseModel):
        title: str
        price: int

    id: int
    name: str
    alias: list[str]

    skus: list[Sku]


class ShipNameBinding(BaseModel):
    id: int
    ship_name: str
    ship_pic_name: str


def get_ship_alias() -> list[ShipAlis]:
    with (global_path_data / 'ship_alias.json').open('r', encoding='utf-8', errors='ignore') as f:
        data = json.loads(f.read())
    return [ShipAlis(**item) for item in data]


def get_ship_alias_by_id(alias_id: int) -> Optional[ShipAlis]:
    ship_alias = get_ship_alias()
    for item in ship_alias:
        if item.id == alias_id:
            return item


def get_ship_name_binding() -> list[ShipNameBinding]:
    with (global_path_data / 'ship_name_binding.json').open('r', encoding='utf-8', errors='ignore') as f:
        data = json.loads(f.read())
    return [ShipNameBinding(**item) for item in data]


def save_ship_name_binding(data: list[ShipNameBinding]):
    with (global_path_data / 'ship_name_binding.json').open('w', encoding='utf-8', errors='ignore') as f:
        f.write(json.dumps([item.model_dump() for item in data], indent=4, ensure_ascii=False))


def get_ship_name_binding_by_name(name: str) -> Optional[ShipNameBinding]:
    ship_name_binding = get_ship_name_binding()
    for item in ship_name_binding:
        if item.ship_name == name:
            return item
    return None


# def update_ship_name_binding(ships: list[Ship]):
#     name_set = set([ship.name for ship in ships])
#     ship_name_binding_list = get_ship_name_binding()
#
#     render_path = Path(r"C:\Users\Summerkirakira\PycharmProjects\sc-ship-information-picture\ship-render")
#
#     file_list = [file.stem for file in render_path.iterdir()]
#
#     ship_id = None
#     ship_pic_name = None
#
#     for name in name_set:
#
#         ship_name = name.replace(name.split(' ')[0], '').strip()
#         for alias in get_ship_alias():
#             if ship_name == alias.name or name in alias.alias:
#                 ship_id = alias.id
#                 print(f'{name}的id为{ship_id} / {alias.name}')
#
#         for file_name in file_list:
#             if ship_name.lower() == file_name.lower():
#                 ship_pic_name = file_name
#                 print(f'{name}的图片名称为{ship_pic_name}')
#
#         ship_name_binding = get_ship_name_binding_by_name(name)
#         if ship_name_binding is None:
#             if ship_id is None:
#                 ship_id = int(input(f'请输入id: {name} '))
#             if ship_pic_name is None:
#                 ship_pic_name = input(f'请输入{name}的图片名称:')
#             ship_name_binding_list.append(ShipNameBinding(id=ship_id, ship_name=name, ship_pic_name=ship_pic_name))
#             ship_id = None
#             ship_pic_name = None
#         save_ship_name_binding(ship_name_binding_list)

