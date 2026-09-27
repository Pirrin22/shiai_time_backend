from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
from routers import usuarios

# Esta es la línea que crea las tablas den la base de datos.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def inicio():
    return {'mensaje': 'Bienvenidos a la API de Shiai Time'}

app.include_router(usuarios.router)