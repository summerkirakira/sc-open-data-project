from utils.file_manager import sc, get_json_dir
from models.controller import ControllerRaw, Controller
from utils.file_manager import load_raw_data_from_dict
from .cap_assignment_loader import load_cap_assignment
from loguru import logger
import json


json_dir = get_json_dir()


def load_controller_from_p4k() -> list[Controller]:
    """Load a controller from a P4K file"""
    controller_path = "libs/foundry/records/entities/scitem/ships/controller/*"
    controller_files = sc.datacore.search_filename(controller_path)
    controller_list = []
    cap_assignment_list = load_cap_assignment()
    for controller_file in controller_files:
        controller_info = sc.datacore.record_to_dict(controller_file)
        try:
            controller_info = load_raw_data_from_dict(controller_info)
            controller_raw = ControllerRaw(**controller_info)
        except Exception as e:
            logger.error(f"Failed to load {controller_file}: {e}")
            continue


        controller = controller_raw.to_controller(cap_assignment_list)
        controller_list.append(controller)

        logger.success(f"Loaded {controller.chinese_name} successfully")

    cache_data = [controller.model_dump(mode="json") for controller in controller_list]
    with open(json_dir / "controller.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return controller_list


def load_controller_from_cache() -> list[Controller]:
    """Load a controller from a json file"""
    controller_list = []
    with open(json_dir / "controller.json", "r") as f:
        controller_raw_list = json.load(f)
    for controller_raw in controller_raw_list:
        controller = Controller(**controller_raw)
        controller_list.append(controller)
        logger.success(f"Loaded {controller.chinese_name} successfully")
    return controller_list


def load_controller() -> list[Controller]:
    """Load a controller from cache if exists, otherwise load from P4K"""
    try:
        return load_controller_from_cache()
    except FileNotFoundError:
        return load_controller_from_p4k()


if __name__ == "__main__":
    load_controller()
