<template>
    <div class="col-12  m-0 p-0" style="background-color: transparent;border: none; ">



        <!-- Diálogo para confirmar eliminación de adicional -->
<Dialog header="Confirmación" v-model:visible="displayConfirmationAdicional" :style="{ width: '350px' }" :modal="true">
    <div class="flex align-items-center justify-content-center">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem"></i>
        <span>¿Seguro que desea eliminar <b>{{ adicionalParaBorrar.name }}</b>?</span>
    </div>
    <template #footer>
        <Button label="No" icon="pi pi-times" @click="closeConfirmationAdicional" class="p-button-text" />
        <Button label="Sí" icon="pi pi-check" @click="deleteAdicional(adicionalParaBorrar[ids[route.params.adicionales]])" class="p-button-text" autofocus />
    </template>
</Dialog>


<!-- Diálogo existente para confirmar eliminación de grupo -->
<Dialog header="Confirmación" v-model:visible="displayConfirmation" :style="{ width: '350px' }" :modal="true">
    <div class="flex align-items-center justify-content-center">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem"></i>
        <span>¿Seguro que desea eliminar <b>{{ grupoParaBorrar.name }}</b>?</span>
    </div>
    <template #footer>
        <Button label="No" icon="pi pi-times" @click="closeConfirmation" class="p-button-text" />
        <Button label="Sí" icon="pi pi-check" @click="deleteGrupoAdicional(grupoParaBorrar[grupoIds[route.params.adicionales]])" class="p-button-text" autofocus />
    </template>
