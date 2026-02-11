from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import Date

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# models
class TravelProject(Base):
    __tablename__ = "travel_project"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String,nullable=True)
    start_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False)
    places = relationship('ProjectPlaces', back_populates="project")
    
class ProjectPlaces(Base):
    __tablename__='project_places'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("travel_project.id"))
    project = relationship('TravelProject',back_populates='places')
    external_id = Column(Integer, nullable=False)
    note = Column(String, nullable=True)
    is_visited = Column(Boolean, default=False)
