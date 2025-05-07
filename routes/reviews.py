from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Review, User, Professional
from schemas import ReviewCreate, ReviewResponse
from typing import List
from datetime import datetime

router = APIRouter()

# 📌 POST /reviews – Új értékelés létrehozása
@router.post("/reviews", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    customer = db.query(User).filter(User.id == review.customer_id, User.user_type == "customer").first()
    professional = db.query(Professional).filter(Professional.id == review.professional_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Ügyfél nem található.")
    if not professional:
        raise HTTPException(status_code=404, detail="Szakember nem található.")

    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Az értékelés csak 1 és 5 között lehet.")

    new_review = Review(
        customer_id=review.customer_id,
        professional_id=review.professional_id,
        rating=review.rating,
        comment=review.comment,
        created_at=datetime.utcnow()
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    # 🔹 `created_at` mezőt stringgé alakítjuk
    return ReviewResponse(
        id=new_review.id,
        customer_id=new_review.customer_id,
        professional_id=new_review.professional_id,
        rating=new_review.rating,
        comment=new_review.comment,
        created_at=new_review.created_at.strftime("%Y-%m-%d %H:%M:%S") if new_review.created_at else None
    )

# 📌 GET /reviews – Összes értékelés lekérdezése
@router.get("/reviews", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return [
        ReviewResponse(
            id=r.id,
            customer_id=r.customer_id,
            professional_id=r.professional_id,
            rating=r.rating,
            comment=r.comment,
            created_at=r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None
        )
        for r in reviews
    ]

# 📌 GET /reviews/{professional_id} – Adott szakember értékeléseinek lekérése
@router.get("/reviews/{professional_id}", response_model=List[ReviewResponse])
def get_reviews_by_professional(professional_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.professional_id == professional_id).all()
    
    if not reviews:
        raise HTTPException(status_code=404, detail="Ehhez a szakemberhez még nem érkezett értékelés.")

    return [
        ReviewResponse(
            id=r.id,
            customer_id=r.customer_id,
            professional_id=r.professional_id,
            rating=r.rating,
            comment=r.comment,
            created_at=r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None
        )
        for r in reviews
    ]