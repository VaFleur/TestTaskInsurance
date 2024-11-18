from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import InsuranceRate
from app.schemas import InsuranceRateCreate, InsuranceRateResponse
from app.database import get_db
from sqlalchemy.future import select

router = APIRouter()


@router.post("/rate", response_model=InsuranceRateResponse)
async def add_rate(rate: InsuranceRateCreate, db: AsyncSession = Depends(get_db)):
    new_rate = InsuranceRate(
        cargo_type=rate.cargo_type,
        rate=rate.rate,
        effective_date=rate.effective_date
    )
    db.add(new_rate)
    await db.commit()
    await db.refresh(new_rate)
    return new_rate
