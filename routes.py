from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import TravelProject, ProjectPlaces
from schemas import (
    ProjectResponse,
    ProjectCreate,
    ProjectUpdate,
    PlaceBase,
    PlaceUpdate,
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


@router.get('/', response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    """Retrieve all travel projects."""
    projects = db.query(TravelProject).all()
    return projects


@router.get('/{project_id}', response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project by its ID."""
    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Project #{project_id} is not found",
        )
    return project


@router.post('/{project_id}/places/', response_model=ProjectResponse)
async def add_place_to_project(
    project_id: int, place_in: PlaceBase, db: Session = Depends(get_db)
):
    """
    Add an artwork to an existing project.
    
    Validates the artwork exists and project has room for more places.
    Raises 400 if artwork already added to this project.
    """
    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()
    if not project:
      
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Project #{project_id} is not found",
        )

    if len(project.places) >= MAX_PLACES_PER_PROJECT:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The Project has max places({MAX_PLACES_PER_PROJECT})",
        )

    existing_place = db.query(ProjectPlaces).filter(
        ProjectPlaces.project_id == project_id,
        ProjectPlaces.external_id == place_in.external_id,
    ).first()
    if existing_place:
       
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"That art is added to the project",
        )

    is_valid = await validate_artwork(place_in.external_id)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The art {place_in.external_id} is not found",
            )

    new_place = ProjectPlaces(
        project_id=project_id,
        external_id=place_in.external_id,
        note=place_in.note,
    )
    db.add(new_place)
    db.commit()
    db.refresh(project)

    return project


@router.patch('/{project_id}', response_model=ProjectResponse)
def update_project_status(
    project_id: int, update_data: ProjectUpdate, db: Session = Depends(get_db)
):
    """Mark a project as completed or reopen it."""
    project = db.query(TravelProject).filter(TravelProject.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Project #{project_id} is not found",
        )

    project.is_completed = update_data.is_completed
    db.commit()
    db.refresh(project)

    return project


@places_router.patch('/{place_id}')
def update_place_status(
    place_id: int, update_data: PlaceUpdate, db: Session = Depends(get_db)
):
    """Mark an artwork as visited or unvisited."""
    place = db.query(ProjectPlaces).filter(ProjectPlaces.id == place_id).first()
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The art #{place_id} is not found",
        )

    place.is_visited = update_data.is_visited
    db.commit()
    db.refresh(place)

    return place
