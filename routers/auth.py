from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import models
from sqlalchemy.orm import Session
from security import verify_password, create_acces_token


router = APIRouter(
    prefix='/auth',
    tags=['Autenticación']
)


@router.post('/login')
def login(
        from_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    # Buscamos el usuario por su email
    user = db.query(models.User). filter(models.User.email == from_data.username).first()

    # Si el usuario no coincide lanzamos un error 401 (No Autorizado)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales Incorrectas'
        )

    # Si el usuario existe, verificamos la contraseña usando tu funcion de segcurity.py
    if not verify_password(plain_password=from_data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales Incorrectas'
        )

    access_token = create_acces_token(data={'sub': user.email})

    # Si pasa todos los filtros, la utenticación es exitosa. (Generamos el token JWT en el siguiente paso)
    return {'access_token': access_token, 'token_type': 'bearer'}


