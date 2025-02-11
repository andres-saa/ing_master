<template>

    <Toast></Toast>
    <Dialog :closable="false"  header="GESTOR DE CATEGORIAS" closeOnEscape v-model:visible="store.visibles.dialogGestorCategoria" modal style="width: 40rem;">




        
            <div style="display: flex;justify-content: end;width: 100%;" class="mb-3">

                <Button @click="visible_add_dialog = true" style="background-color: var(--primary-color);border-radius: .3rem;border: none;" label="Nueva categoria" icon="pi pi-plus">

                </Button>

                
            </div>



        <Button @click="store.visibles.dialogGestorCategoria = false" severity="danger"
            style="position: absolute; right: 0; top: 0; right: -1rem; top: -1rem; border-radius: 50%;" rounded icon="pi pi-times"></Button>


        <div>

            <DataTable  style="background-color: white;" showGridlines stripedRows :value="categories">


               

                <Column style="text-transform: capitalize;" class="p-0 px-2" field="aditional_item_name"
                    header="ID">

                    

                    <template #body="categorie">

                        <h6 class="m-0 " style="text-transform: uppercase;"> {{ categorie.data.id }} </h6>

                    </template>

                </Column>

                <Column style="text-transform: capitalize;" class="p-0 px-2" field="aditional_item_name"
                    header="NOMBRE">

                    

                    <template #body="categorie">

                        <h6 class="m-0 " style="text-transform: uppercase;"> {{ categorie.data.name }} </h6>

                    </template>

                </Column>

                <Column style="width: 2rem;" class="p-0  py-1 pl-3 px-2" header="Interactuar">
                <template #body="adicion">
                    <div style="display: flex;gap: .5rem;justify-content: end;">
                        <Button @click="open_to_edit(adicion.data)" style="width: 2.5rem;height: 2.5rem;border-radius: .3rem;" severity="warning"
                            class="p-0 m-0" rounded icon=" pi pi-pencil"></Button>
                        <Button @click="open_to_delete(adicion.data)" style="width: 2.5rem;height: 2.5rem;border-radius: .3rem;" severity="danger" class="p-1"
                            rounded icon=" pi pi-trash"></Button>
                    </div>
                </template>
                </Column>
      
            </DataTable>


        </div>
      
    </Dialog>



    <Dialog style="width: 30rem;" :closable="false"  header="Nueva categoria"  modal v-model:visible="visible_add_dialog">

        <Button @click="visible_add_dialog = false" severity="danger"
            style="position: absolute; right: 0; top: 0; right: -1rem; top: -1rem; border-radius: 50%;" rounded icon="pi pi-times"></Button>


        <h6 class=""> <b>NOMBRE</b> </h6>
        <InputText v-model="new_category.name"  style="width: 100%;"></InputText>


        <template #footer>
            <div class="col-12 px-0 py-0 m-0 ">
                <Button @click="send_category" style="background-color: var(--primary-color); border: none;border-radius: .3rem;" severity="success" label="Guardar"></Button>
            </div>
        </template>
    </Dialog>


    <Dialog style="width: 30rem;" :closable="false"  header="Editar categoria"  modal v-model:visible="visible_edit_dialog">



        
    <Button @click="visible_edit_dialog = false" severity="danger"
        style="position: absolute; right: 0; top: 0; right: -1rem; top: -1rem; border-radius: 50%;" rounded icon="pi pi-times"></Button>


    <h6 class=""> <b>NOMBRE</b> </h6>
    <InputText  v-model="category_to_edit.name" style="width: 100%;"></InputText>


    <template #footer>
        <div class="col-12 px-0 py-0 m-0 ">
            <Button @click="edit_categorie" style="background-color: var(--primary-color); border: none;border-radius: .3rem;" severity="success" label="Guardar"></Button>
        </div>
    </template>
    </Dialog>




        <Dialog style="width: 30rem;" :closable="false"  header="Eliminar categoria"  modal v-model:visible="visible_delete_dialog">

            <Button @click="visible_delete_dialog = false" severity="danger"
            style="position: absolute; right: 0; top: 0; right: -1rem; top: -1rem; border-radius: 50%;" rounded icon="pi pi-times"></Button>

        <h6> Esta seguro de eliminar la categoria {{ category_to_delete.name }}?</h6>
            <template #footer>
                <div class="col-12 px-0 py-0 m-0 ">
                    <Button @click="delete_categorie" style="background-color: var(--primary-color); border: none;border-radius: .3rem;" severity="success" label="Eliminar"></Button>
                </div>
            </template>
    </Dialog>


</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useProductStore } from '@/store/productStore';
import { adicionalesService } from '@/service/restaurant/aditionalService';
import { formatoPesosColombianos } from '@/service/formatoPesos';
import { productService } from '@/service/ProductService';
import { restaurantService } from '@/service/restaurant/restaurantService.js';
import { categoriesService } from '@/service/restaurant/categoriesService';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';

import { useSitesStore } from '../../store/site';
import { fetchService } from '../../service/utils/fetchService'
import { URI } from '../../service/conection';



const new_category = ref({
  "name": "",
  "index": 0,
  "resturant_id": 5,
  "main": false
})


const send_category = async() => {


     if(!new_category.value){
        alert("por favor proporcione un nombre para la categoria")
        return
     }

     await fetchService.post(`${URI}/product-categories/`, new_category.value)
     visible_add_dialog.value = false
     categories.value = await categoriesService.getCategoriesByRestaurantId(5);


}





const sabores = ref([])
const category_to_delete = ref({})

const visible_add_dialog = ref(false)
const visible_edit_dialog = ref(false)
const visible_delete_dialog = ref(false)
const category_to_edit = ref({
    name:''
})


const open_to_edit = (category) => {
    visible_edit_dialog.value =  true
    category_to_edit.value = {...category, category_id:category.id}

}


const edit_categorie = async() => {
    await fetchService.put(`${URI}/product-categories/${category_to_edit.value.id}`, category_to_edit.value)
    visible_edit_dialog.value =  false
    categories.value = await categoriesService.getCategoriesByRestaurantId(5);

} 


const delete_categorie = async() => {

    await fetchService.delete(`${URI}/product-categories/${category_to_delete.value.id}`)
    categories.value = await categoriesService.getCategoriesByRestaurantId(5);
    visible_delete_dialog.value = false

}

const open_to_delete = async(category) => {
    category_to_delete.value = category
    visible_delete_dialog.value = true
}


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
    img_identifier: null
});
const categories = ref([{}]);
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

const send = async () => {
    const product = {
        "name": newProduct.value.product_name,
        "price": newProduct.value.price || 0,
        "last_price": newProduct.value.last_price || 0,
        "description": newProduct.value.product_description,
        "category_id": newProduct.value.category_id,
        "restaurant_id": 5,
        "status": true,
        "img_identifier": newProduct.value.img_identifier || '', // Establecer un valor predeterminado
        "parent_id": null // Asegúrate de que este campo esté incluido si es necesario
    };

    const additional_item_ids = seleccionados.value;
    await productService.createProductInstance(product, additional_item_ids);
    resetForm()


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

    if (adicionales.value?.length > 0) {
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
