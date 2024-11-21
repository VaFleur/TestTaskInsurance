from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from app.database import get_db
from app.schemas import InsuranceRateCreate, InsuranceRateResponse
from app.crud import create_insurance_rate, get_insurance_rate, update_insurance_rate, delete_insurance_rate
from app.kafka import send_log_message

router = APIRouter()


@router.get("/calculate")
async def calculate_insurance(
    cargo_type: str,
    declared_value: float,
    date: date = date.today(),
    db: AsyncSession = Depends(get_db),
    user_id: int = None
):
    rate = await get_insurance_rate(db, cargo_type, date)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found for the specified cargo type and date")

    insurance_cost = declared_value * rate.rate

    send_log_message(
        user_id=user_id,
        action="calculate_insurance",
        timestamp=datetime.utcnow()
    )

    return {
        "cargo_type": cargo_type,
        "declared_value": declared_value,
        "rate": rate.rate,
        "insurance_cost": insurance_cost
    }


@router.post("/rate", response_model=InsuranceRateResponse)
async def add_rate(rate: InsuranceRateCreate, db: AsyncSession = Depends(get_db), user_id: int = None):
    new_rate = await create_insurance_rate(db, rate)
    send_log_message(user_id=user_id, action="create_rate", timestamp=datetime.utcnow())
    return new_rate


@router.put("/rate/{rate_id}", response_model=InsuranceRateResponse)
async def edit_rate(rate_id: int, update_data: dict, db: AsyncSession = Depends(get_db), user_id: int = None):
    try:
        updated_rate = await update_insurance_rate(db, rate_id, update_data)
        send_log_message(user_id=user_id, action="edit_rate", timestamp=datetime.utcnow())
        return updated_rate
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/rate/{rate_id}")
async def delete_rate(rate_id: int, db: AsyncSession = Depends(get_db), user_id: int = None):
    try:
        deleted_rate = await delete_insurance_rate(db, rate_id)
        send_log_message(user_id=user_id, action="delete_rate", timestamp=datetime.utcnow())
        return {"message": f"Rate with id {rate_id} has been deleted"}
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
