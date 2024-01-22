from __future__ import annotations

from pydantic import BaseModel, Field
from .base_model import InputOutputMapping


class CapAssignment(BaseModel):
    ref: str
    path: str
    type: str
    inputOutputMapping: InputOutputMapping


class CapAssignmentRaw(BaseModel):
    ref: str = Field(..., alias='__id')
    path: str = Field(..., alias='__path')
    type: str = Field(..., alias='__type')
    inputOutputMapping: InputOutputMapping

    def to_cap_assignment(self) -> CapAssignment:
        return CapAssignment(
            ref=self.ref,
            path=self.path,
            type=self.type,
            inputOutputMapping=self.inputOutputMapping,
        )
