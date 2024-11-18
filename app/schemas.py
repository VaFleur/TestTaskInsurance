from pydantic import BaseModel
from datetime import date


class InsuranceRateCreate(BaseModel):
    cargo_type: str
    rate: float
    effective_date: date


class InsuranceRateResponse(BaseModel):
    id: int
    cargo_type: str
    rate: float
    effective_date: date

    class Config:
        orm_mode = True
