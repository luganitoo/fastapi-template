from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import func
from datetime import datetime
from geopy.geocoders import Nominatim

from src.api.endpoints import router
from src.api.database import get_db
from src.api.models import VehicleData, Vin
from src.api.authentication import authenticate

app = FastAPI()
app.include_router(router)

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

# Initialize the geolocator
geolocator = Nominatim(user_agent="vehicle_locator")

def get_location(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), language='en')
    
    if location:
        address = location.raw.get('address', {})
        return address
    else:
        return None
    
# Get all VINs
@app.get("/api/v1/vins")
async def get_vins(db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):
    query = db.query(Vin.vin).all()
        
    if query is None: 
        raise HTTPException(status_code=404, detail="Not found")

    result = [row.vin for row in query]
    return result

# Get all companies
@app.get("/api/v1/companies")
async def get_companies(db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):
    
    query = db.query(VehicleData.company).distinct().all()

    if query is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    result = [row.company for row in query]
    
    return result

# Get last updated data from column by VIN eg. Company, Speed
@app.get("/api/v1/data/{column}/{vin}")
async def get_column_data(column: str, vin: str, db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):

    query = (
            db.query(VehicleData)
            .order_by(VehicleData.id.desc())
            .join(Vin, Vin.id == VehicleData.vin_id)
            .filter(Vin.vin == vin)
            .first()
    )
        
    if query is None: 
        raise HTTPException(status_code=404, detail="Not found")
    
    result = getattr(query, column, None)
    
    if result is None: 
        raise HTTPException(status_code=404, detail="Not found")
    
    return result

# Get last updated data from a specific vehicle VIN
@app.get("/api/v1/vehicle/{vin}/last")
async def get_vehicle_last_data(vin: str, db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):

    query = (
        db.query(VehicleData)
        .join(Vin, Vin.id == VehicleData.vin_id)
        .filter(Vin.vin == vin)
        .order_by(VehicleData.id.desc())
        .first()
    )
    
    if query is None: 
        raise HTTPException(status_code=404, detail="Not found")
    
    location = get_location(query.latitude, query.longitude)
    
    result = {
        'vehicle_data' : query,
        'location': location
    }
    
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)

# Get all data from a specific vehicle VIN xxxxxxxxxxxxxxx
@app.get("/api/v1/vehicle/{vin}")
async def get_vehicle_data(vin: str, db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):
    query = (
        db.query(VehicleData)
        .join(Vin, Vin.id == VehicleData.vin_id)
        .filter(Vin.vin == vin)
    )
    
    result = query.all()
    
    if query is None: 
        raise HTTPException(status_code=404, detail="Not found")

    
    return result

# Get all data from a time window, with optional datapoints
@app.get("/api/v1/vehicles/date-hour-range")
async def get_data_from_time(start_time: str, end_time: str, datapoints: str | None = None, db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):

    start_datetime = datetime.fromisoformat(start_time)
    end_datetime = datetime.fromisoformat(end_time)
    
    # Retrieve only specified columns
    if datapoints:
        # Split the datapoints string into a list
        chosen_datapoints = datapoints.split(',') if datapoints else []
        # Convert column names to SQLAlchemy column objects
        requested_columns = [getattr(VehicleData, col) for col in chosen_datapoints] if chosen_datapoints else [VehicleData]
        
        query = (
            db.query(VehicleData)
            .options(load_only(*requested_columns))
            .filter(VehicleData.date_hour >= start_datetime)
            .filter(VehicleData.date_hour <= end_datetime)
        )
        
    # Retrieve all columns
    else:
        query = (
                db.query(VehicleData)
                .filter(VehicleData.date_hour >= start_datetime)
                .filter(VehicleData.date_hour <= end_datetime)
        )
    
    # Join VIN for identification
    query = query.options(joinedload(VehicleData.vin))
    result = query.all()
    
    if not query: 
        raise HTTPException(status_code=404, detail="Not found")

    return result

# Get Statistics by a specific vehicle VIN
@app.get("/api/v1/statistics/{vin}")
async def get_statistics(vin: str, db: Session = Depends(get_db), current_user: dict = Depends(authenticate)):

    # Calculate basic statistics
    total_charging_power = db.query(func.sum(VehicleData.charging_power)).join(Vin, Vin.id == VehicleData.vin_id).filter(Vin.vin == vin).scalar()
    max_speed = db.query(func.max(VehicleData.speed)).join(Vin, Vin.id == VehicleData.vin_id).filter(Vin.vin == vin).scalar()
    min_remaining_range = db.query(func.min(VehicleData.remaining_electrical_range)).join(Vin, Vin.id == VehicleData.vin_id).filter(Vin.vin == vin).scalar()
    mean_mileage = db.query(func.avg(VehicleData.mileage)).join(Vin, Vin.id == VehicleData.vin_id).filter(Vin.vin == vin).scalar()

    return {
        "statistics": {
            "total_charging_power": total_charging_power,
            "max_speed": max_speed,
            "min_remaining_range": min_remaining_range,
            "mean_mileage": mean_mileage,
        }
    }