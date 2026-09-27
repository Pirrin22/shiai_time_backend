from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix='/clasificacion',
    tags=['Tabla de Clasificación']
    )


@router.get('/')
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.ranking_points.desc()).all()

    return users