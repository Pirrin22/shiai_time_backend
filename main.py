from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

# Esta es la línea que crea las tablas den la base de datos.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def inicio():
    return {'mensaje': 'Bienvenidos a la API de Shiai Time'}
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Funcion para crear usuarios
@app.post('/usuarios/')
def create_users(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    new_user = models.Usuario(name=user.name, email=user.email, password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/usuarios/{usuario_id}')
def read_user(usuario_id:int, db: Session = Depends(get_db)):
    user_found = db.query(models.Usuario).filter(models.Usuario.id==usuario_id).first()

    if user_found is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    return user_found

@app.put('/usuarios/{usuario_id}')
def update_user(usuario_id: int, user_update: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    user_found = db.query(models.Usuario).filter(models.Usuario.id==usuario_id).first()

    if user_found is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_found, key, value)

    db.commit()
    db.refresh(user_found)

    return user_found

@app.delete('/usuarios/{usuario_id}')
def delete_user(usuario_id: int, db: Session = Depends(get_db)):
    user_found = db.query(models.Usuario).filter(models.Usuario.id==usuario_id).first()

    if user_found is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    db.delete(user_found)
    db.commit()

    return {'Mensaje': 'Usuario eliminado de Shiai Time'}

@app.get('/usuarios/')
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.Usuario).order_by(models.Usuario.ranking_points.desc()).all()

    return users