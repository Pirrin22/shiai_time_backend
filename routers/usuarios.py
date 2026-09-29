from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix='/usuarios',
    tags=['Usuarios']
)

# Funcion para crear usuarios
@router.post('/', response_model=schemas.UsuarioResponse)
def create_users(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Funcion para recibir la información del usuario
@router.get('/{usuario_id}', response_model=schemas.UsuarioResponse)
def read_user(usuario_id:int, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.id==usuario_id).first()

    if user_found is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    return user_found
# Funcion para actualizar datos de Usuarios
@router.patch('/{usuario_id}', response_model=schemas.UsuarioResponse)
def update_user(usuario_id: int, user_update: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.id==usuario_id).first()

    if user_found is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_found, key, value)

    db.commit()
    db.refresh(user_found)

    return user_found
# Funcion para eliminar Usuarios
@router.delete('/{usuario_id}')
def delete_user(usuario_id: int, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.id==usuario_id).first()

    if user_found is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    db.delete(user_found)
    db.commit()

    return {'Mensaje': 'Usuario eliminado de Shiai Time'}

