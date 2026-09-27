from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    name:str
    email:str
    password:str
    country_id:int | None = None
    region_id:int | None = None
    city:str | None = None


class UsuarioUpdate(BaseModel):
    name:str | None = None
    belt:str | None = None
    profile_picture:str | None = None
    email:str | None = None
    password:str | None = None
    country_id:int | None = None
    region_id:int | None = None
    city:str | None = None

