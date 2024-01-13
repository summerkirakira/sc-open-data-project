from pydantic import BaseModel
from typing import List, Optional


class UniversalData(BaseModel):
    type: str
    name: str
    chinese_name: Optional[str]
    description: Optional[str] = None
    chinese_description: Optional[str] = None
    ref: str

