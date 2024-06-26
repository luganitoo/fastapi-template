import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.etl.extract_csv import extract_data
from src.etl.transform_vehicle_csv import transform_data
from src.etl.load_vehicle_csv import load_data
from src.api.database import get_db
from src.api.authentication import authenticate

router = APIRouter()

@router.get("/load-data")
async def load_data_endpoint(db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):
    csv_path = "src/data/vehicle_data.csv"
    extracted_data = extract_data(csv_path)
    transformed_data = transform_data(extracted_data)
    load_data(transformed_data, db_url=os.getenv("DATABASE_URL"))

    return {"message": "Data loaded successfully"}