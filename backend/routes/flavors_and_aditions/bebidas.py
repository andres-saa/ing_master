# routes/bebidas_router.py

from fastapi import APIRouter, HTTPException
from  schema.bebida import (
    BebidaTypeSchema, BebidaCreateSchema, BebidaUpdateSchema,
    BebidaReadSchema, BebidaGroupCreateSchema, BebidaGroupUpdateSchema,
    BebidaGroupReadSchema, BebidaAssociationSchema
)
from typing import List
from models.flavors_and_aditions.bebida import Bebidas

bebidas_router = APIRouter()

# ------------------- Rutas para Bebidas -------------------

@bebidas_router.post('/create-bebida', tags=['bebidas'])
def create_bebida(data: BebidaCreateSchema):
    bebidas_service = Bebidas()
    bebida_id = bebidas_service.insert_bebida(data)
    bebidas_service.close_connection()
    if bebida_id:
        return {"id": bebida_id}
    else:
        raise HTTPException(status_code=400, detail="No se pudo crear la bebida.")

@bebidas_router.get('/get-bebidas', tags=['bebidas'])
def get_bebidas():
    bebidas_service = Bebidas()
    bebidas = bebidas_service.get_all_bebidas()
    bebidas_service.close_connection()
    return bebidas

@bebidas_router.get('/get-bebida/{bebida_id}', tags=['bebidas'])
def get_bebida(bebida_id: int):
    bebidas_service = Bebidas()
    bebida = bebidas_service.get_bebida_by_id(bebida_id)
    bebidas_service.close_connection()
    if bebida:
        return bebida
    else:
        raise HTTPException(status_code=404, detail="Bebida no encontrada.")

@bebidas_router.put('/update-bebida/{bebida_id}', tags=['bebidas'])
def update_bebida(bebida_id: int, data: BebidaUpdateSchema):
    bebidas_service = Bebidas()
    success = bebidas_service.update_bebida(bebida_id, data)
    bebidas_service.close_connection()
  
    return {"message": "Bebida actualizada con éxito."}
 
@bebidas_router.delete('/delete-bebida/{bebida_id}', tags=['bebidas'])
def delete_bebida(bebida_id: int):
    bebidas_service = Bebidas()
    success = bebidas_service.delete_bebida(bebida_id)
    bebidas_service.close_connection()
    if success:
        return {"message": "Bebida eliminada con éxito."}
    else:
        raise HTTPException(status_code=404, detail="Bebida no encontrada.")

# ------------------- Rutas para Grupos de Bebidas -------------------

@bebidas_router.post('/create-bebida-group', tags=['bebidas'])
def create_bebida_group(data: BebidaGroupCreateSchema):
    bebidas_service = Bebidas()
    group_id = bebidas_service.insert_bebida_group(data)
    bebidas_service.close_connection()
    if group_id:
        return {"id": group_id}
    else:
        raise HTTPException(status_code=400, detail="No se pudo crear el grupo de bebidas.")

@bebidas_router.get('/get-bebida-groups', tags=['bebidas'])
def get_bebida_groups():
    bebidas_service = Bebidas()
    groups = bebidas_service.get_all_bebida_groups()
    bebidas_service.close_connection()
    return groups

@bebidas_router.get('/get-bebida-group/{group_id}', tags=['bebidas'])
def get_bebida_group(group_id: int):
    bebidas_service = Bebidas()
    group = bebidas_service.get_bebida_group_by_id(group_id)
    bebidas_service.close_connection()
    if group:
        return group
    else:
        raise HTTPException(status_code=404, detail="Grupo de bebidas no encontrado.")

@bebidas_router.put('/update-bebida-group/{group_id}', tags=['bebidas'])
def update_bebida_group(group_id: int, data: BebidaGroupUpdateSchema):
    if group_id != data.id:
        raise HTTPException(status_code=400, detail="El ID del grupo en la URL no coincide con el ID en el cuerpo.")
    bebidas_service = Bebidas()
    success = bebidas_service.update_bebida_group(group_id, data)
    bebidas_service.close_connection()
    if success:
        return {"message": "Grupo de bebidas actualizado con éxito."}
    else:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el grupo de bebidas.")

@bebidas_router.delete('/delete-bebida-group/{group_id}', tags=['bebidas'])
def delete_bebida_group(group_id: int):
    bebidas_service = Bebidas()
    success = bebidas_service.delete_bebida_group(group_id)
    bebidas_service.close_connection()
    if success:
        return {"message": "Grupo de bebidas eliminado con éxito."}
    else:
        raise HTTPException(status_code=404, detail="Grupo de bebidas no encontrado.")

# ------------------- Rutas para Asociaciones entre Bebidas y Grupos -------------------

@bebidas_router.post('/assign-bebida-to-group', tags=['bebidas'])
def assign_bebida_to_group(data: BebidaAssociationSchema):
    bebidas_service = Bebidas()
    try:
        for bebida_id in data.bebida_ids:
            bebidas_service.assign_bebida_to_group(bebida_id, data.product_id)
        return {"message": "Bebidas asignadas con éxito al grupo."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        bebidas_service.close_connection()

@bebidas_router.get('/get-bebidas-by-group/{group_id}', tags=['bebidas'])
def get_bebidas_by_group(group_id: int):
    bebidas_service = Bebidas()
    bebidas = bebidas_service.get_bebidas_by_group(group_id)
    bebidas_service.close_connection()
    return bebidas

@bebidas_router.get('/get-groups-by-bebida/{bebida_id}', tags=['bebidas'])
def get_groups_by_bebida(bebida_id: int):
    bebidas_service = Bebidas()
    groups = bebidas_service.get_bebida_groups_by_bebida(bebida_id)
    bebidas_service.close_connection()
    return groups

# ------------------- Rutas para Asociar Bebidas con Productos -------------------

@bebidas_router.post('/associate-bebidas-with-product', tags=['bebidas'])
def associate_bebidas_with_product(data: BebidaAssociationSchema):
    bebidas_service = Bebidas()
    try:
        bebidas_service.associate_bebidas_with_product(data.product_id, data.bebida_ids)
        return {"message": "Bebidas asociadas con éxito al producto."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        bebidas_service.close_connection()

@bebidas_router.get('/get-bebidas-by-product/{product_id}', tags=['bebidas'])
def get_bebidas_by_product(product_id: int):
    bebidas_service = Bebidas()
    bebidas = bebidas_service.get_bebidas_by_product(product_id)
    bebidas_service.close_connection()
    return bebidas

# ------------------- Rutas Adicionales para Crear y Editar Bebidas Directamente -------------------

@bebidas_router.post('/create-bebida-with-product/{product_id}', tags=['bebidas'])
def create_bebida_with_product(product_id: int, data: BebidaCreateSchema):
    bebidas_service = Bebidas()
    try:
        bebida_id = bebidas_service.insert_bebida(data)
        if bebida_id:
            bebidas_service.assign_bebida_to_product(product_id, bebida_id)
            return {"id": bebida_id, "message": "Bebida creada y asociada al producto con éxito."}
        else:
            raise HTTPException(status_code=400, detail="No se pudo crear la bebida.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        bebidas_service.close_connection()

@bebidas_router.post('/edit-bebida/{bebida_id}', tags=['bebidas'])
def edit_bebida(bebida_id: int, data: BebidaUpdateSchema):
    bebidas_service = Bebidas()
    success = bebidas_service.update_bebida(bebida_id, data)
    bebidas_service.close_connection()
    if success:
        return {"message": "Bebida editada con éxito."}
    else:
        raise HTTPException(status_code=400, detail="No se pudo editar la bebida.")
