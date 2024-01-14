from utils.file_manager import sc, load_raw_data_from_dict, get_json_dir
from models.fps_magazine import FPSMagazineRaw, FPSMagazine
from fps_ammo_loader import load_fps_ammo
from models.fps_ammo import FPSAmmo
from loguru import logger
import json

json_dir = get_json_dir()


def load_fps_magazine_from_p4k() -> list[FPSMagazine]:
    """Load a fps_magazine from a P4K file"""
    fps_magazine_path = "libs/foundry/records/entities/scitem/weapons/magazines/*"
    fps_magazine_files = sc.datacore.search_filename(fps_magazine_path)
    fps_magazine_list = []
    ammo_list = load_fps_ammo()
    for fps_magazine_file in fps_magazine_files:
        fps_magazine_info = sc.datacore.record_to_dict(fps_magazine_file)
        fps_magazine_info = load_raw_data_from_dict(fps_magazine_info)
        try:
            fps_magazine_raw = FPSMagazineRaw(**fps_magazine_info)
        except Exception as e:
            logger.error(f"Failed to load {fps_magazine_file}: {e}")
            continue

        fps_magazine = fps_magazine_raw.to_magazine(ammo_list)
        if fps_magazine is None:
            continue
        fps_magazine_list.append(fps_magazine)

        logger.success(f"Loaded {fps_magazine.chinese_name} successfully")

    cache_data = [fps_magazine.model_dump(mode="json") for fps_magazine in fps_magazine_list]
    with open(json_dir / "fps_magazine.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return fps_magazine_list


def load_fps_magazine_from_cache() -> list[FPSMagazine]:
    """Load a fps_magazine from a json file"""
    fps_magazine_list = []
    with open(json_dir / "fps_magazine.json", "r") as f:
        fps_magazine_raw_list = json.load(f)
    for fps_magazine_raw in fps_magazine_raw_list:
        fps_magazine = FPSMagazine(**fps_magazine_raw)
        fps_magazine_list.append(fps_magazine)
        logger.success(f"Loaded {fps_magazine.chinese_name} successfully")
    return fps_magazine_list


def load_fps_magazine() -> list[FPSMagazine]:
    """Load a fps_magazine from cache if exists, otherwise load from P4K"""
    try:
        return load_fps_magazine_from_cache()
    except FileNotFoundError:
        return load_fps_magazine_from_p4k()


if __name__ == "__main__":
    load_fps_magazine()