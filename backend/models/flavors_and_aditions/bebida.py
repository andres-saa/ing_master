# services/Bebidas.py

from db.db import Db as DataBase
from pydantic import BaseModel
from typing import List, Optional
from schema.bebida import (
    BebidaCreate, BebidaRead, BebidaUpdate,
    BebidaGroupCreate, BebidaGroupRead, BebidaGroupUpdate
)

class Bebidas:
    def __init__(self):
        self.db = DataBase()
    
    # ------------------- Métodos para Bebida -------------------
    
    def insert_bebida(self, bebida_data: BebidaCreate) -> Optional[int]:
        insert_query = """
        INSERT INTO inventory.bebida (name, price, premium)
        VALUES (%s, %s, %s) RETURNING id;
        """
        params = (bebida_data.name, bebida_data.price, bebida_data.premium)
        result = self.db.execute_query(query=insert_query, params=params, fetch=True)
        if result:
            return result[0]['id']
        return None
    
    def get_bebida_by_id(self, bebida_id: int) -> Optional[BebidaRead]:
        select_query = "SELECT id, name, price, premium FROM inventory.bebida WHERE id = %s;"
        params = (bebida_id,)
        result = self.db.execute_query(query=select_query, params=params, fetch=True)
        if result:
            bebida = result[0]
            return BebidaRead(**bebida)
        return None
    
    def get_all_bebidas(self) -> List[BebidaRead]:
        select_query = "SELECT id, name, price, premium FROM inventory.bebida;"
        result = self.db.execute_query(query=select_query, fetch=True)
        return [BebidaRead(**bebida) for bebida in result]
    
    def update_bebida(self, bebida_id: int, bebida_data: BebidaUpdate) -> bool:
        fields = []
        params = []
        
        if bebida_data.name is not None:
            fields.append("name = %s")
            params.append(bebida_data.name)
        if bebida_data.price is not None:
            fields.append("price = %s")
            params.append(bebida_data.price)
        if bebida_data.premium is not None:
            fields.append("premium = %s")
            params.append(bebida_data.premium)
        
        if not fields:
            return False  # No hay campos para actualizar
        
        update_query = f"UPDATE inventory.bebida SET {', '.join(fields)} WHERE id = %s;"
        params.append(bebida_id)
        
        result = self.db.execute_query(query=update_query, params=params)
        return result is not None
    
    def delete_bebida(self, bebida_id: int) -> bool:
        delete_query = "DELETE FROM inventory.bebida WHERE id = %s;"
        params = (bebida_id,)
        result = self.db.execute_query(query=delete_query, params=params)
        return result is not None
    
    # ------------------- Métodos para Bebida Group -------------------
    
    def insert_bebida_group(self, group_data: BebidaGroupCreate) -> Optional[int]:
        insert_query = """
        INSERT INTO inventory.bebida_group (name)
        VALUES (%s) RETURNING id;
        """
        params = (group_data.name,)
        result = self.db.execute_query(query=insert_query, params=params, fetch=True)
        if result:
            return result[0]['id']
        return None
    
    def get_bebida_group_by_id(self, group_id: int) -> Optional[BebidaGroupRead]:
        select_query = "SELECT id, name FROM inventory.bebida_group WHERE id = %s;"
        params = (group_id,)
        result = self.db.execute_query(query=select_query, params=params, fetch=True)
        if result:
            group = result[0]
            return BebidaGroupRead(**group)
        return None
    
    def get_all_bebida_groups(self) -> List[BebidaGroupRead]:
        select_query = "SELECT id, name FROM inventory.bebida_group;"
        result = self.db.execute_query(query=select_query, fetch=True)
        return [BebidaGroupRead(**group) for group in result]
    
    def update_bebida_group(self, group_id: int, group_data: BebidaGroupUpdate) -> bool:
        fields = []
        params = []
        
        if group_data.name is not None:
            fields.append("name = %s")
            params.append(group_data.name)
        
        if not fields:
            return False  # No hay campos para actualizar
        
        update_query = f"UPDATE inventory.bebida_group SET {', '.join(fields)} WHERE id = %s;"
        params.append(group_id)
        
        result = self.db.execute_query(query=update_query, params=params)
        return result is not None
    
    def delete_bebida_group(self, group_id: int) -> bool:
        delete_query = "DELETE FROM inventory.bebida_group WHERE id = %s;"
        params = (group_id,)
        result = self.db.execute_query(query=delete_query, params=params)
        return result is not None
    
    # ------------------- Métodos para Asociar Bebida con Bebida Group -------------------
    
    def assign_bebida_to_group(self, bebida_id: int, group_id: int) -> Optional[int]:
        insert_query = """
        INSERT INTO inventory.bebida_group_bebida (bebida_id, bebida_group_id)
        VALUES (%s, %s) RETURNING id;
        """
        params = (bebida_id, group_id)
        result = self.db.execute_query(query=insert_query, params=params, fetch=True)
        if result:
            return result[0]['id']
        return None
    
    def remove_bebida_from_group(self, bebida_id: int, group_id: int) -> bool:
        delete_query = """
        DELETE FROM inventory.bebida_group_bebida
        WHERE bebida_id = %s AND bebida_group_id = %s;
        """
        params = (bebida_id, group_id)
        result = self.db.execute_query(query=delete_query, params=params)
        return result is not None
    
    def get_bebidas_by_group(self, group_id: int) -> List[BebidaRead]:
        select_query = """
        SELECT b.id, b.name, b.price, b.premium
        FROM inventory.bebida b
        JOIN inventory.bebida_group_bebida bgb ON b.id = bgb.bebida_id
        WHERE bgb.bebida_group_id = %s;
        """
        params = (group_id,)
        result = self.db.execute_query(query=select_query, params=params, fetch=True)
        return [BebidaRead(**bebida) for bebida in result]
    
    def associate_bebidas_with_product(self, product_id: int, bebida_ids: List[int]):
        """
        Asocia una lista de bebidas a un producto específico.
        
        Args:
            product_id (int): ID del producto al que se asociarán las bebidas.
            bebida_ids (List[int]): Lista de IDs de bebidas a asociar.
        
        Este método primero elimina todas las asociaciones existentes de bebidas con el producto,
        y luego inserta las nuevas asociaciones proporcionadas en la lista `bebida_ids`.
        """
        try:
            # Inicia una transacción
            self.db.execute_query("BEGIN;")
            
            # Eliminar asociaciones existentes
            clear_query = "DELETE FROM inventory.bebida_product WHERE product_id = %s"
            self.db.execute_query(query=clear_query, params=(product_id,))
            
            # Insertar nuevas asociaciones
            insert_query = "INSERT INTO inventory.bebida_product (bebida_id, product_id) VALUES (%s, %s)"
            for bebida_id in bebida_ids:
                self.db.execute_query(query=insert_query, params=(bebida_id, product_id))
            
            # Confirmar la transacción
            self.db.execute_query("COMMIT;")
            return {"message": "Bebidas asociadas con éxito al producto."}
        
        except Exception as e:
            # Revertir la transacción en caso de error
            self.db.execute_query("ROLLBACK;")
            print(f"Error al asociar bebidas con el producto: {e}")
            return {"error": f"Error al asociar bebidas con el producto: {e}"}
    
    def get_bebida_groups_by_bebida(self, bebida_id: int) -> List[BebidaGroupRead]:
        select_query = """
        SELECT bg.id, bg.name
        FROM inventory.bebida_group bg
        JOIN inventory.bebida_group_bebida bgb ON bg.id = bgb.bebida_group_id
        WHERE bgb.bebida_id = %s;
        """
        params = (bebida_id,)
        result = self.db.execute_query(query=select_query, params=params, fetch=True)
        return [BebidaGroupRead(**group) for group in result]
    
    # ------------------- Métodos para Relacionar Bebidas con Productos -------------------
    
    def assign_bebida_to_product(self, product_id: int, bebida_id: int) -> Optional[int]:
        insert_query = """
        INSERT INTO inventory.bebida_product (product_id, bebida_id)
        VALUES (%s, %s) RETURNING id;
        """
        params = (product_id, bebida_id)
        result = self.db.execute_query(query=insert_query, params=params, fetch=True)
        if result:
            return result[0]['id']
        return None
    
    def remove_bebida_from_product(self, product_id: int, bebida_id: int) -> bool:
        delete_query = """
        DELETE FROM inventory.bebida_product
        WHERE product_id = %s AND bebida_id = %s;
        """
        params = (product_id, bebida_id)
        result = self.db.execute_query(query=delete_query, params=params)
        return result is not None
    
    def get_bebidas_by_product(self, product_id: int) -> List[BebidaRead]:
        select_query = """
        SELECT b.id, b.name, b.price, b.premium
        FROM inventory.bebida b
        JOIN inventory.bebida_product bp ON b.id = bp.bebida_id
        WHERE bp.product_id = %s;
        """
        params = (product_id,)
        result = self.db.execute_query(query=select_query, params=params, fetch=True)
        return [BebidaRead(**bebida) for bebida in result]
    
    # ------------------- Cerrar Conexión -------------------
    
    def close_connection(self):
        self.db.close_connection()
