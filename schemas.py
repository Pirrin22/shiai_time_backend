from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    name:str
    email:str
    password:str


class UsuarioUpdate(BaseModel):
    name:str | None = None
    belt:str | None = None
    porfile_picture:str | None = None
    email:str | None = None
    password:str | None = None
