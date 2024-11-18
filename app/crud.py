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
