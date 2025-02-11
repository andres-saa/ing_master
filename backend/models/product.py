
from typing import Optional
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import os
from schema.product import Product as Product_schema
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

class ProductSchemaPost(BaseModel):
    name: str
    price: int
    description: str
    category_id: Optional[int] = None
    porcion: str
    


class Product:
    def __init__(self, product_id=None):
        self.conn_str = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
        self.conn = psycopg2.connect(self.conn_str)
        self.cursor = self.conn.cursor()
        self.product_id = product_id

    # def create_table(self):
    #     create_table_script = """
    #     CREATE TABLE IF NOT EXISTS products (
    #         product_id SERIAL PRIMARY KEY,
    #         name VARCHAR(255),
    #         price INT,
    #         description VARCHAR(255),
    #         category_id INTEGER,
    #         porcion VARCHAR(50)
    #     );
    #     """
        # self.cursor.execute(create_table_script)
        # self.conn.commit()

    def insert_product(self, product_data: Product_schema):
        insert_query = """
        INSERT INTO inventory.products (
            name, description, category_id
        ) VALUES (%s, %s, %s) RETURNING id;
        """
        self.cursor.execute(insert_query, (
            product_data.name,
            product_data.description,
            product_data.category_id # Incluir los nuevos campos
        ))
        product_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return product_id


    def select_products_by_site_and_category_active(self, site_id: int, category_id: int, restaurant_id:int):
        select_query = f"""
        select * from inventory.complete_product_instances
        WHERE site_id = {site_id} AND category_id = {category_id} AND restaurant_id = {restaurant_id} AND status = true order by price;
        """
        self.cursor.execute(select_query)
        columns = [desc[0] for desc in self.cursor.description]
        products = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in products]
    


    def deactivate_product(self, product_id):
        update_query = f"""
        UPDATE inventory.products SET visible = false WHERE id = {product_id}
        """
        self.cursor.execute(update_query)
        self.conn.commit()
        return 'ok'

        
    
    def select_products_by_site_and_category_all(self, site_id: int, category_id: int, restaurant_id:int):
        select_query = f"""
        select * from inventory.complete_product_instances
        WHERE site_id = {site_id} AND category_id = {category_id} AND  restaurant_id = {restaurant_id} order by price;
        """
        self.cursor.execute(select_query)
        columns = [desc[0] for desc in self.cursor.description]
        products = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in products]


    def select_all_products(self):
        select_query = "SELECT * FROM inventory.products;"
        self.cursor.execute(select_query)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    
                
    def select_all_sabores_by_product_id(self, product_id: int):
        """
        Obtiene todos los sabores asociados a un producto específico y los separa en dos listas:
        - 'normal': Sabores cuyo grupo no tiene la cualidad 'gaseosa'.
        - 'gaseosa': Sabores cuyo grupo tiene la cualidad 'gaseosa'.

        Args:
            product_id (int): El ID del producto.

        Returns:
            dict: Un diccionario con dos listas de sabores: 'normal' y 'gaseosa'.
        """
        # Consulta para obtener los sabores asociados al producto, incluyendo la cualidad 'gaseosa' del grupo
        select_query = """
            SELECT 
                spv.id AS flavor_id,
                spv.name AS flavor_name,
                spv.price AS flavor_price,
                spv.premium AS is_premium,
                TRUE AS has_flavor,  -- Dado que estamos filtrando por product_id, siempre tendrá sabor
                spv.gaseosa AS is_gaseosa
            FROM 
                inventory.sabor_product_view spv
            WHERE 
                spv.product_id = %s;
        """
        params = (product_id,)

        try:
            self.cursor.execute(select_query, params)
            columns = [desc[0] for desc in self.cursor.description]
            raw_result = [dict(zip(columns, row)) for row in self.cursor.fetchall()]

            # Inicializar listas para almacenar los sabores
            normal_flavors = []
            gaseosa_flavors = []

            for row in raw_result:
                flavor = {
                    'id': row['flavor_id'],
                    'name': row['flavor_name'],
                    'price': row['flavor_price'],
                    'premium': row['is_premium'],
                    'has_flavor': row['has_flavor']
                }

                if row['is_gaseosa']:
                    gaseosa_flavors.append(flavor)
                else:
                    normal_flavors.append(flavor)

            # Retornar un diccionario con ambas listas
            return {
                'normal': normal_flavors,
                'gaseosa': gaseosa_flavors
            }

        except Exception as e:
            # Manejo de excepciones: puedes personalizar esto según tus necesidades
            print(f"Error al obtener los sabores: {e}")
            return {
                'normal': [],
                'gaseosa': []
            }

    def select_all_sabores(self):
        select_query = "SELECT * FROM inventory.sabor;"
        self.cursor.execute(select_query)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    
    def select_all_restaurants(self):
        select_query = "SELECT * FROM restaurants.restaurant;"
        self.cursor.execute(select_query)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def select_all_sizes(self):
        select_query = "SELECT * FROM inventory.sizes;"
        self.cursor.execute(select_query)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    
    def select_history(self,order_id:str):
        select_query = f"SELECT * FROM orders.order_status_overview where order_id = '{order_id}'"
        self.cursor.execute(select_query)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    

    def select_product_by_id(self, product_id):
        select_query = "SELECT * FROM inventory.product_full_view WHERE product_instance_id = %s;"
        self.cursor.execute(select_query, (product_id,))
        columns = [desc[0] for desc in self.cursor.description]
        results = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in results] if results else []


    def select_products_by_name(self, name: str):
        select_query = "SELECT * FROM inventory.product_full_view; WHERE name = %s;"
        self.cursor.execute(select_query, (name,))
        columns = [desc[0] for desc in self.cursor.description]
        results = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in results] if results else []
    

    def select_product_by_name(self, name: str):
        select_query = "SELECT * FROM products WHERE name = %s;"
        self.cursor.execute(select_query, (name,))
        columns = [desc[0] for desc in self.cursor.description]
        result = self.cursor.fetchone()
        if result:
            return dict(zip(columns, result))
        else:
            return None


    def select_products_by_category_name(self, category_name: str):
            select_query = """
            SELECT p.* FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE c.category_name = %s;
            """
            self.cursor.execute(select_query, (category_name,))
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]


    def select_products_by_category_id_and_site(self, category_id: int, site_id: int):
        select_query = """
        SELECT * FROM inventory.product_full_view 
        WHERE category_id = %s AND site_id = %s AND status; 
        """
        self.cursor.execute(select_query, (category_id, site_id))
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    

    def set_main_product(self, product_id: int):
        try:
            # Inicia una transacción
            self.cursor.execute("BEGIN;")
            
            # Obtener la categoría del producto
            self.cursor.execute(
                "SELECT category_id FROM inventory.products WHERE id = %s;",
                (product_id,)
            )
            result = self.cursor.fetchone()
            if not result:
                self.cursor.execute("ROLLBACK;")
                return "Producto no encontrado."
            category_id = result[0]
            
            # Poner main = false para todos los productos de la misma categoría
            self.cursor.execute(
                "UPDATE inventory.products SET main = false WHERE category_id = %s;",
                (category_id,)
            )
            
            # Poner main = true para el producto especificado
            self.cursor.execute(
                "UPDATE inventory.products SET main = true WHERE id = %s;",
                (product_id,)
            )
            
            # Confirmar la transacción
            self.cursor.execute("COMMIT;")
            return "Producto principal actualizado con éxito."
        
        except Exception as e:
            # Revertir la transacción en caso de error
            self.cursor.execute("ROLLBACK;")
            return f"Error al actualizar el producto principal: {str(e)}"




        
    def update_product_and_its_instances(self, product_info, additional_item_ids, flavor_ids):
        try:
            # Inicia una transacción
            self.cursor.execute("BEGIN;")

            update_product_query = """
            UPDATE inventory.products
            SET name = %s, description = %s, img_identifier = %s, max_flavor = %s
            WHERE id = %s;
            """
            self.cursor.execute(update_product_query, (
                product_info['name'],
                product_info['description'],
                product_info['img_identifier'],
                product_info['max_flavor'],  # Asumiendo que max_flavor se pasa en product_info
                product_info['product_id']
            ))

            # Recupera todos los site_id disponibles
            self.cursor.execute("SELECT site_id FROM public.sites WHERE show_on_web = true;")
            all_sites = self.cursor.fetchall()

            # Actualiza o inserta las instancias del producto en todas las sedes
            for site in all_sites:
                site_id = site[0]
                self.cursor.execute("""
                    UPDATE inventory.product_instances
                    SET price = %s, last_price = %s
                    WHERE product_id = %s AND site_id = %s;
                """, (product_info['price'], product_info['last_price'], product_info['product_id'], site_id))

            # Elimina las asociaciones de productos con adicionales
            self.cursor.execute("""
                DELETE FROM orders.product_aditional_item_instances
                WHERE product_instance_id IN (
                    SELECT id FROM inventory.product_instances WHERE product_id = %s
                );
            """, (product_info['product_id'],))

            # Inserta nuevas instancias de adicionales y crea relaciones con el producto
            for additional_id in additional_item_ids:
                for site in all_sites:
                    site_id = site[0]
                    self.cursor.execute("SELECT price FROM orders.aditional_items WHERE id = %s;", (additional_id,))
                    additional_price = self.cursor.fetchone()[0]

                    self.cursor.execute("""
                        INSERT INTO orders.aditional_item_instances (price, status, aditional_item_id, site_id, category_id)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """, (additional_price, True, additional_id, site_id, product_info['category_id']))
                    additional_instance_id = self.cursor.fetchone()[0]

                    self.cursor.execute("""
                        INSERT INTO orders.product_aditional_item_instances (aditional_item_instance_id, product_instance_id)
                        SELECT %s, id FROM inventory.product_instances WHERE product_id = %s AND site_id = %s;
                    """, (additional_instance_id, product_info['product_id'], site_id))

            # Elimina las asociaciones de productos con sabores existentes
            self.cursor.execute("""
                DELETE FROM inventory.sabor_product
                WHERE product_id = %s;
            """, (product_info['product_id'],))

            # Inserta las nuevas asociaciones de sabores
            for flavor_id in flavor_ids:
                for site in all_sites:
                    site_id = site[0]
                    self.cursor.execute("""
                        INSERT INTO inventory.sabor_product (sabor_id, product_id)
                        VALUES (%s, %s);
                    """, (flavor_id, product_info['product_id']))

            # Confirma los cambios
            self.cursor.execute("COMMIT;")
            return "Producto, sus instancias, adicionales y sabores actualizados con éxito en todas las sedes."

        except Exception as e:
            # Si algo falla, revierte la transacción
            self.cursor.execute("ROLLBACK;")
            return f"Error al actualizar: {str(e)}"



    
    def create_product_and_its_instances(self, product_info, additional_item_ids):
        try:
            # Inicia una transacción
            self.cursor.execute("BEGIN;")

            # Inserta el nuevo producto en la tabla inventory.products
            insert_product_query = """
            INSERT INTO inventory.products (name, description, category_id, has_recipe, gramos, img_identifier)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """
            self.cursor.execute(insert_product_query, (
                product_info['name'],
                product_info['description'],
                product_info['category_id'],
                product_info.get('has_recipe', False),
                product_info.get('gramos', 0),  # Valor por defecto si no se provee
                product_info.get('img_identifier', '')
            ))
            # Recupera el ID del nuevo producto
            new_product_id = self.cursor.fetchone()[0]

            # Recupera todos los site_id disponibles
            self.cursor.execute("SELECT site_id FROM public.sites WHERE show_on_web = true;")
            all_sites = self.cursor.fetchall()

            # Crea las instancias del producto en todas las sedes
            for site in all_sites:
                site_id = site[0]

                insert_product_instance_query = """
                INSERT INTO inventory.product_instances (product_id, site_id, status, price, last_price, restaurant_id,size_id)
                VALUES (%s, %s, %s, %s, %s, %s,%s);
                """
                self.cursor.execute(insert_product_instance_query, (
                    new_product_id,
                    site_id,
                    True,  # Asumiendo que el estado inicial es activo
                    product_info['price'],
                    product_info.get('last_price', 0),  # Valor por defecto para last_price
                    product_info['restaurant_id'],
                    product_info.get('size_id', 7)
                ))

            # Inserta las instancias de adicionales y crea las relaciones con el producto
            for additional_id in additional_item_ids:
                for site in all_sites:
                    site_id = site[0]

                    # Obtener el precio del adicional desde la tabla de adicionales
                    self.cursor.execute(f"SELECT price FROM orders.aditional_items WHERE id = {additional_id}")
                    aditiona_price = self.cursor.fetchone()[0]

                    # Inserta la instancia del adicional en cada sede
                    insert_additional_instance_query = """
                    INSERT INTO orders.aditional_item_instances (price, status, aditional_item_id, site_id, category_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """
                    self.cursor.execute(insert_additional_instance_query, (
                        aditiona_price,
                        True,
                        additional_id,
                        site_id,
                        product_info['category_id']
                    ))
                    additional_instance_id = self.cursor.fetchone()[0]

                    # Relaciona el adicional con la instancia del producto
                    insert_product_additional_relation_query = """
                    INSERT INTO orders.product_aditional_item_instances (aditional_item_instance_id, product_instance_id)
                    SELECT %s, id FROM inventory.product_instances WHERE product_id = %s AND site_id = %s;
                    """
                    self.cursor.execute(insert_product_additional_relation_query, (
                        additional_instance_id,
                        new_product_id,
                        site_id
                    ))

            # Confirma los cambios
            self.cursor.execute("COMMIT;")
            return f"Producto '{product_info['name']}' creado con éxito en todas las sedes."

        except Exception as e:
            # Si algo falla, revierte la transacción
            self.cursor.execute("ROLLBACK;")
            return f"Error al crear el producto: {str(e)}"



    def close_connection(self):
        self.conn.close()

