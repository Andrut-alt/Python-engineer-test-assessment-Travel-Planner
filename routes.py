from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import TravelProject, ProjectPlaces
from schemas import (
    ProjectResponse,
    ProjectCreate,
)
from validators import validate_artwork

MAX_PLACES_PER_PROJECT = 10

router = APIRouter(prefix="/projects", tags=["projects"])
places_router = APIRouter(prefix="/places", tags=["places"])


@router.post('/', response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new travel project.
    
    Validates all provided artworks exist in Art Institute before creating the project.
    Returns the newly created project with all places.
    """
    if len(project_in.places) > MAX_PLACES_PER_PROJECT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Максимум {MAX_PLACES_PER_PROJECT} місць видимо у одному проєкті",
        )

    for place_data in project_in.places:
        is_valid = await validate_artwork(place_data.external_id)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The art {place_data.external_id} is not found",
            )

    new_project = TravelProject(
        name=project_in.name,
        description=project_in.description,
        start_date=project_in.start_date,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    for place_data in project_in.places:
        new_place = ProjectPlaces(
            project_id=new_project.id,
            external_id=place_data.external_id,
            note=place_data.note,
        )
        db.add(new_place)

    db.commit()
    db.refresh(new_project)

    return new_project


