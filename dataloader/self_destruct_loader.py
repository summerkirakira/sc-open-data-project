from utils.file_manager import sc, get_json_dir
from models.self_destruct import SelfDestructRaw, SelfDestruct
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_self_destruct_from_p4k() -> list[SelfDestruct]:
    """Load a self_destruct from a P4K file"""
    self_destruct_path = "libs/foundry/records/entities/scitem/ships/selfdestruct/*"
    self_destruct_files = sc.datacore.search_filename(self_destruct_path)
    self_destruct_list = []
    for self_destruct_file in self_destruct_files:
        self_destruct_info = sc.datacore.record_to_dict(self_destruct_file)
        try:
            self_destruct_info = load_raw_data_from_dict(self_destruct_info)
            self_destruct_raw = SelfDestructRaw(**self_destruct_info)
        except Exception as e:
            logger.error(f"Failed to load {self_destruct_file}: {e}")
            continue

        self_destruct = self_destruct_raw.to_self_destruct()
        self_destruct_list.append(self_destruct)

        logger.success(f"Loaded {self_destruct.chinese_name} successfully")

    cache_data = [self_destruct.model_dump(mode="json") for self_destruct in self_destruct_list]
    with open(json_dir / "self_destruct.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return self_destruct_list


def load_self_destruct_from_cache() -> list[SelfDestruct]:
    """Load a self_destruct from a json file"""
    self_destruct_list = []
    with open(json_dir / "self_destruct.json", "r") as f:
        self_destruct_raw_list = json.load(f)
    for self_destruct_raw in self_destruct_raw_list:
        self_destruct = SelfDestruct(**self_destruct_raw)
        self_destruct_list.append(self_destruct)
        logger.success(f"Loaded {self_destruct.chinese_name} successfully")
    return self_destruct_list


def load_self_destruct() -> list[SelfDestruct]:
    """Load a self_destruct from cache if exists, otherwise load from P4K"""
    try:
        return load_self_destruct_from_cache()
    except FileNotFoundError:
        return load_self_destruct_from_p4k()


if __name__ == "__main__":
    load_self_destruct()
