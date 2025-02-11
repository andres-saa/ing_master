<template>


<div class="col-12 p-3">

    <p  class=" text-4xl text-center px-4" style="font-weight: bold; margin-top: 6rem;">
    <i class="fa-solid fa-truck-arrow-right"></i>
       Domicilios
    </p>


<Dialog v-model:visible="showAddNeighborhoodDialog" header="Agregar Nuevo Barrio" :modal="true" :closable="false">
        <div class="p-fluid">
            <div class="p-field">
                <label for="name">Nombre del Barrio</label>
                <InputText id="name" v-model="newNeighborhood.name" />
            </div>
            <div class="p-field">
                <label for="delivery_price">Precio de Domicilio</label>
                <InputNumber id="delivery_price" v-model="newNeighborhood.delivery_price" mode="currency" currency="USD" locale="en-US"/>
            </div>
            <!-- Asumiendo que ya tienes cargados 'sites' y 'cities' -->
            <div class="p-field">
                <label for="site">Sede</label>
                <Dropdown id="site" v-model="newNeighborhood.site_id" :options="sites" optionLabel="site_name" placeholder="Selecciona una Sede"/>
            </div>
            <div class="p-field">
                <label for="city">Ciudad</label>
                <Dropdown id="city" v-model="newNeighborhood.city_id" :options="cities" optionLabel="name" placeholder="Selecciona una Ciudad"/>
            </div>
        </div>
        <template #footer>
            <Button label="Cancelar" icon="pi pi-times" @click="showAddNeighborhoodDialog = false" class="p-button-text" />
            <Button label="Guardar" icon="pi pi-check" @click="addNeighborhood" class="p-button-text" />
        </template>
    </Dialog>


<div style="max-width: 700px;" class="m-auto ">

    <div style="display: flex;gap:1rem; align-items: center;;">

        <!-- <p class="m-0 p-2  " style="font-weight: bold;"> SEDE</p> -->




        <!-- <Dropdown style="width: 100%;"  filter v-model="site" :options="sites.filter(n => n.show_on_web)" placeholder="SEDE" optionLabel="site_name"
                            required="true" :class="{ 'p-invalid': submitted && !currentUser.position }" 
                            /> -->
    </div>





    <RouterView>

    </RouterView>
</div>


</div>

</template>
        
        
<script setup>


import { onMounted, ref, watch } from 'vue';
import { URI } from '@/service/conection';
import router from '../../router';
import { useRoute } from 'vue-router';
const sites  = ref([])
const site = ref({})


const showAddNeighborhoodDialog = ref(false);
const newNeighborhood = ref({
  neighborhood_id: 0, // Generalmente asignado por el servidor
  name: '',
  delivery_price: 0,
  site_id: 0,
  city_id: 0
});

// const sites = ref([]); // Debes cargar estos datos desde tu backend
const cities = ref([]); // Debes cargar estos datos desde tu backend

// Método para abrir el diálogo
function openAddNeighborhoodDialog() {
  showAddNeighborhoodDialog.value = true;
}

// Método para agregar el nuevo barrio
async function addNeighborhood() {
  try {
    const response = await fetch(`${URI}/neighborhoods`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newNeighborhood.value)
    });

    if (!response.ok) {
      throw new Error('Error al crear el barrio');
    }

    // Cerrar el diálogo y actualizar la lista de barrios
    showAddNeighborhoodDialog.value = false;
    // Aquí deberías también actualizar la lista de barrios para reflejar el nuevo
    console.log('Barrio agregado con éxito');
  } catch (error) {
    console.error('Error al agregar el barrio:', error);
  }
}






























const route = useRoute()


watch(site, (newValue, oldValue) => {
  // Asegurarse de que el nuevo valor tenga el 'neighborhood_id' antes de intentar navegar
  if (newValue && newValue.site_id !== undefined) {
    router.push(`/admin/domicilios/${31}`);
  }
}, { deep: true });


watch(() => route.path, () => {
    const site_id = route.params.site_id

    // Llama a getNeighborhoods cada vez que cambia la ruta
    getSites().then(data => {
        sites.value = data
        site.value = data.filter(s => s.site_id == site_id)[0]
    })
});



const getSites = async() => {
    try {
        const response = await fetch(`${URI}/sites`)

        if(response.ok) {
            const data = await response.json()
            return data

        }

        
    } catch (error) {
        
    }
}



onMounted( async() => {
    const site_id = route.params.site_id
    getSites().then(data => {
        sites.value = data
        site.value = data.filter(s => s.site_id == site_id)[0]
    })

   
})  






















</script>
        
<style scoped>
Button {
    font-weight: bold;
}

.vacaciones {
    display: flex;
    background-color: #64748B;
    justify-content: center;

}

.licencia {
    display: flex;
    background-color: #64748B;
    justify-content: center;
}

.general {
    display: flex;
    background-color: #64748B;
    justify-content: center;
}


.generado {
    display: flex;
    background-color: #eeff0060;
    justify-content: center;
}

* {
    overflow-wrap: break-word;
    white-space: normal;
    overflow: hidden;
}

.aprobado {
    display: flex;
    background-color: #2bff0060;
    justify-content: center;
}

.rechazado {
    display: flex;
    background-color: #ff000044;
    justify-content: center;
}

Button {
    text-transform: capitalize;
}



.Agendada {
    background-color: var(--yellow-200);
    border-radius: 5rem;
}

.Completada {
    background-color: var(--green-200);
    border-radius: 5rem;
}

.Cancelada {
    background-color: var(--red-200);
    border-radius: 5rem;
}
</style>