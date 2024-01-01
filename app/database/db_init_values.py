import sys, logging
from fastapi import status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..utils.web_scraper import WebScraper
from ..utils.utils import generate_unique_id
from . import db_models
from .db_setup import SessionLocal

def car_exists(car_general, db: Session = SessionLocal()):
    """
    Checks if a car already exists in the database.

    Args:
        db: The database session.
        car_general: Dictionary containing general car information.

    Returns:
        bool: True if the car exists, False otherwise.
    """
    existing_car = db.query(db_models.General).filter(
        db_models.General.brand == car_general.get('Brand'),
        db_models.General.model == car_general.get('Model'),
        db_models.General.variant == car_general.get('Variant'),
        db_models.General.series == car_general.get('Series'),
        db_models.General.mfg_year == car_general.get('Mfg. Year')
    ).first()
    if existing_car is not None:
        return True
    return False

def initialize_table_data(url: str, limit: int = 50, db: Session = SessionLocal()):
    """
    Initialize data in the 'Company' and 'Source' tables.

    This function adds data to the 'Company' and 'Source' tables if it does not already exist.

    Returns:
        None
    """

    try:
        """Initialize data for the 'Shop' and 'ShopLocation' table"""
        print("Initializing....")
        car_details = WebScraper(url=url).scrap_all_cars(limit=limit)
        for car in car_details:
            """Add the car details into database"""
            car_general = car.get('GENERAL', {})
            if car_exists(car_general=car_general):
                print("Car already exists in the database, skipping...")
                continue
            car_price = car.get('PRICE', {})
            car_transmission = car.get('TRANSMISSION', {})
            car_engine = car.get('ENGINE', {})
            car_dimension_and_weight = car.get('DIMENSION & WEIGHT', {})
            car_brakes = car.get('BRAKES', {})
            car_suspension = car.get('SUSPENSION', {})
            car_steering = car.get('STEERING', {})
            car_tyres_and_wheels = car.get('TYRES & WHEELS', {})

            car_id = generate_unique_id()
            new_car_general = db_models.General(
                car_id = car_id,
                brand = car_general.get('Brand'),
                model = car_general.get('Model'),
                variant = car_general.get('Variant'),
                series = car_general.get('Series'),
                mfg_year = car_general.get('Mfg. Year'),
                mileage = car_general.get('Mileage'),
                type = car_general.get('Type'),
                seat_capacity = car_general.get('Seat Capacity'),
                country_of_origin = car_general.get('Country of Origin'),
                price = car_price.get('Price')
            )
            db.add(new_car_general)
            db.flush()

            new_car_transmission = db_models.Transmission(
                car_id = car_id,
                transmission = car_transmission.get('Transmission')
            )
            db.add(new_car_transmission)

            new_car_engine = db_models.Engine(
                car_id = car_id,
                engine_cc = car_engine.get('Engine CC'),
                compression_ratio = car_engine.get('Compression Ratio'),
                peak_power = car_engine.get('Peak Power (KW)'),
                peak_torque = car_engine.get('Peak Torque (NM)'),
                engine_type = car_engine.get('Engine Type'),
                fuel_type = car_engine.get('Fuel Type')
            )
            db.add(new_car_engine)

            new_car_dimension_and_weight = db_models.DimensionAndWeight(
                car_id = car_id,
                length = car_dimension_and_weight.get('Length (mm)'),
                width = car_dimension_and_weight.get('Width (mm)'),
                height = car_dimension_and_weight.get('Height (mm)'),
                wheel_base = car_dimension_and_weight.get('Wheel Base (mm)'),
                kerb_weight = car_dimension_and_weight.get('Kerb Weight (kg)'),
                fuel_tank = car_dimension_and_weight.get('Fuel Tank (litres)')
            )
            db.add(new_car_dimension_and_weight)

            new_car_brakes = db_models.Brakes(
                car_id = car_id,
                front_brakes = car_brakes.get('Front Brakes'),
                rear_brakes = car_brakes.get('Rear Brakes'),
            )
            db.add(new_car_brakes)

            new_car_suspension = db_models.Suspension(
                car_id = car_id,
                front_suspension = car_suspension.get('Front Suspension'),
                rear_suspension = car_suspension.get('Rear Suspension'),
            )
            db.add(new_car_suspension)

            new_car_steering = db_models.Steering(
                car_id = car_id,
                steering = car_steering.get('Steering'),
            )
            db.add(new_car_steering)

            new_car_tyres_and_wheels = db_models.TyresAndWheels(
                car_id = car_id,
                front_tyres = car_tyres_and_wheels.get('Front Tyres'),
                rear_tyres = car_tyres_and_wheels.get('Rear Tyres'),
                front_rims = car_tyres_and_wheels.get('Front Rims (inches)'),
                rear_rims = car_tyres_and_wheels.get('Rear Rims (inches)'),
            )
            db.add(new_car_tyres_and_wheels)
                
        """Commit the changes to the database"""
        db.commit()

    except SQLAlchemyError as sqla_error:
        logging.error("SQLAlchemy error occurred: {}".format(str(sqla_error)), exc_info=True)
        db.rollback()  # Rollback the transaction in case of an SQLAlchemy error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    except Exception as e:
        logging.error(
            f"An error occurred while saving the response: {e}", 
            exc_info=sys.exc_info()
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    finally:
        db.close()