from pydantic import BaseModel, ConfigDict
from datetime import date


class PlaceBase(BaseModel):

    external_id: int
    note: str | None = None
    
class PlaceResponse(PlaceBase):
    model_config = ConfigDict(from_attributes=True)
    id:int
    project_id: int
    is_visited:bool
   

class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None
    
class ProjectCreate(ProjectBase):
    places : list[PlaceBase] = []
    
class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id:int
    is_completed:bool
    places : list[PlaceResponse]
    

