from pydantic import BaseModel, Field

class EarthingInput(BaseModel):
    earth_resistivity: float = Field(..., gt=0)
    fault_current: float = Field(..., gt=0)
    fault_clearing_time: float = Field(..., gt=0)

    rod_diameter_mm: float = Field(..., gt=0)
    rod_radius_m: float = Field(..., gt=0)
    rod_length_m: float = Field(..., gt=0)
    number_of_pits: int = Field(..., gt=0)

    strip_width_mm: float = Field(..., gt=0)
    strip_thickness_mm: float = Field(..., gt=0)
    number_of_strips: int = Field(..., gt=0)
    strip_length_m: float = Field(..., gt=0)

    strip_material: str


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
