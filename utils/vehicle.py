from scdatatools import StarCitizen
from .file_manager import sc, get_zip_info_ignore_case
from scdatatools.engine.cryxml import etree_from_cryxml_string
from xml.etree import ElementTree
from pydantic import BaseModel
from typing import Tuple


class ShipDefinition(BaseModel):
    name: str


def load_vehicle_definition(path: str) -> ElementTree:

    file = get_zip_info_ignore_case(sc.p4k, path)

    with sc.p4k.open(file, 'r') as f:
        data = f.read()
    data = etree_from_cryxml_string(data)
    return data


def get_vehicle_definition(path: str) -> Tuple[list[dict], float]:
    """Get a vehicle definition from a P4K file"""
    data = load_vehicle_definition(f'data/{path}')

    hull_health = []

    mass = float(data.find('Parts/Part').attrib['mass'].replace('\u202c', ''))

    for part in data.find('Parts/Part/Parts'):
        if 'damageMax' in part.attrib and part.attrib['damageMax'] is not None:
            hull_health.append({
                'name': part.attrib['name'],
                'health': float(part.attrib['damageMax'])
            })
    return hull_health, mass
