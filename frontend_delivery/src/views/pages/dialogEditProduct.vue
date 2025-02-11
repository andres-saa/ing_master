<template>
    <Dialog closeOnEscape v-model:visible="store.visibles.dialogEditProduct" modal style="width: 40rem;">

        <!-- {{ seleccionados }} -->
        <!-- <Button @click="store.visibles.dialogEditProduct = false" severity="danger"
            style="position: absolute; right: 0;top: 0;right: -1rem; top: -1rem;" rounded icon="pi pi-times"></Button> -->

        <!-- {{ store.currentProductToEdit }} -->

        <Button @click="store.visibles.dialogEditProduct = false" severity="danger"
            style="position: absolute; right: 0; top: 0; right: -1rem; top: -1rem; border-radius: 50%;" rounded icon="pi pi-times"></Button>



        <div class="image" style="display: flex; flex-direction: column;position: relative; justify-content: end; align-items: end;">
            <img v-if="imagePreview" :src="imagePreview" alt="Preview"
                style="width: 100%; aspect-ratio: 1 / 1; background-color: rgb(255, 255, 255); object-fit: cover; border-radius: 0.2rem;" />

                <img v-else :src="`${URI}/read-photo-product/${store?.currentProductToEdit?.img_identifier}`" alt="Preview"
                style="width: 100%; aspect-ratio: 1 / 1; background-color: rgb(255, 255, 255); object-fit: cover; border-radius: 0.2rem;" />
                

            <div v-if="subiendo_foto" style="position: absolute;left: 0; top: 0; width: 100%;display: flex;justify-content: center;align-items: center; height: 100%;background-color: #ffffff80;">
                <ProgressSpinner strokeWidth="8" style="color: white;"></ProgressSpinner>
            </div>
            
            <Button class="my-3" severity="help" @click="fileInput.click()">Agregar foto</Button>
            <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />
        </div>



        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <div>
                <span>Nombre:</span>
                <InputText v-model="store.currentProductToEdit.product_name" style="width: 100%;">
                </InputText>
            </div>
            <div>
                <span>descripcion:</span>
                <Textarea v-model="store.currentProductToEdit.product_description" rows="3"
                    style="width: 100%;resize: none;">
                </Textarea>
            </div>


            <div>
                <span>Precio anterior:</span>
                <InputNumber v-model="store.currentProductToEdit.last_price" prefix="$" maxFractionDigits="0" rows="3"
                    style="width: 100%;resize: none;">
                </InputNumber>
            </div>
            <div>
                <span>Precio actual:</span>
                <InputNumber v-model="store.currentProductToEdit.price" prefix="$" maxFractionDigits="0" rows="3"
                    style="width: 100%;resize: none;">
                </InputNumber>
            </div>

            <!-- <div>
                <span>cuantos sabores puede combinar?:</span>
                <InputNumber v-model="store.currentProductToEdit.max_flavor" suffix=" sabores" maxFractionDigits="0" rows="3" min="0" max="2"
                    style="width: 100%;resize: none;">
                </InputNumber>
            </div> -->

           
        </div>






        <template #footer>

            <div class="col-12 px-0 pb-0">
                <Button class="" @click="prepareToSend" severity="success" label="Guardar"></Button>
            </div>
        </template>
    </Dialog>


</template>


<script setup>
import { ref, watch } from 'vue';
import { useProductStore } from '@/store/productStore';
import { adicionalesService } from '@/service/restaurant/aditionalService';
import { formatoPesosColombianos } from '@/service/formatoPesos';
import { onMounted } from 'vue';
import { productService } from '@/service/ProductService';
import { URI } from '@/service/conection';
import { fetchService } from '../../service/utils/fetchService';

import { useSitesStore } from '../../store/site';




// Verifica si todos los sabores en un grupo están seleccionados
const allFlavorsSelected = (grupo) => {
    return grupo.flavors.every(flavor => flavor.has_flavor);
};

// Cambiar el estado de todos los sabores en un grupo
const toggleFlavorGroup = (grupo, value) => {
    grupo.flavors.forEach(flavor => {
        flavor.has_flavor = value;
        handleFlavorSwitch(flavor.flavor_id, value);
    });
};

// Manejar conmutadores individuales de sabores
const handleFlavorSwitch = (flavorId, value) => {
    sabores.value.forEach(grupo => {
        const flavor = grupo.flavors.find(f => f.flavor_id === flavorId);
        if (flavor) {
            flavor.has_flavor = value;
        }
    });
};


const visible_group_items = ref([])

const sabores = ref([])


const site_store = useSitesStore()
const currentAditions = ref([]);
const store = useProductStore();
const adicionales = ref([]);

