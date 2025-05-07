from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, Profession, ProfessionalProfession
from schemas import ProfessionalProfessionCreate
from typing import List

router = APIRouter()

@router.post("/professional_professions")
def assign_professions(professional_professions: List[ProfessionalProfessionCreate], db: Session = Depends(get_db)):
    """Több szakmát rendel hozzá egy szakemberhez egyszerre"""
    
    for prof_profession in professional_professions:
        professional = db.query(Professional).filter(Professional.id == prof_profession.professional_id).first()
        profession = db.query(Profession).filter(Profession.id == prof_profession.profession_id).first()

        if not professional:
            raise HTTPException(status_code=404, detail=f"Szakember ({prof_profession.professional_id}) nem található.")
        if not profession:
            raise HTTPException(status_code=404, detail=f"Szakma ({prof_profession.profession_id}) nem található.")

        # Ellenőrizzük, hogy már létezik-e a kapcsolat
        existing_assignment = db.query(ProfessionalProfession).filter(
            ProfessionalProfession.professional_id == prof_profession.professional_id,
            ProfessionalProfession.profession_id == prof_profession.profession_id
        ).first()

        if existing_assignment:
            continue  # Ha már létezik, kihagyjuk

        # Új kapcsolat létrehozása
        new_assignment = ProfessionalProfession(
            professional_id=prof_profession.professional_id,
            profession_id=prof_profession.profession_id
        )

        db.add(new_assignment)

    db.commit()
    return {"message": "Szakmák sikeresen hozzárendelve a szakemberhez."}