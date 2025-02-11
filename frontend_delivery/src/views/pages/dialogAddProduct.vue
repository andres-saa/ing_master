<template>

    <Toast></Toast>
    <Dialog closeOnEscape v-model:visible="store.visibles.dialogAddProduct" modal style="width: 40rem;">
        <Button @click="store.visibles.dialogAddProduct = false" severity="danger"
            style="position: absolute; right: 0; top: 0; right: -1rem; top: -1rem; border-radius: 50%;" rounded icon="pi pi-times"></Button>

        <div class="image" style="display: flex; flex-direction: column;position: relative; justify-content: end; align-items: end;">
            <img v-if="imagePreview" :src="imagePreview" alt="Preview"
                style="width: 100%; aspect-ratio: 1 / 1; background-color: rgb(255, 255, 255); object-fit: cover; border-radius: 0.2rem;" />

            <div v-if="subiendo_foto" style="position: absolute;left: 0; top: 0; width: 100%;display: flex;justify-content: center;align-items: center; height: 100%;background-color: #ffffff80;">
                <ProgressSpinner strokeWidth="8" style="color: white;"></ProgressSpinner>
            </div>
            
            <Button class="my-3" severity="help" @click="fileInput.click()">Agregar foto</Button>
            <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />
        </div>

        <div style="display: flex; flex-direction: column; gap: 1rem;">
     
            <div>
                <span>ID de Categoría:</span>
                <Dropdown v-model="newProduct.category_id" :options="categories" optionLabel="name" optionValue="id" placeholder="Selecciona una categoría" style="width: 100%;" />
            </div>

            <div>
                <span>Nombre:</span>
                <InputText v-model="newProduct.product_name" style="width: 100%;"></InputText>
            </div>
            <div>
                <span>Descripción:</span>
                <Textarea v-model="newProduct.product_description" rows="3" style="width: 100%; resize: none;"></Textarea>
            </div>
          
            <div>
                <span>Anterior Precio:</span>
                <InputNumber v-model="newProduct.last_price" prefix="$" maxFractionDigits="0" style="width: 100%;"></InputNumber>
            </div>

            <div>
                <span>Precio Actual:</span>
                <InputNumber v-model="newProduct.price" prefix="$" maxFractionDigits="0" style="width: 100%;"></InputNumber>
            </div>

            <!-- <div>
                <span>cuantos sabores puede combinar?:</span>
                <InputNumber v-model="newProduct.max_flavor" suffix=" sabores" maxFractionDigits="0" rows="3" min="0" max="2"
                    style="width: 100%;resize: none;">
                </InputNumber>
            </div> -->
        </div>







        <template #footer>
            <div class="col-12 px-0 pb-0">
                <Button @click="prepareToSend" severity="success" label="Guardar"></Button>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, onMounted,watch,computed } from 'vue';
import { useProductStore } from '@/store/productStore';
import { adicionalesService } from '@/service/restaurant/aditionalService';
import { formatoPesosColombianos } from '@/service/formatoPesos';
import { productService } from '@/service/ProductService';
import { restaurantService } from '@/service/restaurant/restaurantService.js';
import { categoriesService } from '@/service/restaurant/categoriesService';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';

import { useSitesStore } from '../../store/site';
import {fetchService} from '../../service/utils/fetchService'
import { URI } from '../../service/conection';



const sabores = ref([])


const site_store = useSitesStore()
const toast = useToast()

const subiendo_foto = ref(false)

const seleccionados = ref([])
const store = useProductStore();
const adicionales = ref([]);
const newProduct = ref({
    product_name: '',
    product_description: '',
    price: 0,
    last_price: 0,
    category_id: null,
    restaurant_id: 5,
    img_identifier: null,
    max_flavor:0
});
const categories = ref([]);
const restaurants = ref([]);
const imagePreview = ref(null);
const fileInput = ref(null);

// Cargar categorías y restaurantes al montar el componente
onMounted(async () => {
    try {
        // categories.value = await categoriesService.getCategories();
        restaurants.value = await restaurantService.getAllRestaurants();
        categories.value = await categoriesService.getCategoriesByRestaurantId(5);
        adicionales.value = await adicionalesService.getAllAditionsRegistered();
    } catch (error) {
        console.error('Error loading data:', error);
    }


    sabores.value = await fetchService.get(`${URI}/get-flavor-grouped`)
});


const restaurantId = 5