</Dialog>

























        <div class=" p-0 lg:p-6" style=" border: none;">
            <p class="text-2xl titulo my-3" style="text-transform: capitalize; font-weight: bold;">grupos de {{ route.params.adicionales }} 
                
            </p> 
               
               <Button size="small" :severity="severity[route.params.adicionales]" class="mb-6" style="text-transform: capitalize; " @click="showAgregarGrupoAdicional = !showAgregarGrupoAdicional">Nuevo grupo de {{ route.params.adicionales }}</Button>
            
                <div class="col-12  grid  m-0 p-0" style="" >

                    <!-- {{ adicionales }} -->
                    <div class="col-12 md:col-12 p-0 m-0 mb-4 " style="background-color: ;" v-for=" Grupoadicional in grupoAdicionales">

                        
                        <div class="card m-0 grid col-12 p-1"  :style="`background-color:${pastelColors[route.params.adicionales]}`" style="position: relative;">

                            <p style="text-transform:capitalize;" class="text-xl mb-4 col-12"> <b>{{ Grupoadicional.name }}</b>
                            </p>
                            <Button size="small" severity="danger" @click="openConfirmation(Grupoadicional)" class="add-cart-btn text-xl" style="cursor: pointer; position: absolute;top: -1rem;right: 0rem; width: 2.5rem;height: 2.5rem;border-radius: 50%; display: flex; align-items: center; justify-content: center; border: none;">
                                
                                <i   class="icono text-2xl  p-0 m-0 " :class="PrimeIcons.TIMES"> </i> 
                            
                            </Button>


                           







                            <div style="text-transform: capitalize; border-right: 2px solid rgba(0, 0, 0, 0.144) ;" class="grid col-12 lg:col-6 mx-0 px-0"  st
                                v-for=" (adicional,index ) in  grupos[Grupoadicional[grupoIds[route.params.adicionales]]]">
                                <span class="col-9 text-left py-0"> {{ adicional.name }} <Button  @click="openEditar(adicional)" class="p-0" size="small" text label="Editar"></Button></span>
                                
                                <span class="col-3 text-right py-0"> {{ formatoPesosColombianos(adicional.price) }} </span>
                            </div>






                        </div>

                        






                    </div>

                    

                    



                </div>


                <div class="card col-12  p-4 " >

                    <p style="text-transform:capitalize;" class="text-xl mb-6 mt-3 "> <b>Todas las {{ route.params.adicionales
                    }}</b>
                    </p>


                    <div class=" grid">


                        <div style="text-transform: lowercase; text-transform:;" class="grid lg:col-6 col-12 px-0 py-3 mx-0"
                            v-for=" adicional in  adicionales">
                            <span style="" class="col-6 text-left py-0"> {{ adicional.name }} <Button  @click="openEditar(adicional)" class="p-0" size="small" text label="Editar"></Button> </span>
                            <span class="col-6 text-right py-0"> {{ formatoPesosColombianos(adicional.price) }} </span>
                        </div>

                        
                    </div>

                    <div class="col-12" style="display: flex; justify-content: center;">
                        <Button severity="info" size="small" style="text-transform: capitalize; "
                            @click="showAgregarAdicional = !showAgregarAdicional">Agregar</Button>

                    </div>
                   










                </div>

   
        </div>
    </div>



    <Dialog v-model:visible="showAgregarAdicional" modal="true" :style="{ width: '500px', height: 'max-content' }"
        header="Agregar" :modal="true" class="p-fluid p-2 m-3" style="   ; background-color: white;border-radius:1rem">


        <inputText class="mb-4" v-model="newAdicional.name"></inputText>
        <inputNumber class="mb-4" v-model="newAdicional.price"></inputNumber>

        {{ newAdicional }}
        <Button size="small" severity="info" style="text-transform: capitalize;" @click="enviarAdicional">Agregar</Button>
    </Dialog>



    <Dialog v-model:visible="dialogoEditarAdicional" modal="true" :style="{ width: '500px', height: 'max-content' }"
        :header="`EDITAR ${adicionalEditar.name}`" :modal="true" class="p-fluid p-2 m-3" style="   ; background-color: white;border-radius:1rem">


        <inputText class="mb-4" v-model="adicionalEditar.name"></inputText>
        <inputNumber class="mb-4" v-model="adicionalEditar.price"></inputNumber>

        <!-- {{ newAdicional }} -->
        <Button style="text-transform: capitalize;" @click="guardarAdicional(adicionalEditar[ids[route.params.adicionales]])">Guardar</Button>
    </Dialog>






    <Dialog v-model:visible="showAgregarGrupoAdicional" modal="true" :style="{ width: '500px', height: 'max-content' }"
        header="Agregar" :modal="true" class="p-fluid p-2 m-3" style="   ; background-color: white;border-radius:1rem">


        <h5>Nombre del grupo</h5>
        <inputText class="mb-4" v-model="newGrupoAdicional.name"></inputText>   
        <!-- <inputNumber class="mb-4" v-model="newAdicional.price"></inputNumber> -->
        
        <!-- {{ newGrupoAdicional }} -->

        <div v-for="adicional in adicionales" style="display: flex;">
        

        

        <!-- <checkbox v-model="newGrupoAdicional"  boolen="true"></checkbox> -->

        <Checkbox v-model="listAdicionales.lista[adicional[ids[route.params.adicionales]]]" binary :value="false" />

        <div class="grid col-12 p-0 pl-2">
            
            <div class="col-6"> {{ adicional.name }} </div>
            <div class="col-6 text-right"> {{ formatoPesosColombianos(adicional.price ) }} </div>
        
        </div>

        </div>
        <Button style="text-transform: capitalize;" @click="enviarGrupoAdicionales">Crear Grupo</Button>


        {{ listAdicionales }}
        {{ newGrupoAdicional }}
      
    </Dialog>




           
                <!-- <Button label="Delete" icon="pi pi-trash" class="p-button-danger" style="width: auto"  /> -->
                <Dialog header="Confirmation" v-model:visible="displayConfirmation" :style="{ width: '350px' }" :modal="true">
                    <div class="flex align-items-center justify-content-center">
                        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                        <span>Seguro que desea eliminar <b>{{ grupoParaBorrar.name  }}</b></span>
                    </div>
                    <template #footer>
                        <Button label="No" icon="pi pi-times" @click="closeConfirmation" class="p-button-text" />
                        <Button label="Si" icon="pi pi-check" @click="deleteGrupoAdicional(grupoParaBorrar[[grupoIds[route.params.adicionales]]])" class="p-button-text" autofocus />
                    </template>
                </Dialog>
     

</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { URI } from '../../../service/conection';
import { formatoPesosColombianos } from '../../../service/formatoPesos';
import { pastelColors } from '@/service/valoresReactivosCompartidos'
import { PrimeIcons } from 'primevue/api';
import { useReportesStore } from '../../../store/reportes';
const store = useReportesStore()
const adicionales = ref();
const grupoAdicionales = ref();
const grupos = ref([])
const route = useRoute();
const showAgregarAdicional = ref(false)
const showAgregarGrupoAdicional = ref(false)
const grupoParaBorrar = ref()
const dialogoEditarAdicional = ref()
const adicionalEditar = ref({})

const displayConfirmation = ref(false)
const newAdicional = ref({price:0})
const listAdicionales = ref({lista:{}})
const newGrupoAdicional = ref({grupo:[]})


const openEditar = (adicional) => {
    dialogoEditarAdicional.value = true
    adicionalEditar.value = adicional

}










// Referencias para manejar la eliminación de adicionales individuales
const adicionalParaBorrar = ref(null);
const displayConfirmationAdicional = ref(false);

