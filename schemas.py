import phonenumbers
from pydantic import BaseModel, EmailStr, field_validator, model_validator
import re

countries = {1 : 'ES', 2 : 'FR', 3 : 'IT', 4 : 'AND'}


class UsuarioCreate(BaseModel):
    nickname: str
    first_name: str
    last_name_1: str
    last_name_2: str | None = None
    phone: str | None = None
    email: EmailStr
    password: str
    country_id: int | None = None
    region_id: int | None = None
    city: str | None = None

    @field_validator('password')
    @classmethod
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe contener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', v):
            raise ValueError('La contraseña debe contener al menos un símbolo especial')
        return v 

    @model_validator(mode='after')
    def phone_validation_with_contries_codes(self):
        # Si el usuario no ha puesto teléfono o país, saltamos la validación
        if not self.phone or not self.country_id:
            return self

        # Aqui obtenemos el codigo del diccionario.
        country_code = countries.get(self.country_id)
        if not country_code:
            raise ValueError('El ID del país no está soportado o no existe')

        try:
            # Leemos el número usando las reglas de ese país especifico
            parsed_number = phonenumbers.parse(self.phone, country_code)
            # Le preguntamos a la librería si es un número real en el país
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('El número de teléfono no es válido para este país')

        except phonenumbers.NumberParseException:
            raise ValueError('Formato de teléfono irreconocible')

        return self


class UsuarioUpdate(BaseModel):
    nickname: str | None = None
    first_name: str | None = None
    last_name_1: str | None = None
    last_name_2: str | None = None
    phone: str | None = None
    belt: str | None = None
    profile_picture: str | None = None
    email: str | None = None
    password: str | None = None
    country_id: int | None = None
    region_id: int | None = None
    city: str | None = None

class UsuarioResumen(BaseModel):
    id: int
    nickname: str
    profile_picture: str | None = None

    model_config = {'from_attributes': True}

class UsuarioResponse(BaseModel):
    id: int
    nickname: str
    first_name: str
    last_name_1: str
    last_name_2: str | None = None
    ranking_points: int
    belt: str | None = None
    profile_picture: str | None = None
    country_id: int | None = None
    region_id: int | None = None
    city: str | None = None

    followers: list[UsuarioResumen] = []
    following: list[UsuarioResumen] = []
    
    model_config = {'from_attributes': True}




