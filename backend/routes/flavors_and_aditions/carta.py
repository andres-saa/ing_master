from fastapi import FastAPI, HTTPException, Depends ,APIRouter
from pydantic import BaseModel
from typing import List,Optional
from models.flavors_and_aditions.carta import Carta
carta_router = APIRouter()


class CartaSchema(BaseModel):
    index: int
    img_identifier: str


class CartaSchema2(BaseModel):
    id:int
    index: int
    img_identifier: str

class CartaReorderSchema(BaseModel):
    cartas: List[CartaSchema]


carta = Carta()
    

@carta_router.post("/carta/reorder")
def reorder_carta(cartas: List[CartaSchema2]):
    if not carta:
        raise HTTPException(status_code=400, detail="No carta provided for reordering.")
    
    result = carta.reorder_cartas(cartas)
    
    if result.get("status") == "success":
        return result
    else:
        raise HTTPException(status_code=500, detail=result.get("message"))
    


@carta_router.post("/carta/")
def create_carta(cartas:CartaSchema):
    result = carta.create_carta(cartas)
    return result


@carta_router.get("/carta/")
def read_carta():
    result = carta.get_carta()
    return result


@carta_router.delete("/carta/{carta_id}", response_model=dict)
def delete_carta(carta_id: int):
    result = carta.delete_carta(carta_id)
    if result:
        return {"status": "success", "message": "carta deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="carta not found")
