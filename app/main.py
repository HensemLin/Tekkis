from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .database import db_models
from .database.db_setup import engine
from .database.db_init_values import initialize_table_data
from .routers import *

db_models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # code to execute when app is loading
    url = "https://www.mudah.my/malaysia/cars-for-sale"
    print(f"Initializing app: scrapping data from {url}")
    initialize_table_data(url=url, limit=50)
    yield
    # code to execute when app is shutting down
    print("shutdown application")

app = FastAPI(lifespan=app_lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(car_router)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to my api"}