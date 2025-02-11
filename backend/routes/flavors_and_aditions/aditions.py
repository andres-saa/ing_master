from fastapi import FastAPI, HTTPException, Depends ,APIRouter
from models.flavors_and_aditions.aditions import Aditions
from pydantic import BaseModel
from typing import List,Optional

adition_router = APIRouter()


class BannerAppSchema(BaseModel):
    index: int
    img_identifier: str

class BannerAppSchema2(BaseModel):
    id:int
    index: int
    img_identifier: str

class BannerReorderSchema(BaseModel):
    banners: List[BannerAppSchema]


class aditional_type_schema(BaseModel):
    name:str
    
class aditional_schema(BaseModel):
    name:str
    type_id:int
    price:int
    
class aditional_schema_edit(BaseModel):
    name:str
    price:int

class FlavorAssociationSchema(BaseModel):
    product_id: int 
    flavor_ids: List[int] 
    
class FlavorEditSchema(BaseModel):
    name: str

class FlavorDeleteSchema(BaseModel):
    soft_delete: bool
additions = Aditions()


#crea grupos de adiciones

@adition_router.post('/create-aditional-category',tags=['flavors and aditions'])
def create_adition_category(data:aditional_type_schema):
    
    aditional_instance = Aditions()
    result = aditional_instance.create_aditional_group(name=data.name)
    return result


@adition_router.post('/create-aditional-to-group',tags=['flavors and aditions'])
def create_adition_category(data:aditional_schema):
    
    aditional_instance = Aditions()
    result = aditional_instance.create_aditional_to_group(data=data)
    return result


#obtiene grupos de sabores
@adition_router.get('/get-aditional-category',tags=['flavors and aditions'])
def create_adition_category():
    
    aditional_instance = Aditions()
    result = aditional_instance.get_additional_categories()
    return result



@adition_router.get('/get-aditional-category-types',tags=['flavors and aditions'])
def create_adition_category():
    
    aditional_instance = Aditions()
    result = aditional_instance.get_additional_categories_categories()
    return result




 #le mete adiciones a un grupo
@adition_router.post('/put-flavors/',tags=['flavors and aditions'])
def create_adition_category(data:FlavorAssociationSchema):
    
    aditional_instance = Aditions()
    result = aditional_instance.associate_flavors_with_product(data.product_id,data.flavor_ids)
    return result



#obgtiene los sabores agrupados
@adition_router.get('/get-flavor-grouped',tags=['flavors and aditions'])
def create_adition_category():
    
    aditional_instance = Aditions()
    result = aditional_instance.get_flavor_grouped()
    return result



class flavor_group_schema(BaseModel):
    name:str
    
    
class flavor_group_schema_edit(BaseModel):
    id:int
    name:str

@adition_router.post('/create-flavor-grouped',tags=['flavors and aditions'])
def create_adition_category(data:flavor_group_schema):
    aditional_instance = Aditions()
    result = aditional_instance.create_flavor_group(data)
    return result



@adition_router.post('/edit-flavor-grouped',tags=['flavors and aditions'])
def create_adition_category(data:flavor_group_schema_edit):
    aditional_instance = Aditions()
    result = aditional_instance.edit_flavor_group(data)
    return result


#actualiza el 
@adition_router.put('/update_aditional_category/{type_id}',tags=['flavors and aditions'])
def create_adition_category(data:aditional_type_schema,type_id:int):
    
    aditional_instance = Aditions()
    result = aditional_instance.edit_aditional_group(name=data.name,type_id=type_id)
    return result


@adition_router.put('/update_aditional_item/{id}',tags=['flavors and aditions'])
def create_adition_category(data:aditional_schema_edit,id:int):
    aditional_instance = Aditions()
    result = aditional_instance.edit_aditional(data=data,id=id)
    return result


@adition_router.delete('/delete_aditional_category/{type_id}',tags=['flavors and aditions'])
def create_adition_category(type_id:int):
    
    aditional_instance = Aditions()
    result = aditional_instance.delete_aditional_group(type_id=type_id)
    return result



@adition_router.delete('/delete_aditional/{aditional_id}',tags=['flavors and aditions'])
def create_adition_category(aditional_id:int):
    
    aditional_instance = Aditions()
    result = aditional_instance.delete_aditional(id=aditional_id)
    return result

