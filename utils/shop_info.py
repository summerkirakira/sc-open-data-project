from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from pathlib import Path
import json
from utils.localizer import translate_en_to_cn
from loguru import logger

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


shops = load_shops_from_json()


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
    return shop_infos


if __name__ == '__main__':
    print(get_shop_info_by_ref('78e0c040-6668-4b43-a29c-4c47051bba8d'))
    # print(shops)

