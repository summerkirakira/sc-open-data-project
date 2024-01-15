from utils.file_manager import sc, get_json_dir
from models.qd import QuantumDriveRaw, QuantumDrive
from utils.file_manager import load_raw_data_from_dict
from loguru import logger
import json


json_dir = get_json_dir()


def load_qd_from_p4k() -> list[QuantumDrive]:
    """Load a qd from a P4K file"""
    qd_path = "libs/foundry/records/entities/scitem/ships/quantumdrive/*"
    qd_files = sc.datacore.search_filename(qd_path)
    qd_list = []
    for qd_file in qd_files:
        qd_info = sc.datacore.record_to_dict(qd_file)
        try:
            qd_info = load_raw_data_from_dict(qd_info)
            qd_raw = QuantumDriveRaw(**qd_info)
        except Exception as e:
            logger.error(f"Failed to load {qd_file}: {e}")
            continue

        qd = qd_raw.to_quantum_drive()
        qd_list.append(qd)

        logger.success(f"Loaded {qd.chinese_name} successfully")

    cache_data = [qd.model_dump(mode="json") for qd in qd_list]
    with open(json_dir / "qd.json", "w") as f:
        json.dump(cache_data, f, indent=4, ensure_ascii=False)
    return qd_list


def load_qd_from_cache() -> list[QuantumDrive]:
    """Load a qd from a json file"""
    qd_list = []
    with open(json_dir / "qd.json", "r") as f:
        qd_raw_list = json.load(f)
    for qd_raw in qd_raw_list:
        qd = QuantumDrive(**qd_raw)
        qd_list.append(qd)
        logger.success(f"Loaded {qd.chinese_name} successfully")
    return qd_list


def load_qd() -> list[QuantumDrive]:
    """Load a qd from cache if exists, otherwise load from P4K"""
    try:
        return load_qd_from_cache()
    except FileNotFoundError:
        return load_qd_from_p4k()


if __name__ == "__main__":
    load_qd()