// Cargar todas las adiciones y detalles de adiciones actuales al montar el componente
// onMounted(async () => {
//     currentAditions.value = await adicionalesService.getAditional(store.currentProductToEdit.id); // Obtener las adiciones actuales
//     adicionales.value = await adicionalesService.getAllAditionsRegistered(); // Obtener todos los adicionales registrados
//     updateAdicionalesStatus();
// });

// Función para actualizar el estado de los items en `adicionales` basado en `currentAditions`
// Mantener la vista previa de la imagen localmente
const imagePreview = ref(null);  // Aquí se almacena la URL de la imagen seleccionada

const fileInput = ref(null);



const subiendo_foto = ref(false)

const img = ref('')

const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    imagePreview.value = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
        subiendo_foto.value = true
        const response = await productService.uploadPhoto(formData);
        img.value = response.image_identifier;
        URL.revokeObjectURL(imagePreview.value);
        subiendo_foto.value = false
        
    } catch (error) {
        console.error("Error uploading image:", error);
        subiendo_foto.value = false 
      
    }


   
};


const updateAdicionalesStatus = () => {
    // Asegurar que adicionales está completo y listo para ser procesado
    if (!adicionales.value || adicionales.value.length === 0) return;

    // Recorrer cada grupo de adicionales
    Object.entries(adicionales.value).forEach(([grupo, items]) => {
        items.forEach(item => {
            // Buscar coincidencia en currentAditions
            const match = currentAditions.value.some(addition =>
                addition.items.some(aditional =>
                    aditional.aditional_item_name.toLowerCase() === item.item_name.toLowerCase()
                    && aditional.aditional_item_price === item.item_price &&
                    aditional.aditional_item_type_name === item.type_name
                )
            );
            // Establecer el estado basado en la existencia de la coincidencia
            item.status = match;
        });
    });
};

// Verifica si todos los items en un grupo están seleccionados
const allSelected = (grupo) => {
    return adicionales.value[grupo].every(item => item.status);
};

// Cambiar el estado de todos los items en un grupo
const toggleGroup = (grupo, value) => {
    adicionales.value[grupo].forEach(item => {
        item.status = value;
        handleSwitch(item.item_id, grupo, value);
    });
};

// Manejar conmutadores individuales
const handleSwitch = (itemId, grupo, value) => {
    const index = adicionales.value[grupo].findIndex(item => item.item_id === itemId);
    if (index !== -1) {
        adicionales.value[grupo][index].status = value;
    }
};


onMounted(async() => {
    img.value = store.currentProductToEdit.img_identifier

})

watch(() => store.currentProductToEdit.id, async () => {
    currentAditions.value = await adicionalesService.getAditional(store.currentProductToEdit.id); // Obtener las adiciones actuales
    adicionales.value = await adicionalesService.getAllAditionsRegistered(); // Obtener todos los adicionales registrados
    updateAdicionalesStatus();
    sabores.value = await fetchService.get(`${URI}/get_flavors_by_product/${store?.currentProductToEdit?.product_id}`)

})


const seleccionados = ref([])

const prepareToSend = () => {
    let aditional_ids = [];
    let flavor_ids = [];

    // Recolectar IDs de adicionales
    for (const group in adicionales.value) {
        if (adicionales.value.hasOwnProperty(group)) {
            adicionales.value[group].forEach(item => {
                if (item.status) {
                    aditional_ids.push(item.item_id);
                }
            });
        }
    }

    // Recolectar IDs de sabores
    sabores.value.forEach(grupo => {
        grupo.flavors.forEach(flavor => {
            if (flavor.has_flavor) {  // Asegúrate que 'has_flavor' es el campo correcto
                flavor_ids.push(flavor.flavor_id);  // Asumiendo que 'flavor_id' es el identificador de sabor
            }
        });
    });

    seleccionados.value = aditional_ids;
    send(aditional_ids, flavor_ids);
}


const send = (additional_item_ids, flavor_ids) => {
    const product = {
        "product_id": store.currentProductToEdit.id,
        "name": store.currentProductToEdit.product_name,
        "price": store.currentProductToEdit.price,
        "last_price": store.currentProductToEdit.last_price || 0,
        "description": store.currentProductToEdit.product_description,
        "category_id": store.currentProductToEdit.category_id,
        "status": true,
        "img_identifier": img.value || store.currentProductToEdit.img_identifier,
        "parent_id": store.currentProductToEdit.product_id,
        "max_flavor":store.currentProductToEdit.max_flavor  // Incluir el nuevo identificador
    };

    // Llamar al servicio para actualizar el producto, adicionales y sabores
    productService.updateProductInstance(product, additional_item_ids, flavor_ids);
    site_store.update += 1;
};

</script>
