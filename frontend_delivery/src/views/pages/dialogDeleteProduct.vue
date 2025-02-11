<template>
    <Dialog :close="loaded = false" closeOnEscape v-model:visible="store.visibles.dialogDeleteProduct" modal style="width: 20rem;">


         Esta seguro de eliminar <b>{{ store.currentProductToDelete.product_name }}</b> ?

         <div class="py-3" style="overflow: hidden;">
            <img  v-show="loaded" @load="see" :class="loaded && izq? 'cargado1': loaded && !izq? 'cargado2': 'nada'" class=""
                style="width: 100%;height: 100%; background-color: rgb(255, 255, 255);object-fit: contain; border-radius: 0.2rem;"
                :src="`https://backend.salchimonster.com/read-product-image/300/${store.currentProductToDelete.product_name}`" alt=""
               >

               <div  v-show="!loaded" @load="see" :class="loaded? 'cargado': 'sin-cargar'" class="p-0"
                style="width: 100%;aspect-ratio: 1 / 1; background-color: red; height: 100%; background-color: rgb(255, 255, 255);object-fit: contain; border-radius: 0.2rem;"
                 alt=""
               > </div>
         </div>
         

        <template #footer>
            <div class="col-12 p-0">
                <Button style="width: 100%;" @click="deleteProduct(store.currentProductToDelete.product_id)" severity="danger" label="Eliminar producto"></Button>
            </div>
        </template>

    </Dialog>

     
</template>


<script setup>
import { ref, watch } from 'vue';
import { useProductStore } from '@/store/productStore';
import { adicionalesService } from '@/service/restaurant/aditionalService';


import { productService } from '@/service/ProductService';
import { useSitesStore } from '@/store/site';




const site_store = useSitesStore()

const loaded = ref(false)

const see = () => {
    loaded.value = true
    izq.value = !izq.value
}

const izq = ref(false)

const currentAditions = ref([]);
const store = useProductStore();
const adicionales = ref([]);

const product = ref(store.currentProductToDelete) 

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


const deleteProduct = async(product_id) => {
   await productService.deleteProduct(product_id)
   store.visibles.dialogDeleteProduct = false
   site_store.update += 1
}

watch(() => store.currentProductToEdit.id, async () => {
    currentAditions.value = await adicionalesService.getAditional(store.currentProductToEdit.id); // Obtener las adiciones actuales
    adicionales.value = await adicionalesService.getAllAditionsRegistered(); // Obtener todos los adicionales registrados
    updateAdicionalesStatus();
})


const seleccionados = ref([])

const prepareToSend = () => {
    let aditional_ids = [];

    // Iteramos sobre cada grupo en el objeto 'adicionales'
    for (const group in adicionales.value) {
        // Aseguramos que estamos accediendo a una propiedad propia del objeto
        if (adicionales.value.hasOwnProperty(group)) {
            // Iteramos sobre cada item en el grupo
            adicionales.value[group].forEach(item => {
                if (item.status) {
                    aditional_ids.push(item.item_id);
                }
            });
        }
    }

    seleccionados.value = aditional_ids;
    send()
}


const send = () => {
    
    
  const product = {
    "product_id": store.currentProductToEdit.id,
    "name": store.currentProductToEdit.product_name,
    "price":store.currentProductToEdit.price,
    "description": store.currentProductToEdit.product_description,
    "category_id": store.currentProductToEdit.category_id,
    "status": true
  }

  const additional_item_ids = seleccionados.value

  productService.updateProductInstance(product,additional_item_ids)



}
</script>
<style scoped>

@keyframes fadeIn1 {
    from {
       opacity: 0;
        transform: translateX(-100px);
        /* transform: scale(.5); */
        /* background-color: rgb(255, 255, 0); */
        /* filter: blur(1px); */
    }
    to {
        opacity: 1;
        /* filter: blur(1px); */

    }
}

.cargado1 {
    opacity: 0; /* Inicialmente invisible */
    animation: fadeIn1 .1s ease-out forwards; /* Duración de 1 segundo, 'ease-out' para desacelerar hacia el final, y 'forwards' para mantener el estado final visible */
}



@keyframes fadeIn2 {
    from {
       opacity: 0;
        transform: translateX(100px);
        /* transform: scale(.5); */
        /* background-color: rgb(255, 255, 0); */
        /* filter: blur(1px); */
    }
    to {
        opacity: 1;
        /* filter: blur(1px); */

    }
}

.cargado2 {
    opacity: 0; /* Inicialmente invisible */
    animation: fadeIn2 .1s ease-out forwards; /* Duración de 1 segundo, 'ease-out' para desacelerar hacia el final, y 'forwards' para mantener el estado final visible */
}


</style>