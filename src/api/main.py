from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import text, column
from datetime import datetime
from geopy.geocoders import Nominatim

from src.api import endpoints
from src.api.database import get_db
from src.api.models import VehicleData, Vin
from src.api.authentication import authenticate

app = FastAPI()
app.include_router(endpoints.router)

# Replace IP
origins = ["*"]  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    # allow_methods=["GET", "POST"]
    allow_headers=["*"],
    # allow_headers=["Content-Type", "Authorization"]
)

# Get Companies by Vin or all
@app.get("/api/v1/company")
async def get_company(vin: str | None = None,db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):
    if vin is None:
        query = db.query(VehicleData.company).distinct().all()
        keyword = "companies"
    else:
        query = db.query(VehicleData.company).filter(Vin.vin == vin).first()
        keyword = "company"
        
    if query is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    result = [row.company for row in query] if vin is None else query.company
    
    return {keyword : result}

# Get Vins data
@app.get("/api/v1/vins")
async def get_vins(vin: str | None = None,db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):
    if vin is None:
        query = db.query(Vin.vin).distinct().all()
        keyword = "vins"
    else:
        query = db.query(Vin).filter(Vin.vin == vin).first()
        keyword = "vin"
        
    if query is None: 
        raise HTTPException(status_code=404, detail="Not found")
    
    result = [row.vin for row in query] if vin is None else query
    return {keyword : result}

# # Get data from a specific vehicle
# @app.get("/api/v1/vehicles/last-row")
# async def get_vehicle_last_row(vin: str, db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):

#     result = (
#         db.query(VehicleData)
#         .join(Vin, Vin.id == VehicleData.vin_id)
#         .filter(Vin.vin == vin)
#         .order_by(VehicleData.id.desc())
#         .first()
#     )
    
#     if result is None:
#         raise HTTPException(status_code=404, detail="Not found")
    
#     return {"vehicle" : result}

# Get data from a time window --------- STILL HAVE TO MAKE THE DATAPOINTS WORK
@app.get("/api/v1/data/date-hour-range")
async def get_data_from_time(start_time: str, end_time: str, datapoints: str | None = None, db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):

    start_datetime = datetime.fromisoformat(start_time)
    end_datetime = datetime.fromisoformat(end_time)
    
    # Split the datapoints string into a list
    chosen_datapoints = datapoints.split(',') if datapoints else []

    # Dynamically build the list of columns to select
    selected_columns = [
        VehicleData,
        Vin,
        *[text(datapoint) if datapoint not in ['vin', 'company'] else column(datapoint) for datapoint in chosen_datapoints]
    ]

    query = (
        db.query(*selected_columns)
        .filter(VehicleData.date_hour >= start_datetime)
        .filter(VehicleData.date_hour <= end_datetime)
    )

    query = query.join(Vin).all()
    
    if not query:
        raise HTTPException(status_code=404, detail="Not found")

    result = [{
        "vehicle_data": row.VehicleData,
        "vin": row.Vin.vin,
        }
        for row in query
    ]
    
    json_compatible_item_data = jsonable_encoder(result)
    
    return JSONResponse(content=json_compatible_item_data)
