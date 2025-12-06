import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from backend.config import settings
from backend.database import mongo, sqlite_fallback
from backend.routes import organizaciones, proyectos, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar DB
    if settings.use_sqlite_fallback:
        await sqlite_fallback.init_sqlite()
        app.state.db = await sqlite_fallback.get_db()
    else:
        app.state.db = mongo
    
    yield
    
    # Cerrar conexiones
    if hasattr(app.state.db, "close"):
        await app.state.db.close()

app = FastAPI(lifespan=lifespan)

# Servir frontend
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Rutas API
app.include_router(organizaciones.router)
app.include_router(proyectos.router)
app.include_router(auth.router)

@app.get("/")
async def home():
    return {"mensaje": "pampeano-web API"}
