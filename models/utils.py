from .base_model import UniversalData
from typing import Optional
from loguru import logger


def get_item_by_ref(items: list[UniversalData], ref: str) -> Optional[UniversalData]:
    for item in items:
        if item.ref == ref:
            return item
    logger.error(f"Item with ref {ref} not found!")
    return None