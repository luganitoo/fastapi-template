from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api import endpoints
from src.api.database import get_db
from src.api.models import VehicleData, Vin

app = FastAPI()
app.include_router(endpoints.router)

# Get Company by VIN number
@app.get("/company/{vin}")
async def get_company(vin: str, db: Session = Depends(get_db)):
    company = db.query(Vin).filter(Vin.vin == vin).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {"company" : company.company}