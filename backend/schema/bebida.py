# schema/bebida.py

from typing import Optional
from pydantic import BaseModel

from typing import List, Optional

class BebidaCreate(BaseModel):
    name: str
    price: int = 0
    premium: bool = False

class BebidaUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    premium: Optional[bool] = None

class BebidaRead(BaseModel):
    id: int
    name: str
    price: int
    premium: bool

class BebidaGroupCreate(BaseModel):
    name: str

class BebidaGroupUpdate(BaseModel):
    name: Optional[str] = None

class BebidaGroupRead(BaseModel):
    id: int
    name: str



class BebidaTypeSchema(BaseModel):
    name: str

class BebidaCreateSchema(BaseModel):
    name: str
    price: int = 0
    premium: bool = False

class   BebidaUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    premium: Optional[bool] = None

class BebidaReadSchema(BaseModel):
    id: int
    name: str
    price: int
    premium: bool

class BebidaGroupCreateSchema(BaseModel):
    name: str

class BebidaGroupUpdateSchema(BaseModel):
    id: int
    name: str

class BebidaGroupReadSchema(BaseModel):
    id: int
    name: str

class BebidaAssociationSchema(BaseModel):
    product_id: int
    bebida_ids: List[int]