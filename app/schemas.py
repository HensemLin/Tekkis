from pydantic import BaseModel
from datetime import datetime

class General(BaseModel):
    brand: str
    model: str
    variant: str
    series: str
    mfg_year: str
    mileage: str
    type: str
    seat_capacity: str
    country_of_origin: str
    price: str

class Transmission(BaseModel):
    transmission: str

class Engine(BaseModel):
    engine_cc: str
    compression_ratio: str
    peak_power: str
    peak_torque: str
    engine_type: str
    fuel_type: str

class DimensionAndWeight(BaseModel):
    length: str
    width: str
    height: str
    wheel_base: str
    kerb_weight: str
    fuel_tank: str

class Brakes(BaseModel):
    front_brakes: str
    rear_brakes: str

class Suspension(BaseModel):
    front_suspension: str
    rear_suspension: str

class Steering(BaseModel):
    steering: str

class TyresAndWheels(BaseModel):
    front_tyres: str
    rear_tyres: str
    front_rims: str
    rear_rims: str

class CarDetails(BaseModel):
    id: str
    general: General
    transmission: Transmission
    engine: Engine
    dimension_and_weight: DimensionAndWeight
    brakes: Brakes
    suspension: Suspension
    steering: Steering
    tyres_and_wheels: TyresAndWheels
    created_at: datetime

    class Config:
        orm_mode = True

class ApiKeyOut(BaseModel):
    id: str                     
    apiKey: str                 
    created_at: datetime        

    class Config:
        orm_mode = True