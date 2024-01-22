from utils.file_manager import sc, get_json_dir
from models.cap_assignment import CapAssignmentRaw, CapAssignment
from loguru import logger
import json


json_dir = get_json_dir()


def load_cap_assignment_from_p4k() -> list[CapAssignment]:
    """Load a cap_assignment from a P4K file"""
    cap_assignment_path = "libs/foundry/records/capacitorassignment/*"
    cap_assignment_files = sc.datacore.search_filename(cap_assignment_path)
    cap_assignment_list = []
    for cap_assignment_file in cap_assignment_files:
        cap_assignment_info = sc.datacore.record_to_dict(cap_assignment_file)
        try:
            cap_assignment_raw = CapAssignmentRaw(**cap_assignment_info)
        except Exception as e:
            logger.error(f"Failed to load {cap_assignment_file}: {e}")
            continue

        cap_assignment_list.append(cap_assignment_raw.to_cap_assignment())

        logger.success(f"Loaded {cap_assignment_raw.ref} successfully")

    cache_data = [cap_assignment.model_dump(mode="json") for cap_assignment in cap_assignment_list]
    with open(json_dir / "cap_assignment.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return cap_assignment_list


def load_cap_assignment_from_cache() -> list[CapAssignment]:
    """Load a cap_assignment from a json file"""
    cap_assignment_list = []
    with open(json_dir / "cap_assignment.json", "r") as f:
        cap_assignment_raw_list = json.load(f)
    for cap_assignment_raw in cap_assignment_raw_list:
        cap_assignment = CapAssignment(**cap_assignment_raw)
        cap_assignment_list.append(cap_assignment)
        logger.success(f"Loaded {cap_assignment.ref} successfully")
    return cap_assignment_list


def load_cap_assignment() -> list[CapAssignment]:
    """Load a cap_assignment from cache if exists, otherwise load from P4K"""
    try:
        return load_cap_assignment_from_cache()
    except FileNotFoundError:
        return load_cap_assignment_from_p4k()


if __name__ == "__main__":
    load_cap_assignment()
