<template>
    <div class="container"  ref="reuqests">


        <Dialog v-model:visible="cancelDialogVisible" closeOnEscape :closable="true" modal style="width: 30rem;">
            <template #header>
              <h3> <b>Rechazar esta solicitud</b> </h3>
            </template>

            <form @submit.prevent="resolve(false,cancelData.id,cancelData.reason)" style="display: flex;gap: 1rem; flex-direction: column;align-items:start">
        
              
              <Textarea style="resize: none; text-transform: lowercase; width:100%" id="reason" v-model="cancelData.reason" rows="5"
                placeholder="Porque desea rechazar esta solicitud?"></Textarea>
        
              <Button  style="width: 100%;border-radius:0.5rem" label="Rechazar" type="submit" class="p-button-danger" />

            </form>
        </Dialog>

        <Dialog v-model:visible="aceptDialogVisible" closeOnEscape :closable="true" modal style="width: 30rem;">
            <template #header>
              <h3> <b>Aprobar esta solicitud</b> </h3>
            </template>

            <Dropdown v-model="selectedCancellationCategorie" optionLabel="name" :options="cancellationCategories" placeholder="CATEGORIA DE LA CANCELACION" class="mb-3" style="width: 100%;">
                
            </Dropdown>

            <form @submit.prevent="resolve(true,cancelData.id,cancelData.reason)" style="display: flex;gap: 1rem; flex-direction: column;align-items:start">
        
              
              <Textarea style="resize: none; text-transform: lowercase; width:100%" id="reason" v-model="cancelData.reason" rows="5"
                placeholder="Notas para el solicitante"></Textarea>
        
              <Button style="width: 100%;border-radius:0.5rem" label="Aprobar" type="submit" class="p-button-success" />

            </form>
        </Dialog>

        <DataTable   :paginator="true" :rows="15" :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} solicitudes"
          :rowsPerPageOptions="[5, 10, 25, 100]"
          scrollable
          scrollHeight="65vh"
        stripedRows style="" v-model:filters="filters" class="col-12 m-auto"
        :value="cancellationRequests" tableStyle="min-width: 50rem;">
        <template #header>
            <div class="grid" style="align-items:center;justify-content: space-between;">
                <div class="col-12 md:col-6 p-3"> 
                    <span  class="text-xl" style="width: 100%;"> Solicitudes de cancelacion - <span style="text-transform: capitalize;">{{route.params.request_status.split('-').join(' ')}}</span> </span>
                </div>

                <span class="md:mt-0 p-input-icon-right m-3">
                                <i class="pi pi-search" />
                                <InputText class="" v-model="filters['global'].value"
                                    placeholder="Buscar Solicitud..." />
                            </span>
            </div>
        </template>


        <Column style="" class="py-1 pl-0" field="order_id" header="ID orden" frozen>
        
        
        <template #body="data">

            <p style="min-width: max-content;"> {{ data.data.order_id }}</p>

        </template>
    </Column>
        

        <!-- <Column class="py-1" field="id" header="ID"></Column> -->
        <Column class="py-1" field="site_name" header="Sede"></Column>
        <Column class="py-1" field="site_name" header="Fecha">
        
            <template #body="data">
            
                <p style="min-width: max-content;">{{ buildData(data.data.timestamp).date }}</p>
            
            </template>
        
        </Column>

        <Column class="py-1" field="site_name" header="Hora">
        
        <template #body="data">
        
            <p style="min-width: max-content;">{{ buildData(data.data.timestamp).time }}</p>
        
        </template>
    
    </Column>


        <Column style="min-width: 15rem;" class="py-1" field="cancellation_categorie" header="Categoria">
        
            <template #body="data">
                <Tag :style="`background-color:${idColors[data.data.cancellation_category_id] } ;`" v-if="data.data.cancellation_categorie">{{ data.data.cancellation_categorie }}</Tag>
            </template>
        </Column>

        <Column style="min-width: 30rem;" class="py-1" field="reason" header="Motivo"></Column>
        <Column style="min-width: 30rem;" class="py-1" field="responsible_observation" header="Observacion Call center"></Column>


        <Column style="min-width: 10rem;" class="py-1" field="responsible" header="Quien solicita?"></Column>
        <Column style="min-width: 20em;" class="py-1" field="user_name" header="Nombre del cliente"></Column>
        <Column style="min-width: 10rem;" class="py-1" field="user_phone" header="Cel. cliente"></Column>


        <Column style="" class="py-1 px-0" field="date" header="Action" frozen alignFrozen="right">
            <template #body="data">

                <div style="display: flex;gap:0.5rem;">
                  
                        <Button size="" v-if="route.params.request_status != 'aprobadas'" @click="show(true,data.data.id)" style="height: 1.8rem;width: 2rem;" severity="success" class="p-1" icon="pi pi-check" />
                        <Button v-if="route.params.request_status != 'rechazadas'" @click="show(false,data.data.id)" style="height: 1.8rem;width: 2rem;background:var(--primary-color);border:none"  severity="danger" class="p-1"
                        icon="pi pi-times" />

                    
                </div>
                
            </template>
        </Column>


    </DataTable>





    </div>

</template>

<script setup>

import {ref,onMounted,onBeforeMount,watch,onUnmounted} from 'vue'
import {PathService} from '@/service/pathService.js'
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import {useRoute} from 'vue-router'
import {orderService} from '@/service/menu/orderService.js'
import {loginStore} from '@/store/user.js'
import { useOrderStore } from '../../../store/order';
import { months } from 'moment-timezone';
const cancelDialogVisible = ref(false)
const cancellationRequests = ref([])
const aceptDialogVisible =ref(false)
const userStore = loginStore()
const cancelData = ref({

})
const cancellationCategories = ref ([])
const selectedCancellationCategorie = ref({})

