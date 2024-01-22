from models.ship import Ship
from pathlib import Path
from PIL import Image
from dataloader.ship_item_loader import ShipItemLoader
from .file_manager import get_manufacturer
import random

import shutil

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


manufacturer_path = Path(__file__).parent.parent / "data" / "manufacture"

ship_thumbnail_path = Path(__file__).parent.parent / "data" / "ship_thumb"

ship_render_path = Path(r"C:\Users\Summerkirakira\PycharmProjects\sc-ship-information-picture\ship-render")


def extract_thumbnail_from_ship_image(ship: Ship):
    """Extract ship thumbnail from ship image"""
    ship_image_path = ship_render_path / f"{ship.ship_name_binding.ship_pic_name}.png"
    ship_thumbnail = Image.open(ship_image_path)
    ship_thumbnail.thumbnail((256, 256))
    ship_thumbnail.save(ship_thumbnail_path / f"{ship.ship_name_binding.ship_pic_name}.thumb.png")


def copy_ship_thumbnail_from_manufacturer(ship: Ship, ship_item_loader: ShipItemLoader):
    paint = random.choice(ship.paints)
    manufacturer = get_manufacturer(ship_item_loader, paint.manufacturer)
    if manufacturer is None:
        raise Exception(f"Cannot find manufacturer {paint.manufacturer}")
    manufacturer_thumbnail_path = manufacturer_path / manufacturer.logo.logo
    shutil.copy(manufacturer_thumbnail_path, ship_thumbnail_path / f"{ship.ship_name_binding.ship_pic_name}.thumb.png")


def extract_ship_thumbnail(ship: Ship, ship_item_loader: ShipItemLoader):
    """Extract ship thumbnail from Skin"""

    if ship.ship_name_binding.ship_pic_name == '""':
        return
    if ship.ship_name_binding.ship_pic_name == '':
        return

    if len(ship.paints) == 0:
        extract_thumbnail_from_ship_image(ship)
    else:
        try:
            copy_ship_thumbnail_from_manufacturer(ship, ship_item_loader)
        except Exception as e:
            print(e)
            extract_thumbnail_from_ship_image(ship)
    print(f"Extracted {ship.ship_name_binding.ship_pic_name}.thumb.png")