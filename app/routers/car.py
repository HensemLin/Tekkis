from fastapi import APIRouter, Depends
from typing import List
from ..controller import *
from .. import schemas
from ..middleware.verify_api_key import verify_api_key

router = APIRouter(
    prefix="/car",
    tags = ["CAR"]
)

router.add_api_route(
    "/", 
    get_car_details, 
    response_model=List[schemas.CarDetails], 
    methods=["GET"],
    dependencies=[Depends(verify_api_key)]
)

router.add_api_route(
    "/{id}", 
    get_car_details_by_id, 
    response_model=schemas.CarDetails, 
    methods=["GET"],
    dependencies=[Depends(verify_api_key)]
)