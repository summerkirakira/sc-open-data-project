from utils.file_manager import sc, get_json_dir
from models.personal_storage import PersonalStorageRaw, PersonalStorage
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_personal_storage_from_p4k() -> list[PersonalStorage]:
    """Load a personal_storage from a P4K file"""
    personal_storage_path = "libs/foundry/records/entities/scitem/ships/personalstorage/*"
    personal_storage_files = sc.datacore.search_filename(personal_storage_path)
    personal_storage_list = []
    for personal_storage_file in personal_storage_files:
        personal_storage_info = sc.datacore.record_to_dict(personal_storage_file)
        try:
            personal_storage_info = load_raw_data_from_dict(personal_storage_info)
            personal_storage_raw = PersonalStorageRaw(**personal_storage_info)
        except Exception as e:
            logger.error(f"Failed to load {personal_storage_file}: {e}")
            continue

        personal_storage = personal_storage_raw.to_personal_storage()
        personal_storage_list.append(personal_storage)

        logger.success(f"Loaded {personal_storage.chinese_name} successfully")

    cache_data = [personal_storage.model_dump(mode="json") for personal_storage in personal_storage_list]
    with open(json_dir / "personal_storage.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return personal_storage_list


def load_personal_storage_from_cache() -> list[PersonalStorage]:
    """Load a personal_storage from a json file"""
    personal_storage_list = []
    with open(json_dir / "personal_storage.json", "r") as f:
        personal_storage_raw_list = json.load(f)
    for personal_storage_raw in personal_storage_raw_list:
        personal_storage = PersonalStorage(**personal_storage_raw)
        personal_storage_list.append(personal_storage)
        logger.success(f"Loaded {personal_storage.chinese_name} successfully")
    return personal_storage_list


def load_personal_storage() -> list[PersonalStorage]:
    """Load a personal_storage from cache if exists, otherwise load from P4K"""
    try:
        return load_personal_storage_from_cache()
    except FileNotFoundError:
        return load_personal_storage_from_p4k()


if __name__ == "__main__":
    load_personal_storage()
