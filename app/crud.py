from datetime import datetime
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import InsuranceRate
from .schemas import InsuranceRateCreate


async def create_insurance_rate(db: AsyncSession, rate_data: InsuranceRateCreate):
    new_rate = InsuranceRate(
        cargo_type=rate_data.cargo_type,
        rate=rate_data.rate,
        effective_date=rate_data.effective_date
    )
    db.add(new_rate)
    await db.commit()
    await db.refresh(new_rate)
    return new_rate


async def get_insurance_rate(db: AsyncSession, cargo_type: str, date):
    query = select(InsuranceRate).where(
        InsuranceRate.cargo_type == cargo_type,
        InsuranceRate.effective_date <= date
    ).order_by(InsuranceRate.effective_date.desc())
    result = await db.execute(query)
    return result.scalars().first()


async def update_insurance_rate(db: AsyncSession, rate_id: int, update_data: dict):
    query = select(InsuranceRate).where(InsuranceRate.id == rate_id)
    result = await db.execute(query)
    rate = result.scalars().first()
    if not rate:
        raise NoResultFound(f"No InsuranceRate found with id: {rate_id}")

    for key, value in update_data.items():
        setattr(rate, key, value)
    rate.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(rate)
    return rate


async def delete_insurance_rate(db: AsyncSession, rate_id: int):
    query = select(InsuranceRate).where(InsuranceRate.id == rate_id)
    result = await db.execute(query)
    rate = result.scalars().first()
    if not rate:
        raise NoResultFound(f"No InsuranceRate found with id: {rate_id}")

    await db.delete(rate)
    await db.commit()
    return rate
