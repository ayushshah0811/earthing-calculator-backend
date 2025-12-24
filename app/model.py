from pydantic import BaseModel, Field
from typing import Literal

class EarthingInput(BaseModel):
    earthing_type: Literal["pipe", "plate"]

    earth_resistivity: float = Field(..., gt=0)
    fault_current: float = Field(..., gt=0)
    fault_clearing_time: float = Field(..., gt=0)

    number_of_pits: int = Field(..., gt=0)

    strip_width_mm: float = Field(..., gt=0)
    strip_thickness_mm: float = Field(..., gt=0)
    number_of_strips: int = Field(..., gt=0)
    strip_length_m: float = Field(..., gt=0)

    strip_material: str

    # 🔵 Pipe (optional now)
    rod_diameter_mm: float | None = Field(None, gt=0)
    rod_radius_m: float | None = Field(None, gt=0)
    rod_length_m: float | None = Field(None, gt=0)

    # 🟢 Plate (optional)
    plate_length_mm: float | None = Field(None, gt=0)
    plate_width_mm: float | None = Field(None, gt=0)
    plate_thickness_mm: float | None = Field(None, gt=0)

class SummaryRow(BaseModel):
    description: str
    result: float
    unit: str
    condition: str
    remarks: str


class EarthingOutput(BaseModel):
    standard: str
    summary: list[SummaryRow]
    overall_status: str