@adition_router.delete('/delete_flavor/{flavor_id}',tags=['flavors and aditions'])
def create_adition_category(flavor_id:int):
    aditional_instance = Aditions()
    result = aditional_instance.delete_flavor(flavor_id)
    return result


@adition_router.delete('/delete_flavor_group/{flavor_id}',tags=['flavors and aditions'])
def create_adition_category(flavor_id:int):
    aditional_instance = Aditions()
    result = aditional_instance.delete_flavor_group(flavor_id)
    return result






@adition_router.get('/get_flavors_by_product/{product_id}', tags=['flavors and aditions'])
def get_flavors_by_product(product_id: int):
    aditional_instance = Aditions()
    result = aditional_instance.get_flavors_by_product(product_id=product_id)
    return result


class new_flavor_schema (BaseModel):
    name:str
    price:int
    
class new_flavor_schema_2 (BaseModel):
    name:str
    price:int
    premium:bool
    
    



@adition_router.post('/create-flavor/{id}',tags=['flavors and aditions'])
def create_adition_category(data:new_flavor_schema, id:int):
    aditional_instance = Aditions()
    
    datafinal = new_flavor_schema_2(
        name=data.name,
        price=data.price,
        premium= data.price > 0
    )
    result = aditional_instance.create_flavor(datafinal, id)
    return result




@adition_router.post('/edit-flavor/{id}',tags=['flavors and aditions'])
def create_adition_category(data:new_flavor_schema, id:int):
    aditional_instance = Aditions()
    
    
    datafinal = new_flavor_schema_2(
        name=data.name,
        price=data.price,
        premium= data.price > 0
    )

    result = aditional_instance.edit_flavor(datafinal, id)
    return result







class ProductCategorySchema(BaseModel):
    name: str
    index: int
    resturant_id: int
    # main: bool = False

# Crear categoría de producto
@adition_router.post('/product-categories/', tags=['product categories'])
def create_product_category(data: ProductCategorySchema):
    aditional_instance = Aditions()
    result = aditional_instance.create_product_category(data)
    return result

# Obtener todas las categorías de productos
@adition_router.get('/product-categories/', tags=['product categories'])
def get_product_categories():
    aditional_instance = Aditions()
    result = aditional_instance.get_product_categories()
    return result

# Actualizar categoría de producto
@adition_router.put('/product-categories/{category_id}', tags=['product categories'])
def update_product_category(category_id: int, data: ProductCategorySchema):
    aditional_instance = Aditions()
    result = aditional_instance.update_product_category(data, category_id)
    return result


# Eliminar categoría de producto
@adition_router.delete('/product-categories/{category_id}', tags=['product categories'])
def delete_product_category(category_id: int):
    aditional_instance = Aditions()
    result = aditional_instance.delete_product_category(category_id)
    return result





@adition_router.post("/banners/reorder")
def reorder_banners(banners: List[BannerAppSchema2]):
    if not banners:
        raise HTTPException(status_code=400, detail="No banners provided for reordering.")
    
    result = additions.reorder_banners(banners)
    
    if result.get("status") == "success":
        return result
    else:
        raise HTTPException(status_code=500, detail=result.get("message"))
    


@adition_router.post("/banners/")
def create_banner(banner: BannerAppSchema):
    result = additions.create_banner(banner)
    return result

@adition_router.get("/banners/")
def read_banners():
    banners = additions.get_banners()
    return banners

@adition_router.get("/banners/{banner_id}", response_model=BannerAppSchema)
def read_banner(banner_id: int):
    banner = additions.get_banner_by_id(banner_id)
    if banner:
        return BannerAppSchema(**banner)
    else:
        raise HTTPException(status_code=404, detail="Banner not found")

@adition_router.put("/banners/{banner_id}", response_model=BannerAppSchema)
def update_banner(banner_id: int, banner: BannerAppSchema):
    result = additions.update_banner(banner_id, banner)
    if result:
        return BannerAppSchema(id=result[0]['id'], **banner.dict())
    else:
        raise HTTPException(status_code=404, detail="Banner not found")

@adition_router.delete("/banners/{banner_id}", response_model=dict)
def delete_banner(banner_id: int):
    result = additions.delete_banner(banner_id)
    if result:
        return {"status": "success", "message": "Banner deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Banner not found")
