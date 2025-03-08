from fastapi import FastAPI  # Importáljuk a FastAPI-t
from routes import users, professionals, locations, appointments, professional_professions  # Új végpontok importálása

app = FastAPI()  # Alkalmazás létrehozása

# 📌 Végpontok regisztrálása
app.include_router(users.router)
app.include_router(professionals.router)
app.include_router(locations.router)
app.include_router(appointments.router)  # 📌 Időpontfoglalás végpont hozzáadása
app.include_router(professional_professions.router)  # 📌 Szakember-szakma kapcsolatok végpont hozzáadása

@app.get("/")  # Alapértelmezett végpont
def home():
    return {"message": "RenoMate API is running! Authentication removed."}
