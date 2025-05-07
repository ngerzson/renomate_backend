from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, User
from schemas import ProfessionalResponse
from typing import List

router = APIRouter()

@router.get("/professionals", response_model=List[ProfessionalResponse])
def get_all_professionals(db: Session = Depends(get_db)):
    professionals = db.query(Professional).all()
    return [ProfessionalResponse.from_orm(professional) for professional in professionals]