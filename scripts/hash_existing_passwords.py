import sys
import os

# 🔗 Projekt gyökérkönyvtár hozzáadása az elérési úthoz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 📌 Importálások
from database import SessionLocal  # Adatbázis kapcsolat importálása
from models import User  # Felhasználó modell importálása
from auth import get_password_hash  # Jelszó titkosító függvény importálása

# 🔄 Adatbázis kapcsolat létrehozása
db = SessionLocal()

# 🔒 Jelszavak titkosítása minden felhasználónál
users = db.query(User).all()

for user in users:
    if not user.password.startswith("$2b$"):  # Ellenőrzés, hogy már hash-elve van-e
        user.password = get_password_hash(user.password)

# ✅ Változások mentése az adatbázisba
db.commit()

# 🔒 Kapcsolat bezárása
db.close()

print("Minden jelszó sikeresen titkosítva!")