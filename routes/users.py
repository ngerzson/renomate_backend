from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Professional, ProfessionalProfession
from schemas import UserCreate, UserResponse, ConvertToProfessional
from passlib.context import CryptContext
from datetime import datetime
from typing import List

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Ez az e-mail már használatban van!")

    birth_date = None
    if user.birth_date:
        try:
            birth_date = datetime.strptime(user.birth_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="A születési dátum formátuma helytelen. Használj YYYY-MM-DD formátumot!")

    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        user_type=user.user_type,
        phone=user.phone,
        location_id=user.location_id,
        profile_picture=user.profile_picture,
        birth_date=birth_date
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.user_type == "professional":
        new_professional = Professional(user_id=new_user.id, experience_years=0, bio="")
        db.add(new_professional)
        db.commit()
        db.refresh(new_professional)

        if user.professions:
            for profession_id in user.professions:
                db.add(ProfessionalProfession(professional_id=new_professional.id, profession_id=profession_id))
            db.commit()

    return UserResponse.from_orm(new_user)

@router.put("/users/{user_id}/convert-to-professional", response_model=UserResponse)
def convert_to_professional(user_id: int, convert_data: ConvertToProfessional, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található.")
    
    if user.user_type == "professional":
        raise HTTPException(status_code=400, detail="A felhasználó már szakember.")

    user.user_type = "professional"
    db.commit()
    db.refresh(user)

    new_professional = Professional(user_id=user.id, experience_years=convert_data.experience_years, bio=convert_data.bio)
    db.add(new_professional)
    db.commit()
    db.refresh(new_professional)

    if convert_data.professions:
        for profession_id in convert_data.professions:
            db.add(ProfessionalProfession(professional_id=new_professional.id, profession_id=profession_id))
        db.commit()

    return UserResponse.from_orm(user)

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található.")

    # Ha a felhasználó szakember, először töröljük őt a professionals táblából és a kapcsolódó szakmákat
    professional = db.query(Professional).filter(Professional.user_id == user.id).first()
    
    if professional:
        db.query(ProfessionalProfession).filter(ProfessionalProfession.professional_id == professional.id).delete()
        db.delete(professional)
        db.commit()

    # Töröljük a felhasználót a `users` táblából
    db.delete(user)
    db.commit()
    
    return {"message": f"Felhasználó ({user_id}) és minden kapcsolódó adata sikeresen törölve."}