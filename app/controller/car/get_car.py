import sys
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
from ...database import db_models
from ...database.db_setup import get_db
from ... import schemas


async def get_car_details(db: Session = Depends(get_db)):
    """
    Retrieves a list of car details from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[CarDetails]: A list of car details.

    Raises:
        HTTPException: If no shops are found, a 404 Not Found Error is raised.
        HTTPException: If any other unexpected error occurs, a 500 Internal Server Error is raised.
    """
    try: 
        """Query the database to join Shop and ShopLocation tables and retrieve all records."""
        car_details = db.query(
            db_models.General, 
            db_models.Transmission, 
            db_models.Engine, 
            db_models.DimensionAndWeight, 
            db_models.Brakes, 
            db_models.Suspension, 
            db_models.Steering, 
            db_models.TyresAndWheels
        ).join(
            db_models.Transmission, 
            db_models.General.car_id == db_models.Transmission.car_id
        ).join(
            db_models.Engine, 
            db_models.General.car_id == db_models.Engine.car_id
        ).join(
            db_models.DimensionAndWeight, 
            db_models.General.car_id == db_models.DimensionAndWeight.car_id
        ).join(
            db_models.Brakes, 
            db_models.General.car_id == db_models.Brakes.car_id
        ).join(
            db_models.Suspension, 
            db_models.General.car_id == db_models.Suspension.car_id
        ).join(
            db_models.Steering, 
            db_models.General.car_id == db_models.Steering.car_id
        ).join(
            db_models.TyresAndWheels, 
            db_models.General.car_id == db_models.TyresAndWheels.car_id
        ).all()
        "If no shops are found, raise a 404 Not Found error."
        if not car_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No car(s) found"
            )
        
        result = []
        for car_detail in car_details:
            car_result = schemas.CarDetails(
                id = car_detail.General.car_id,
                general=schemas.General(**car_detail.General.__dict__),
                transmission = schemas.Transmission(**car_detail.Transmission.__dict__),
                engine = schemas.Engine(**car_detail.Engine.__dict__),
                dimension_and_weight = schemas.DimensionAndWeight(**car_detail.DimensionAndWeight.__dict__),
                brakes = schemas.Brakes(**car_detail.Brakes.__dict__),
                suspension = schemas.Suspension(**car_detail.Suspension.__dict__),
                steering = schemas.Steering(**car_detail.Steering.__dict__),
                tyres_and_wheels = schemas.TyresAndWheels(**car_detail.TyresAndWheels.__dict__),
                created_at=car_detail.General.created_at
            )
            result.append(car_result)
            
        return result
    
    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=sys.exc_info())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def get_car_details_by_id(id: str, db: Session = Depends(get_db)):
    """
    Retrieves a single car and its details from the database based on the given ID.

    Args:
        id (int): The ID of the car to retrieve.
        db (Session): The database session.

    Returns:
        CarDetails: The car details.

    Raises:
        HTTPException: If the specified shop is not found, a 404 Not Found Error is raised.  
        HTTPException: If any other unexpected error occurs, a 500 Internal Server Error is raised.
    """
    try: 
        """Query the database to join Shop and ShopLocation tables 
        and retrieve the first record that matches the given shop ID."""
        car_detail = db.query(
            db_models.General, 
            db_models.Transmission, 
            db_models.Engine, 
            db_models.DimensionAndWeight, 
            db_models.Brakes, 
            db_models.Suspension, 
            db_models.Steering, 
            db_models.TyresAndWheels
        ).join(
            db_models.Transmission, 
            db_models.General.car_id == db_models.Transmission.car_id
        ).join(
            db_models.Engine, 
            db_models.General.car_id == db_models.Engine.car_id
        ).join(
            db_models.DimensionAndWeight, 
            db_models.General.car_id == db_models.DimensionAndWeight.car_id
        ).join(
            db_models.Brakes, 
            db_models.General.car_id == db_models.Brakes.car_id
        ).join(
            db_models.Suspension, 
            db_models.General.car_id == db_models.Suspension.car_id
        ).join(
            db_models.Steering, 
            db_models.General.car_id == db_models.Steering.car_id
        ).join(
            db_models.TyresAndWheels, 
            db_models.General.car_id == db_models.TyresAndWheels.car_id
        ).filter(db_models.General.car_id==id).first()
        
        """If the shops is not found, raise a 404 Not Found error"""
        if not car_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Car with id of '{id}' not found"
            )

        """Unpack the query result into CarDetails variables."""
        result = schemas.CarDetails(
            id = car_detail.General.car_id,
            general=schemas.General(**car_detail.General.__dict__),
            transmission = schemas.Transmission(**car_detail.Transmission.__dict__),
            engine = schemas.Engine(**car_detail.Engine.__dict__),
            dimension_and_weight = schemas.DimensionAndWeight(**car_detail.DimensionAndWeight.__dict__),
            brakes = schemas.Brakes(**car_detail.Brakes.__dict__),
            suspension = schemas.Suspension(**car_detail.Suspension.__dict__),
            steering = schemas.Steering(**car_detail.Steering.__dict__),
            tyres_and_wheels = schemas.TyresAndWheels(**car_detail.TyresAndWheels.__dict__)
        )

        return result
    
    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=sys.exc_info())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )