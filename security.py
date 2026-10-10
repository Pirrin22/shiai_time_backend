from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Depends, HTTPException, status

# --- Configuración JWT ---
# En el futuro guardaremos esta clave en un archivo oculto(.env) por seguridad
SECRET_KEY = 'tu_clave_secreta_super_segura_aqui_cambiala_luego'
ALGORITHM = 'HS256'
ACCES_TOKEN_EXPIRE_MINUTES = 30 # EL token caduca en media hora

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='auth/login')
# Configuramos passlib para que use el algoritmo bcrypt
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Función que recibe una contraseña en texto plano y devuelve el texto encriptado
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Función que compara la contraseña en texto plano con el hash de la base de datos.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para  crear el token
def create_acces_token(data: dict) -> str:
    # Recibe los datos del usuario, añade la fecha de expiración y devuelve el JWT
    to_encode = data.copy()

    # Calculamos la fecha y hora exactas de caducidad
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    # Fabricamos el token uniendo los datos, la clave secreta y el algoritmo
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='No se pudo validar el token'
                )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='El token no existe'
        )

    return email
