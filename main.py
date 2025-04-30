from fastapi import FastAPI
from pydantic import BaseModel 
from datetime import datetime
from typing import List 
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
from fastapi.responses import JSONResponse
from contextlib import contextmanager

# FastAPI app 
app = FastAPI()

# SQLite DB setup 
DATABASE_URL = "sqlite:///./workouts.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Context manager for DB session
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database models 
class Routine(Base):
    __tablename__ = "routines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    routine_name = Column(String)
    exercise = Column(String)
    reps = Column(Integer)
    sets = Column(Integer)
    weight = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    routine_id = Column(Integer, ForeignKey("routines.id"))

Base.metadata.create_all(bind=engine)

# Pydantic schemas
class RoutineCreate(BaseModel):
    name: str

class WorkoutCreate(BaseModel):
    routine_name: str
    exercise: str
    reps: int
    sets: int
    weight: float
    routine_id: int

class WorkoutResponse(WorkoutCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Routes
@app.post("/routines/", response_model=RoutineCreate)
def create_routine(routine: RoutineCreate):
    with get_db() as db:
        db_routine = Routine(name=routine.name)
        db.add(db_routine)
        db.commit()
        db.refresh(db_routine)
        return db_routine

@app.post("/log_workout/", response_model=WorkoutResponse)
def log_new_session(workout: WorkoutCreate):
    with get_db() as db:
        db_workout = Workout(**workout.dict())
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
        return db_workout

@app.get("/routines/{routine_id}/workouts/", response_model=List[WorkoutResponse])
def get_workouts_by_routine(routine_id: int):
    with get_db() as db:
        workouts = db.query(Workout).filter(Workout.routine_id == routine_id).order_by(Workout.timestamp.desc()).all()
        return workouts

@app.get("/recent_workouts/", response_model=List[WorkoutResponse])
def get_recent_workouts():
    with get_db() as db:
        workouts = db.query(Workout).order_by(Workout.timestamp.desc()).limit(5).all()
        return workouts  

@app.get("/routine/{routine_name}", response_model=List[WorkoutResponse])
def get_routine(routine_name: str):
    with get_db() as db:
        workouts = db.query(Workout).filter(Workout.routine_name == routine_name).order_by(Workout.timestamp.desc()).all()
        return workouts

@app.get("/grouped_workouts/")
def get_grouped_workouts():
    with get_db() as db:
        workouts = db.query(Workout).order_by(Workout.timestamp.desc()).all()
        grouped = defaultdict(lambda: defaultdict(list))
        for workout in workouts:
            routine = workout.routine_name
            date = workout.timestamp.strftime("%Y-%m-%d")
            grouped[routine][date].append({
                "exercise": workout.exercise,
                "reps": workout.reps,
                "sets": workout.sets,
                "weight": workout.weight
            })
        return JSONResponse(content=grouped)

@app.get("/latest_session/{routine_name}")
def get_latest_session(routine_name: str):
    with get_db() as db:
        latest_session = db.query(Workout).filter(Workout.routine_name == routine_name).order_by(Workout.timestamp.desc()).first()
        if latest_session:
            return {
                "exercise": latest_session.exercise,
                "reps": latest_session.reps,
                "sets": latest_session.sets,
                "weight": latest_session.weight,
                "timestamp": latest_session.timestamp
            }
        else:
            return {"message": "No previous session found for this routine."}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fitness App API"}