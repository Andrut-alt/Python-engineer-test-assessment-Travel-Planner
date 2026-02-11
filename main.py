from fastapi import FastAPI

from database import engine, Base
from models import TravelProject, ProjectPlaces
from routes import router, places_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API")

app.include_router(router)
app.include_router(places_router)