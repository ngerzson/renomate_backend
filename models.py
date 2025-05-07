from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, Text, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from database import Base

# Felhasználók táblája
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(Enum("customer", "professional", name="user_type"), nullable=False)
    profile_picture = Column(String(500), nullable=True)  # 📌 Hozzáadva az adatbázis alapján
    birth_date = Column(Date, nullable=True)  # 📌 Hozzáadva az adatbázis alapján
    phone = Column(String(20), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))  # 📌 Alapértelmezett érték beállítva

    # 📌 ORM kapcsolatok
    location = relationship("Location", back_populates="users")
    professional_profile = relationship("Professional", back_populates="user", uselist=False)
    reviews = relationship("Review", back_populates="customer")
    appointments = relationship("Appointment", back_populates="customer")  # 📌 ÚJ kapcsolat


# Helyszínek táblája
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    longitude = Column(DECIMAL(10, 8), nullable=True)
    latitude = Column(DECIMAL(10, 8), nullable=True)

    users = relationship("User", back_populates="location")


# Szakemberek táblája
class Professional(Base):
    __tablename__ = "professionals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    experience_years = Column(Integer, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))

    # 📌 ORM kapcsolatok
    user = relationship("User", back_populates="professional_profile")
    appointments = relationship("Appointment", back_populates="professional")
    reviews = relationship("Review", back_populates="professional")

    # 🔹 Helyes kapcsolat a szakmákhoz (Many-to-Many)
    professions = relationship("Profession", secondary="professional_professions", back_populates="professionals")


# Szakmák táblája
class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    # 🔹 Helyes kapcsolat a szakemberekhez (Many-to-Many)
    professionals = relationship("Professional",secondary="professional_professions",back_populates="professions")


# Szakmák és szakemberek kapcsolatát tároló kapcsolótábla
class ProfessionalProfession(Base):
    __tablename__ = "professional_professions"

    professional_id = Column(Integer, ForeignKey("professionals.id", ondelete="CASCADE"), primary_key=True)
    profession_id = Column(Integer, ForeignKey("professions.id", ondelete="CASCADE"), primary_key=True)


# Kategóriák táblája
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    subcategories = relationship("SubCategory", back_populates="category")  # 📌 Helyesen definiált kapcsolat


# Alkategóriák táblája
class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(255), nullable=False, unique=True)

    category = relationship("Category", back_populates="subcategories")  # 📌 Most már biztosan létező osztályra hivatkozik



# Időpontfoglalások táblája (Appointments)
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    appointment_date = Column(TIMESTAMP, nullable=False)
    status = Column(Enum("pending", "confirmed", "completed", "cancelled", name="appointment_status"), default="pending", nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)

    customer = relationship("User", back_populates="appointments")  # 📌 ÚJ kapcsolat
    professional = relationship("Professional", back_populates="appointments")  # 📌 ÚJ kapcsolat


# Értékelések táblája (Reviews)
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="reviews")
    professional = relationship("Professional", foreign_keys=[professional_id], back_populates="reviews")