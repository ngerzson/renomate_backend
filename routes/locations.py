from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Location
from schemas import LocationResponse, LocationCreate
from typing import List 

router = APIRouter()

# 📌 GET /locations - Minden lokáció listázása
@router.get("/locations", response_model=List[LocationResponse])
def get_all_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

# 📌 POST /locations - Új lokáció hozzáadása
@router.post("/locations", response_model=LocationResponse)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    new_location = Location(**location.dict())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location