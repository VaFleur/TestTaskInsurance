from fastapi import FastAPI
from app.routers import insurance
from app.database import engine
from app.models import Base

app = FastAPI()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(insurance.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
