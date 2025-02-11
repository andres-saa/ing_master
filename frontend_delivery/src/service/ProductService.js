import axios from "axios";
import { URI } from "./conection";
import { useProductStore } from "../store/productStore";
import {useReportesStore} from "../store/reportes"
import { useSitesStore } from "../store/site";

const site = useSitesStore()

export const productService = {
    
    
    async getProductsByCategorySite(category_id,site_id) {
        try {
            const response = await axios.get(`${URI}/products-all/category-id/${category_id}/site/${31}/${5}`);
            if (response.status === 200) {
                return response.data;
            } else {
                console.error('An error occurred while fetching the ingredients:', response.status);
                return null;
            }
        } catch (error) {
            console.error('An error occurred while fetching the ingredients:', error);
            return null;
        }
    },




    async updateProductInstanceStatus(product_instance_id, new_status) {
        try {
            const response = await axios.put(`${URI}/product-instance/${product_instance_id}/status`, {
                new_status: new_status // Asegurando que el valor enviado es booleano
            });
            if (response.status === 200) {
                console.log('Product instance status updated successfully:', response.data);
                return response.data;
            } else {
                console.error('Failed to update product instance status:', response.status);
                return null;
            }
        } catch (error) {
            console.error('Error updating product instance status:', error);
      
            return null;
        }
    },

    
    async deleteProduct(product_id) {
        try {
            const response = await axios.put(`${URI}/deactivate-product/${product_id}`)
            if (response.status === 200) {
                console.log('Product instance status updated successfully:', response.data);
                return response.data;
            } else {
                console.error('Failed to update product instance status:', response.status);
                return null;
            }
        } catch (error) {
            console.error('Error updating product instance status:', error);
      
            return null;
        }
    },


    async uploadPhoto(formData) {
        try {
            const response = await axios.post(`${URI}/upload-photo-product`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            if (response.status === 200) {
                console.log('Image uploaded successfully:', response.data);
                return response.data; // Devuelve el identificador de la imagen
            } else {
                console.error('Failed to upload image:', response.status);
                return null;
            }
        } catch (error) {
            console.error('Error uploading image:', error);
            return null;
        }
    },



    async updateProductInstance(product, additional_item_ids, flavor_ids) {
        const productStore = useProductStore();
        const store = useReportesStore();
        store.setLoading(true, 'actualizando en todas las sedes');
        productStore.visibles.dialogEditProduct = false;
    
        try {
            const response = await axios.put(`${URI}/products/update/${product.product_id}`, {
                product,
                additional_item_ids,
                flavor_ids  // Agregar los IDs de sabores
            });
    
            if (response.status === 200) {
                store.setLoading(false, 'actualizando en todas las sedes');
                console.log('Product instance status updated successfully:', response.data);
                return response.data;
            } else {
                console.error('Failed to update product instance status:', response.status);
                store.setLoading(false, 'actualizando en todas las sedes');
                return null;
            }
        } catch (error) {
            console.error('Error updating product instance status:', error);
            store.setLoading(false, 'actualizando en todas las sedes');
            return null;
        }
    },



    async createProductInstance(product, additional_item_ids) {
        const productStore = useProductStore();
        const store = useReportesStore();
        store.setLoading(true, 'creando producto en todas las sedes');
        try {
            const response = await axios.post(`${URI}/products/create/`, {
                product,
                additional_item_ids
            });
            if (response.status === 200) {
                store.setLoading(false, 'creando producto en todas las sedes');
                console.log('Product created successfully:', response.data);
                return response.data;
            } else {
                console.error('Failed to create product:', response.status);
                store.setLoading(false, 'creando producto en todas las sedes');
                return null;
            }
        } catch (error) {
            store.setLoading(false, 'creando producto en todas las sedes');
            console.error('Error creating product:', error);
            return null;
        }
    }

}


