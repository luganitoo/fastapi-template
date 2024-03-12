from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vin(Base):
    __tablename__ = 'vins'

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)

class VehicleData(Base):
    __tablename__ = 'vehicle_data'

    id = Column(Integer, primary_key=True, index=True)
    vin_id = Column(Integer, ForeignKey('vins.id'), nullable=False)
    company = Column(String)
    date_hour = Column(DateTime)
    charging_power = Column(Float)
    remaining_electrical_range = Column(Float)
    engine_status = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    mileage = Column(Integer)
    speed = Column(Float)

    vin = relationship("Vin", back_populates="vehicle_data")

Vin.vehicle_data = relationship("VehicleData", order_by=VehicleData.id, back_populates="vin")