// Función para abrir el diálogo de confirmación de eliminación de adicional
const openConfirmationAdicional = (adicional) => {
    adicionalParaBorrar.value = adicional;
    displayConfirmationAdicional.value = true;
}

// Función para cerrar el diálogo de confirmación de eliminación de adicional
const closeConfirmationAdicional = () => {
    displayConfirmationAdicional.value = false;
    adicionalParaBorrar.value = null;
}

// Función para eliminar un adicional individual
const deleteAdicional = async (adicional_id) => {
    const url = `${URI}/delete_aditional/${adicional_id}`;

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            closeConfirmationAdicional();
            getAdicionaes();
            getGrupoAdicionaes().then(data => data.map(dato => getGrupos(dato[grupoIds[route.params.adicionales]])));
        } else {
            throw new Error('Error al eliminar el adicional');
        }
    } catch (error) {
        console.error('Error al eliminar el adicional:', error);
    }
}

// Referencias para manejar la eliminación de grupos de adicionales (si no están ya)
const grupoParaBorrar = ref(null);
const displayConfirmation = ref(false);

// Función para abrir el diálogo de confirmación de eliminación de grupo
const openConfirmation = (grupo) => {
    grupoParaBorrar.value = grupo;
    displayConfirmation.value = true;
}

// Función para cerrar el diálogo de confirmación de eliminación de grupo
const closeConfirmation = () => {
    displayConfirmation.value = false;
}

// Función para eliminar un grupo de adicionales
const deleteGrupoAdicional = async (grupoId) => {
    const url = `${URI}/delete_aditional_category/${grupoId}`; // Utiliza el endpoint correcto

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            closeConfirmation();
            getAdicionaes();
            getGrupoAdicionaes().then(data => data.map(dato => getGrupos(dato[grupoIds[route.params.adicionales]])));
        } else {
            throw new Error('Error al eliminar el grupo de adicionales');
        }
    } catch (error) {
        console.error('Error al eliminar el grupo de adicionales:', error);
    }
}










const guardarAdicional = (adicional_id) => {

    ids[route.params.adicionales]
    const url = `${URI}/${route.params.adicionales}/${adicional_id}`;

    // Realizar la solicitud POST
    fetch(url, {
        method: 'PUT', // Método HTTP
        headers: {
            'Content-Type': 'application/json' // Indicar el tipo de contenido
        },
        body: JSON.stringify(adicionalEditar.value) // Convertir los datos a formato JSON
    })
        .then(response => response.json()) // Convertir la respuesta en JSON
        .then(json => {
            // console.log(json)
            dialogoEditarAdicional.value = false
            getAdicionaes()
            getGrupoAdicionaes().then(data => data.map(dato => getGrupos(dato[grupoIds[route.params.adicionales]])));
        } ) // Manejar la respuesta
        .catch(error => console.error('Error:', error));

}

watch(() => listAdicionales.value.lista, (nuevaLista) => {
  // Iterar sobre los ids y actualizar 'newGrupoAdicional' según sea necesario
  for (const id in nuevaLista) {
    const idEntero = parseInt(id); // Convierte el id a entero
    if (nuevaLista[id]) {
      // Si el id es 'true', agregarlo a 'newGrupoAdicional.grupo' como entero
      if (!newGrupoAdicional.value.grupo.includes(idEntero)) {
        newGrupoAdicional.value.grupo.push(idEntero);
      }
    } else {
      // Si el id es 'false', eliminarlo de 'newGrupoAdicional.grupo'
      const index = newGrupoAdicional.value.grupo.indexOf(idEntero);
      if (index !== -1) {
        newGrupoAdicional.value.grupo.splice(index, 1);
      }
    }
  }
}, { deep: true });




const openConfirmation = (grupo) => {
    grupoParaBorrar.value = grupo
    displayConfirmation.value = true
    // console.log(func)
}


const closeConfirmation = () => {
    displayConfirmation.value = false

    // console.log(func)
}


const deleteAdicional = () => {

    console.log('borrado')
}




const enviarAdicional = async () => {
    const url = `${URI}/${route.params.adicionales}`;

    // Realizar la solicitud POST
    fetch(url, {
        method: 'POST', // Método HTTP
        headers: {
            'Content-Type': 'application/json' // Indicar el tipo de contenido
        },
        body: JSON.stringify(newAdicional.value) // Convertir los datos a formato JSON
    })
        .then(response => response.json()) // Convertir la respuesta en JSON
        .then(json => {
            // console.log(json)
            showAgregarAdicional.value = false
            getAdicionaes()
        } ) // Manejar la respuesta
        .catch(error => console.error('Error:', error));

}


