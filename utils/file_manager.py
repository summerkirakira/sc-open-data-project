from pathlib import Path
from scdatatools.sc import StarCitizen
from pathlib import Path
from loguru import logger
from .converter import convert_dds_to_png
import json
from zipfile import ZipInfo
from typing import Optional


root_dir = Path(__file__).parent.parent


def get_cache_dir() -> Path:
    """Get the cache directory for starfab

    :return: The cache directory
    """
    return root_dir / "cache"


def get_data_dir(dir_name: str) -> Path:
    """Get the data directory for starfab

    :param dir_name: The name of the directory
    :return: The data directory
    """

    dir_path = root_dir / "data" / dir_name
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True)

    return dir_path


def get_json_dir() -> Path:
    """Get the data directory for starfab

    :param dir_name: The name of the directory
    :return: The data directory
    """

    return get_data_dir("cache")


def load_sc(sc_path: Path) -> StarCitizen:
    """Load a P4K file from the given path"""
    sc = StarCitizen(sc_path)
    logger.debug(f"Loaded {sc_path} successfully")
    return sc


def convert_list_to_dict(list_data: list):
    """Convert a list of dicts to a dict of dicts"""
    new_dict = {}
    for item in list_data:
        for key, value in item.items():
            new_dict[key] = value
    return new_dict


def load_raw_data_from_dict(ship_data: dict) -> dict:
    """Load a P4K file from the given path"""
    ship_data["Components"] = convert_list_to_dict(ship_data["Components"])
    ship_data["StaticEntityClassData"] = convert_list_to_dict(ship_data["StaticEntityClassData"])
    return ship_data


def get_zip_info_ignore_case(zip_file, name):
    """Get the info for a file in a zip file, ignoring case"""
    name = name.replace("\\", "/")
    for info in zip_file.infolist():
        if info.filename.lower() == name.lower():
            return info
    raise KeyError(name)


def get_zip_info_by_dir(zip_file, dir_path: str) -> list[ZipInfo]:
    zip_info_list = []

    for info in zip_file.infolist():
        if info.filename.startswith(dir_path):
            zip_info_list.append(info)
    return zip_info_list

@logger.catch
def extract_image(filename: str, target_path: Path):
    """Extract an image from the given data"""
    if filename.endswith(".tif"):
        filename = filename.replace(".tif", ".dds")
    if not filename.startswith("Data/"):
        filename = "Data/" + filename
    file_info = get_zip_info_ignore_case(sc.p4k, filename)
    sc.p4k.extract(file_info, get_cache_dir())
    convert_dds_to_png(get_cache_dir() / filename, target_path)


def get_manufacturer(ship_item_loader, reference: str):
    for manufacture in ship_item_loader.manufacturer:
        if manufacture.ref == reference:
            return manufacture
    return None


sc_path = Path(r"D:\Programs\RSI\StarCitizen\LIVE")
sc = load_sc(sc_path)


if __name__ == "__main__":
    extract_image("ui/textures/logos/logo_corp_orig_square_white.tif", get_data_dir("images") / "default.png")