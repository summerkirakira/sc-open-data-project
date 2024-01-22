from pydantic import BaseModel
from .ship import Ship
from typing import Optional
from utils.ship_alias import ShipAlis


class FakeShip(BaseModel):
    ref: Optional[str] = None
    name: str
    chinese_name: str
    health: int
    quantum_fuel: int
    fuel: int
    manufactory: str
    manufactory_chinese_name: str
    manufactory_logo_path: str = ""
    manufactory_logo_path_2: str = ""
    size: int
    role: str
    mass: float
    description: str
    crewSize: int
    cargo: int
    is_fake_ship: bool = True
    ship_alias: Optional[ShipAlis] = None

    class Component(BaseModel):
        size: int
        name: str
        num: int

    weapon: list[Component]
    shield: list[Component]
    missile: list[Component]
    qdrive: list[Component]

    class Dimension(BaseModel):
        x: float
        y: float
        z: float

    dimension: Dimension