watch(restaurantId, async (newRestaurantId, oldRestaurantId) => {
    if (newRestaurantId !== oldRestaurantId) {
        categories.value = await categoriesService.getCategoriesByRestaurantId(5);
        newProduct.value.category_id = null
    }
}, { deep: true });






const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    imagePreview.value = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
        subiendo_foto.value = true
        const response = await productService.uploadPhoto(formData);
        newProduct.value.img_identifier = response.image_identifier;
        URL.revokeObjectURL(imagePreview.value);
        subiendo_foto.value = false
    } catch (error) {
        console.error("Error uploading image:", error);
        subiendo_foto.value = false 
    }
};

// Funciones para manejar los adicionales
const allSelected = (grupo) => adicionales.value[grupo].every(item => item.status);
const toggleGroup = (grupo, value) => {
    adicionales.value[grupo].forEach(item => {
        item.status = value;
        handleSwitch(item.item_id, grupo, value);
    });
};

const handleSwitch = (itemId, grupo, value) => {
    const index = adicionales.value[grupo].findIndex(item => item.item_id === itemId);
    if (index !== -1) {
        adicionales.value[grupo][index].status = value;
    }
};

// Guardar el nuevo producto con los adicionales seleccionados
const prepareToSend = () => {
    if (typeof adicionales.value !== 'object' || adicionales.value === null) {
        console.error("adicionales.value no es un objeto", adicionales.value);
        return; // Salir de la función si no es un objeto
    }

    let aditional_ids = [];
    
    // Iterar sobre las propiedades del objeto adicionales.value
    for (const group in adicionales.value) {
        if (adicionales.value.hasOwnProperty(group)) {
            // Aquí, adicionales.value[group] es un array
            adicionales.value[group].forEach(item => {
                if (item.status) {
                    aditional_ids.push(item.item_id);
                }
            });
        }
    }

    seleccionados.value = aditional_ids;
    send();
};

const send = async() => {
    // Validaciones
    if (!newProduct.value.product_name) {
        alert('Por favor ingrese el nombre del producto.');
        return;
    }

    // Verificar que el precio sea un número
    if (newProduct.value.price === undefined || newProduct.value.price === null || newProduct.value.price === '') {
        alert('Por favor ingrese el precio del producto.');
        return;
    } else if (isNaN(newProduct.value.price)) {
        alert('El precio debe ser un número.');
        return;
    }

    // Verificar que last_price sea un número (opcional, pero si se proporciona debe ser un número)
    if (newProduct.value.last_price !== undefined && newProduct.value.last_price !== '' && isNaN(newProduct.value.last_price)) {
        alert('El "last_price" debe ser un número si se proporciona.');
        return;
    }

    if (!newProduct.value.product_description) {
        alert('Por favor ingrese la descripción del producto.');
        return;
    }

    if (!newProduct.value.category_id) {
        alert('Por favor seleccione una categoría.');
        return;
    }

    // max_flavor: Asegurar que se proporcione y sea numérico
    if (newProduct.value.max_flavor === undefined || newProduct.value.max_flavor === null || newProduct.value.max_flavor === '') {
        alert('Por favor ingrese el número máximo de sabores.');
        return;
    } else if (isNaN(newProduct.value.max_flavor)) {
        alert('El número máximo de sabores debe ser un número.');
        return;
    }

    const product = {
        "name": newProduct.value.product_name,
        "price": Number(newProduct.value.price) || 0,
        "last_price": Number(newProduct.value.last_price) || 0,
        "description": newProduct.value.product_description,
        "category_id": newProduct.value.category_id,
        "restaurant_id": 5,
        "status": true,
        "img_identifier": newProduct.value.img_identifier || '',
        "parent_id": null,
        "max_flavor": Number(newProduct.value.max_flavor)
    };

    const additional_item_ids = seleccionados.value;
    await productService.createProductInstance(product, additional_item_ids);
    resetForm();
};


// Resetear el formulario
const resetForm = () => {
    newProduct.value = {
        product_name: '',
        product_description: '',
        price: 0,
        last_price: 0,
        category_id: null,
        restaurant_id: 5,
        img_identifier: null
    };
    imagePreview.value = null;
    // Resetear adicionales si es necesario

    if (adicionales.value?.length > 0){
        adicionales.value?.forEach(items => {
        items.forEach(item => {
            item.status = false; // o el estado que desees
        });
    });

   

    }

    toast.add({
        severity: 'success',
        summary: 'Producto agregado',
        detail: `Listo`,
        life: 3000 // Duración del toast en milisegundos (3 segundos)
    });

    store.visibles.dialogAddProduct = false
    site_store.update += 1

};
</script>
