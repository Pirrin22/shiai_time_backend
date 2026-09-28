from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    nickname: str
    first_name: str
    last_name_1: str
    last_name_2: str | None = None
    phone: str | None = None
    email: str
    password: str
    country_id: int | None = None
    region_id: int | None = None
    city: str | None = None


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