const idColors = ref({
    1: '#27ae60', // Verde Vibrante
    2: '#3498db', // Azul Claro
    3: '#f1c40f', // Amarillo Soleado
    4: '#e74c3c', // Rojo Intenso
    5: '#9b59b6'  // Púrpura Suave
})

const sonido1 = new Audio('/sound/pip1.wav')
const sonido2 = new Audio('/sound/pip2.wav')
const sonido3 = new Audio('/sound/pip3.wav')

const orderStore = useOrderStore()

const intervalId = ref(null); // Guardar la referencia al intervalo

const requestMethods = {
    
    "revisar": orderService.getPendientsCancellationRequest,
    "aprobadas":orderService.getaceptedCancellationAcepted,
    "rechazadas":orderService.getPendientsCancellationRejected
}


watch(cancellationRequests, async() => {
    const element = reuqests.value
    console.log(element)
    element.classList.remove('animator')
    element.classList.add('animator')
}, {deep:true})



const requestMethodsNoLoading = {
    
    "revisar": orderService.getPendientsCancellationRequestNoLoading,
    "aprobadas":orderService.getaceptedCancellationAceptedNoLoading,
    "rechazadas":orderService.getPendientsCancellationRejectedNoLoading
}



onBeforeMount(() => {
    initFilters();

});



const show = (desition,id) => {
    
    cancelData.value.id = id
    desition? aceptDialogVisible.value = true : cancelDialogVisible.value = true

}


const resolve = async(desition,id) => {
 const  data = {
        "authorized": desition,
        "responsible_id": userStore.rawUserData.id,
        "responsible_observation": cancelData.value.reason || 'sin observaciones',
        "category_id":selectedCancellationCategorie.value.id || 5
    }

    await orderService.resolveCancellationRequest(id,data)
    aceptDialogVisible.value = false
    cancelDialogVisible.value = false
    cancellationRequests.value = await requestMethods[route.params.request_status]()


}




const buildData = (timestamp) => {
    const monthsStr = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    const parts = timestamp.split('T');
    const dateParts = parts[0].split('-');

    const day = dateParts[2];
    const month = parseInt(dateParts[1], 10) - 1;  // Convertir a entero y ajustar índice
    const year = dateParts[0];

    const monthStr = monthsStr[month];
    const timeParts = parts[1].split(':');
    const hour = parseInt(timeParts[0], 10);  // Hora en formato de 24 horas
    const minute = timeParts[1];

    const isPM = hour >= 12;
    const formattedHour = hour % 12 || 12;  // Convierte la hora a formato 12 horas y ajusta medianoche a 12
    const paddedHour = formattedHour < 10 ? `0${formattedHour}` : `${formattedHour}`; // Agrega cero si es necesario
    const amPm = isPM ? 'PM' : 'AM';

    return {
        date: `${day}-${monthStr}-${year}`,
        time: `${paddedHour}:${minute} ${amPm}`
    };
}


const  reuqests = ref(null)
const route = useRoute()

const filters = ref()
const initFilters = () => {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    };
};

initFilters();

onMounted(async() => {
    // Ejecutar inicialmente al montar el componente
    fetchCancellationRequests();

    // Configurar el intervalo para actualizar los datos cada 10 segundos
    intervalId.value = setInterval(async() => {
        const recent_cancellation = await orderService.is_recent_order_generated()
        if (recent_cancellation && orderStore.numberCancellationRequests != recent_cancellation) {
            const randomSoundIndex = Math.floor(Math.random() * sounds.length); // Genera un índice aleatorio
            sounds[randomSoundIndex].play(); // Reproduce el sonido seleccionado al azar
            orderStore.numberCancellationRequests = recent_cancellation; // Actualiza el store
        fetchCancellationRequestsNoLoading();
        }
    }, 10000);


    cancellationCategories.value = await orderService.getCancellationCategories()




});



// Función para cargar las solicitudes de cancelación
const fetchCancellationRequests = async () => {
    cancellationRequests.value = await requestMethods[route.params.request_status]();

};


const sounds = [sonido1, sonido2, sonido3]; // Array de sonidos

const fetchCancellationRequestsNoLoading = async () => {
    const method = route.params.request_status || 'revisar'
    cancellationRequests.value = await requestMethodsNoLoading[method]();

    
};


const isActive = PathService.isActiveRoute

watch(()=> route.params.request_status, async() => {
    cancellationRequests.value = await requestMethods[route.params.request_status]()
},{deep:true})





</script>

<style scoped>

ul{
    display: flex;
    justify-content: center;
    overflow-x: auto;
    gap: 1rem;
}

@media (width < 600px) {
    
    ul{

        justify-content: start;
        padding:  0.5rem 0;
     
    }
    
}

.nav-bar--item{
    padding-bottom: 0.3rem;
}


.nav-bar{
    margin: auto;
    width: min-content;
    background-color: rgb(255, 255, 255);
    padding: 0;


    position: sticky;
    top:3rem;
    width: 100%;
    z-index: 99;
}
li{
    list-style:none;  
}

.container{
    margin-top: 3rem;
    position: relative;

}


.nav-var--item-button{
    color:gray;
    border-radius: 0%;
    padding: 0.5rem ;
    min-width: max-content;
}

.nav-var--item-button-selected{
    box-shadow: 0 0.3rem var(--primary-color);
    color: black;
}


@keyframes identifier {

0%{
    opacity: 0;

}

100%{
    opacity: 1;
}

}






.animator{
animation: identifier 1s ease  ;
}

</style>