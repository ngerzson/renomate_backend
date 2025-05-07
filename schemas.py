from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

# 📌 1️⃣ Felhasználói típusok
class UserType(str, Enum):
    customer = "customer"
    professional = "professional"

# 📌 2️⃣ Felhasználó létrehozása
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: UserType
    phone: Optional[str] = None
    location_id: Optional[int] = None
    profile_picture: Optional[str] = None
    birth_date: Optional[str] = None  # 📌 YYYY-MM-DD formátumban
    professions: Optional[List[int]] = []  # 🔹 Szakmák ID listája, ha szakember

# 📌 3️⃣ Felhasználói válaszmodell
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: UserType
    phone: Optional[str]
    location_id: Optional[int]
    profile_picture: Optional[str] = None
    birth_date: Optional[str] = None  # 📌 Stringként kell visszaadni

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            user_type=user.user_type,
            phone=user.phone,
            location_id=user.location_id,
            profile_picture=user.profile_picture,
            birth_date=user.birth_date.strftime("%Y-%m-%d") if user.birth_date else None  # 🔹 Konvertálás stringgé
        )

    class Config:
        from_attributes = True

# 📌 4️⃣ Helyszínek kezelése
class LocationCreate(BaseModel):
    country: str
    city: str
    postal_code: Optional[str] = None
    address: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class LocationResponse(LocationCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 5️⃣ Szakember létrehozása
class ProfessionalCreate(BaseModel):
    user_id: int
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    professions: Optional[List[int]] = []  # 🔹 Szakmák ID listája

# 📌 6️⃣ Szakember válaszmodell (Helyesen kezeli a szakmákat!)
class ProfessionalResponse(BaseModel):
    id: int
    user_id: int
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    created_at: Optional[datetime] = None
    professions: List[str] = []  # 🔹 Professzionokat string listaként adja vissza

    @classmethod
    def from_orm(cls, professional):
        return cls(
            id=professional.id,
            user_id=professional.user_id,
            experience_years=professional.experience_years,
            bio=professional.bio,
            created_at=professional.created_at,
            professions=[pp.name for pp in professional.professions]  # 🔹 Professzionokat string listává alakítjuk
        )

    class Config:
        from_attributes = True

# 📌 7️⃣ Felhasználó szakemberré alakítása
class ConvertToProfessional(BaseModel):
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    professions: Optional[List[int]] = []  # 🔹 Szakmák ID listája

# 📌 8️⃣ Szakmák kezelése
class ProfessionCreate(BaseModel):
    name: str

class ProfessionResponse(ProfessionCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 9️⃣ Időpontfoglalások
class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"

class AppointmentCreate(BaseModel):
    customer_id: int
    professional_id: int
    appointment_date: str  # 📌 YYYY-MM-DD HH:MM formátumban
    status: Optional[AppointmentStatus] = AppointmentStatus.pending

class AppointmentResponse(BaseModel):
    id: int
    customer_id: int
    professional_id: int
    appointment_date: str  # 🔹 Most már mindig stringként adjuk vissza!
    status: AppointmentStatus
    created_at: Optional[str]

    @classmethod
    def from_orm(cls, appointment):
        return cls(
            id=appointment.id,
            customer_id=appointment.customer_id,
            professional_id=appointment.professional_id,
            appointment_date=appointment.appointment_date.strftime("%Y-%m-%d %H:%M:%S"),  # 🔹 Dátum konvertálása
            status=appointment.status,
            created_at=appointment.created_at.strftime("%Y-%m-%d %H:%M:%S") if appointment.created_at else None
        )

    class Config:
        from_attributes = True

# 📌 🔟 Kategóriák kezelése
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 1️⃣1️⃣ Alkategóriák kezelése
class SubCategoryCreate(BaseModel):
    name: str
    category_id: int

class SubCategoryResponse(SubCategoryCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 1️⃣2️⃣ Értékelések
class ReviewCreate(BaseModel):
    customer_id: int
    professional_id: int
    rating: int
    comment: Optional[str] = None

class ReviewResponse(ReviewCreate):
    id: int
    created_at: Optional[str]

    class Config:
        from_attributes = True

# 📌 1️⃣3️⃣ Szakemberhez szakmák hozzárendelése
class ProfessionalProfessionCreate(BaseModel):
    professional_id: int
    profession_id: int