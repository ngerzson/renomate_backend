from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# .env fájl betöltése
load_dotenv()

# Ellenőrizzük, hogy a DATABASE_URL megfelelően betöltődött-e
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("🚨 Hiba: A DATABASE_URL nincs beállítva a .env fájlban!")

# Adatbázis motor létrehozása
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM modellek alapja
Base = declarative_base()

# Adatbázis kapcsolat létrehozása minden egyes kéréshez
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()