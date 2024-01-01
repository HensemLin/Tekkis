from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DATETIME
from .db_setup import Base
    
class General(Base):
    __tablename__ = "general"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), unique=True, nullable=False)
    brand = Column(String(255))
    model = Column(String(255))
    variant = Column(String(255))
    series = Column(String(255))
    mfg_year = Column(String(255))
    mileage = Column(String(255))
    type = Column(String(255))
    seat_capacity = Column(String(255))
    country_of_origin = Column(String(255))
    price = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class Transmission(Base):
    __tablename__ = "transmission"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), ForeignKey('general.car_id'), nullable=False)
    transmission = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class Engine(Base):
    __tablename__ = "engine"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), ForeignKey('general.car_id'), nullable=False)
    engine_cc = Column(String(255))
    compression_ratio = Column(String(255))
    peak_power = Column(String(255))
    peak_torque = Column(String(255))
    engine_type = Column(String(255))
    fuel_type = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class DimensionAndWeight(Base):
    __tablename__ = "dimension_and_weight"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), ForeignKey('general.car_id'), nullable=False)
    length = Column(String(255))
    width = Column(String(255))
    height = Column(String(255))
    wheel_base = Column(String(255))
    kerb_weight = Column(String(255))
    fuel_tank = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class Brakes(Base):
    __tablename__ = "brakes"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), ForeignKey('general.car_id'), nullable=False)
    front_brakes = Column(String(255))
    rear_brakes = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class Suspension(Base):
    __tablename__ = "suspension"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), ForeignKey('general.car_id'), nullable=False)
    front_suspension = Column(String(255))
    rear_suspension = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class Steering(Base):
    __tablename__ = "steering"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), ForeignKey('general.car_id'), nullable=False)
    steering = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class TyresAndWheels(Base):
    __tablename__ = "tyres_and_wheels"

    id = Column(Integer, primary_key=True, nullable=False)
    car_id = Column(String(255), ForeignKey('general.car_id'), nullable=False)
    front_tyres = Column(String(255))
    rear_tyres = Column(String(255))
    front_rims = Column(String(255))
    rear_rims = Column(String(255))
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class ApiKey(Base):
    __tablename__ = "api_key"

    id = Column(Integer, primary_key=True, nullable=False)
    apiKey_id = Column(String(255), unique=True, nullable=False)
    apiKey = Column(LONGTEXT, nullable=False)
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)