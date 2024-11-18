from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.database import get_db
from app.schemas import InsuranceRateCreate, InsuranceRateResponse
from app.crud import create_insurance_rate, get_insurance_rate

router = APIRouter()


@router.post("/rate", response_model=InsuranceRateResponse)
async def add_rate(rate: InsuranceRateCreate, db: AsyncSession = Depends(get_db)):
    return await create_insurance_rate(db, rate)


@router.get("/calculate")
async def calculate_insurance(
    cargo_type: str,
    declared_value: float,
    date: date = date.today(),
    db: AsyncSession = Depends(get_db)
):
    rate = await get_insurance_rate(db, cargo_type, date)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found for the specified cargo type and date")

    insurance_cost = declared_value * rate.rate
    return {"cargo_type": cargo_type, "declared_value": declared_value, "rate": rate.rate, "insurance_cost": insurance_cost}
