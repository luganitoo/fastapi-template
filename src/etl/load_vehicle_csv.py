import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.models import Base, VehicleData, Vin

def create_tables(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
def load_data(df, db_url):
    create_tables(db_url)
    engine = create_engine(db_url) 
    Session = sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():
        # Check if the vin already exists or create a new one
        vin = session.query(Vin).filter_by(vin=row['vin']).first()
        
        if not vin:
            vin = Vin(
                vin=row['vin'],
            )
            session.add(vin)
            session.commit()
            
        # Handle NaN values in integer columns by replacing them with 0
        row = row.fillna(0)

        # Convert 'date_hour' to a valid datetime object
        if pd.notna(row['date_hour']):
            row['date_hour'] = pd.to_datetime(row['date_hour'], errors='coerce')
        else:
            row['date_hour'] = None     
            
        # Reset meaningless negatives
        if row['speed'] < 0: row['speed'] = 0
        if row['chargingpower'] < 0: row['chargingpower'] = 0
        
        # Fix engine_status
        engine_status = str(row['enginestatus']).upper()
        row['enginestatus'] = 'ON' if ('ON' in engine_status) or ('1' in engine_status) else 'OFF'

        # Create and add the vehicle data with the associated vin
        vehicle_data = VehicleData(
            vin_id=vin.id,
            company=row['company'],
            date_hour=row['date_hour'],
            charging_power=row['chargingpower'],
            remaining_electrical_range=row['remainingelectricalrange'],
            engine_status=row['enginestatus'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            mileage=row['mileage'],
            speed=row['speed']
        )
        session.add(vehicle_data)

    session.commit()
    session.close()
    



