from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from pathlib import Path
import json
from utils.localizer import translate_en_to_cn
from loguru import logger
from utils.file_manager import sc, get_zip_info_by_dir

current_dir = Path(__file__).parent

shop_path_data = current_dir / 'data' / 'shop_info'


class Shop(BaseModel):
    class Data(BaseModel):
        class InventoryItem(BaseModel):
            localName: str
            basePrice: int
            price: int
            ref: str

        name: str
        location: str
        chinese_name: Optional[str] = None
        chinese_location: Optional[str] = None
        inventory: List[InventoryItem]
        rental: bool

    calculatorType: str
    data: Data


class ShopNameBinding(BaseModel):
    filename: str
    name: str
    chinese_shop_name: Optional[str] = None
    location: str
    chinese_location: Optional[str] = None


class ShopInv(BaseModel):
    class CollectionType(BaseModel):
        class InventoryItem(BaseModel):
            class ID(BaseModel):
                ID: List[str]

            ID: ID
            BuyPrice: float
            SellPrice: float
            CurrentInventory: float
            MaxInventory: float

        Inventory: List[InventoryItem]

        def to_shop(self, name_binding: ShopNameBinding) -> Shop:
            return Shop(
                calculatorType="Shop",
                data=Shop.Data(
                    name=name_binding.name,
                    location=name_binding.location,
                    chinese_name=translate_en_to_cn(name_binding.name),
                    chinese_location=translate_en_to_cn(name_binding.location),
                    inventory=[Shop.Data.InventoryItem(
                        localName=item.ID.ID[0],
                        basePrice=int(item.BuyPrice),
                        price=int(item.BuyPrice),
                        ref=item.ID.ID[0]
                    ) for item in self.Inventory],
                    rental=False
                )
            )


    Collection: CollectionType

    def to_shop(self, name_binding: ShopNameBinding) -> Shop:
        return Shop(
            calculatorType="Shop",
            data=Shop.Data(
                name=name_binding.name,
                location=name_binding.location,
                chinese_name=translate_en_to_cn(name_binding.name),
                chinese_location=translate_en_to_cn(name_binding.location),
                inventory=[Shop.Data.InventoryItem(
                    localName=item.ID.ID[0],
                    basePrice=int(item.BuyPrice),
                    price=int(item.BuyPrice),
                    ref=item.ID.ID[0]
                ) for item in self.Collection.Inventory],
                rental=False
            )
        )


class ShopInfo(BaseModel):
    name: str
    location: str
    chinese_name: Optional[str] = None
    chinese_location: Optional[str] = None
    base_price: int
    price: int





def load_shops_from_json() -> list[Shop]:
    shops = []
    with (shop_path_data / 'shop.json').open('r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    for shop in data:
        shop_info = Shop(**shop)
        shop_info.data.chinese_name = translate_en_to_cn(shop_info.data.name)
        shop_info.data.chinese_location = translate_en_to_cn(shop_info.data.location)
        shops.append(shop_info)
        # print(shop_info.data.chinese_name)
        # print(shop_info.data.chinese_location)
    logger.success(f'Loaded {len(shops)} shops from shop.json')
    return shops


def load_shop_names_from_json() -> list[ShopNameBinding]:
    shop_names = []
    with (shop_path_data / 'shop_name_binding.json').open('r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    for shop in data:
        shop_info = ShopNameBinding(**shop)
        shop_info.chinese_shop_name = translate_en_to_cn(shop_info.name)
        shop_info.chinese_location = translate_en_to_cn(shop_info.location)
        shop_names.append(shop_info)
    logger.success(f'Loaded {len(shop_names)} shop names from shop_name_binding.json')
    return shop_names


def save_shop_names_to_json(shop_names: list[ShopNameBinding]):
    with (shop_path_data / 'shop_name_binding.json').open('w', encoding='utf-8', errors='ignore') as f:
        json.dump([shop_name.model_dump(mode="json") for shop_name in shop_names], f, ensure_ascii=False, indent=4)
    logger.success(f'Saved {len(shop_names)} shop names to shop_name_binding.json')


shops = load_shops_from_json()
shop_names = load_shop_names_from_json()


def get_shop_info_by_ref(ref: str) -> list[ShopInfo]:
    shop_infos = []
    for shop in shops:
        for item in shop.data.inventory:
            if item.ref == ref:
                shop_info = ShopInfo(
                    name=shop.data.name,
                    location=shop.data.location,
                    chinese_name=shop.data.chinese_name,
                    chinese_location=shop.data.chinese_location,
                    base_price=item.basePrice,
                    price=item.price
                )
                shop_infos.append(shop_info)
    if len(shop_infos) != 0:
        return shop_infos

    for shop in game_shops:
        for item in shop.data.inventory:
            if item.ref == ref:
                shop_info = ShopInfo(
                    name=shop.data.name,
                    location=shop.data.location,
                    chinese_name=shop.data.chinese_name,
                    chinese_location=shop.data.chinese_location,
                    base_price=item.basePrice,
                    price=item.price
                )
                shop_infos.append(shop_info)
    return shop_infos


def get_name_binding_by_filename(ref: str) -> Optional[ShopNameBinding]:
    for shop in shop_names:
        if shop.filename == ref:
            return shop
    return None


game_shops: list[Shop] = []


def load_game_shop():
    json_path = "Data/Scripts/ShopInventories/"
    game_shop_jsons = []
    for zip_info in get_zip_info_by_dir(sc.p4k, json_path):
        if "Anniversary" in zip_info.filename:
            continue
        name_binding = get_name_binding_by_filename(zip_info.filename.split('/')[-1].split('.')[0])
        if name_binding is None:
            # logger.warning(f'Cannot find name binding for {zip_info.filename}')
            print(zip_info.filename)
            name = input('Please input name: ')
            location = input('Please input location: ')

            shop_names.append(
                ShopNameBinding(
                    filename=zip_info.filename.split('/')[-1].split('.')[0],
                    name=name,
                    location=location
                )
            )
            save_shop_names_to_json(shop_names)
            continue

        if name_binding.location == 'Levski':
            continue

        with sc.p4k.open(zip_info.filename) as f:
            data = json.load(f)
        if 'Collection' in data:
            data = ShopInv(**data)
        else:
            data = ShopInv.CollectionType(**data)
        try:
            game_shops.append(data.to_shop(name_binding))
        except Exception as e:
            logger.error(f'Error when loading {zip_info.filename}')
            logger.error(e)
            continue
    return game_shops


load_game_shop()

if __name__ == '__main__':
    print(get_shop_info_by_ref("b62224ba-5c56-4306-857a-70de7d570767"))
    # print(shops)