const enviarGrupoAdicionales = async () => {
    const url = `${URI}/grupo-${route.params.adicionales}`;

    // Realizar la solicitud POST

    const grupoToSend = {} 
    grupoToSend.name = newGrupoAdicional.value.name
    grupoToSend[grupoNames[route.params.adicionales]] = newGrupoAdicional.value.grupo

    // console.log(grupoToSend)

    fetch(url, {
        method: 'POST', // Método HTTP
        headers: {
            'Content-Type': 'application/json' // Indicar el tipo de contenido
        },
        body: JSON.stringify(grupoToSend) // Convertir los datos a formato JSON
    })
        .then(response => response.json()) // Convertir la respuesta en JSON
        .then(json => {
            console.log(json)
            showAgregarGrupoAdicional.value = false
            getAdicionaes()
            getGrupoAdicionaes().then(data => data.map(dato => getGrupos(dato[grupoIds[route.params.adicionales]])));

        } ) // Manejar la respuesta
        .catch(error => console.error('Error:', error));

}

const deleteGrupoAdicional = async (grupoId) => {
    const url = `${URI}/grupo-${route.params.adicionales}/${grupoId}`; // Assuming the ID is part of the URL

    // Realizar la solicitud DELETE
    fetch(url, {
        method: 'DELETE', // Método HTTP
        headers: {
            'Content-Type': 'application/json' // Indicar el tipo de contenido
        }
        // No body is needed for a typical DELETE request
    })
    .then(response => {
        if (response.ok) {
            displayConfirmation.value = false
            return response.json(); // Or handle the response as needed
        }
        throw new Error('Something went wrong');
        
    })
    .then(json => {
        // console.log(json);
        // Actualizar la UI o realizar acciones adicionales después de eliminar
        getAdicionaes();
        getGrupoAdicionaes().then(data => data.map(dato => getGrupos(dato[grupoIds[route.params.adicionales]])));
    })
    .catch(error => console.error('Error:', error));
}




const grupoIds = {
    salsas: "grupo_salsa_id",
    toppings: 'grupo_topping_id',
    cambios: 'grupo_cambio_id',
    acompanantes: 'grupo_acompanante_id',
    adicionales: 'grupo_id'
}

const ids = {
    salsas: "salsa_id",
    toppings: 'topping_id',
    cambios: 'cambio_id',
    acompanantes: 'acompanante_id',
    adicionales: 'adicional_id'
}

const grupoNames = {
    salsas: "salsas",
    toppings: 'toppings',
    cambios: 'cambios',
    acompanantes: 'acompanantes',
    adicionales: 'adicionales'
}







const getAdicionaes = async () => {
    try {
        store.setLoading(true, `cargando ${route.params.adicionales}`)
        const response = await fetch(`${URI}/${route.params.adicionales}`);
        const data = await response.json();
        adicionales.value = data;
        store.setLoading(false, `cargando ${route.params.adicionales}`)

    } catch (error) {
        console.error('Error fetching data: ', error);
    }
}


const getGrupoAdicionaes = async () => {
    try {
        store.setLoading(true, `cargando grupo de ${route.params.adicionales}`)
        const response = await fetch(`${URI}/grupo-${route.params.adicionales}`);
        const data = await response.json();
        grupoAdicionales.value = data;
        store.setLoading(false, `cargando ${route.params.adicionales}`)
        return data
        
    } catch (error) {
        console.error('Error fetching data: ', error);
    }
}


const getGrupos = async (id) => {
    try {
        const response = await fetch(`${URI}/grupo-${route.params.adicionales}/${id}/${route.params.adicionales}`);
        const data = await response.json();
        grupos.value[id] = data;
        return data
    } catch (error) {
        console.error('Error fetching data: ', error);
    }
}

// Observador que se activa cuando cambia el parámetro de la ruta
watch(() => route.params.adicionales, (newVal, oldVal) => {
    if (newVal !== oldVal) {
        getAdicionaes();
        getGrupoAdicionaes().then(data => data.map(dato => getGrupos(dato[grupoIds[route.params.adicionales]])));
    }
});



// Llamada inicial en el montaje del componente
onMounted(getAdicionaes);
onMounted(getGrupoAdicionaes);

onMounted(async () => {


    getGrupoAdicionaes().then(data => data.map(dato => getGrupos(dato[grupoIds[route.params.adicionales]])));

})





const severity = {
    adicionales:'success',
    salsas:'warning',
    toppings:'danger',
    cambios:'info',
    acompanantes:'help'
}



</script>


<style scoped>
.titulo::first-letter {}



* {
    text-transform: lowercase;
}

*::first-letter {
    text-transform: capitalize;
}
</style>