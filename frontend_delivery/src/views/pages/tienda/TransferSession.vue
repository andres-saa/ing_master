<template>
    <div class="container" style="margin-top: 7rem;">

        <p  class=" text-4xl text-center px-4" style="font-weight: bold; margin-top: 6rem;">
    <i class="fa-solid fa-truck-arrow-right"></i>
       Transferencias
    </p>

        <Dialog v-model:visible="cancelDialogVisible" closeOnEscape :closable="true" modal style="width: 30rem;">
            <template #header>
              <h3> <b>Rechazar orden</b> </h3>
            </template>

            <form @submit.prevent="resolve(false,cancelData.id,cancelData.reason)" style="display: flex;gap: 1rem; flex-direction: column;align-items:start">
        
              
              <Textarea style="resize: none; text-transform: lowercase; width:100%" id="reason" v-model="cancelData.reason" rows="5"
                placeholder="Porque desea rechazar esta solicitud?"></Textarea>
        
              <Button  style="width: 100%;border-radius:0.5rem" label="Rechazar" type="submit" class="p-button-danger" />

            </form>
        </Dialog>

        <Dialog v-model:visible="aceptDialogVisible" closeOnEscape :closable="true" modal style="width: 30rem;">
            <template #header>
              <h3> <b>Aprobar esta orden</b> </h3>
            </template>

            <form @submit.prevent="authoize(cancelData.order_id)" style="display: flex;gap: 1rem; flex-direction: column;align-items:start">
        
              
            
              <Button style="width: 100%;border-radius:0.5rem" label="Aprobar (Transferencia confirmada)" type="submit" class="p-button-success" />

            </form>
        </Dialog>

        <DataTable   :paginator="true" :rows="15" :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Transferencias"
          :rowsPerPageOptions="[5, 10, 25, 100]"
          scrollable
          scrollHeight="65vh"
        stripedRows style="" v-model:filters="filters" class="col-12 m-auto"
        :value="TransferRequests" tableStyle="min-width: 50rem;">
        <template #header>
            <div class="grid" style="align-items:center;justify-content: space-between;">
                <div class="col-12 md:col-6 p-3"> 
                    <span  class="text-xl" style="width: 100%;"> Transferencias pendientes <span style="text-transform: capitalize;"></span> </span>
                </div>

                <span class="md:mt-0 p-input-icon-right m-3">
                                <i class="pi pi-search" />
                                <InputText class="" v-model="filters['global'].value"
                                    placeholder="Buscar Solicitud..." />
                            </span>
            </div>
        </template>


        <Column style="" class="py-1 pl-0" field="order_id" header="ID orden" frozen />
        <!-- <Column style="" class="py-1 pl-0" field="Metodo de pago" header="ID orden" frozen /> -->
        <Column style="" class="py-1 pl-0" field="total_order_price" header="Monto de la orden"  >
            <template #body="data">
                {{formatToColombianPeso(data.data.total_order_price)   }}
            </template>
        </Column>


        <Column style="" class="py-1 pl-0" field="total_order_price" header="Hora"  >
            <template #body="data">
                {{ extraerHora(data.data.latest_status_timestamp ) }}
            </template>
        </Column>

        <Column style="" class="py-1 pl-0" field="delivery_price" header="Domicilio"  >
            <template #body="data">
                {{formatToColombianPeso(data.data.delivery_price)   }}
            </template>
        </Column>



        <Column style="" class="py-1 pl-0" field="Total" header="Total"  >
            <template #body="data">
                {{formatToColombianPeso(data.data.delivery_price + data.data.total_order_price)   }}
            </template>
        </Column>
        <!-- <Column style="" class="py-1 pl-0" field="Metodo de pago" header="ID orden" frozen /> -->



        
        <Column style="" class="py-1 pl-0" field="user_name" header="Cliente"  />

        <Column style="" class="py-1 pl-0" field="user_phone" header="Telefono cliente"  />
        <!-- <Column style="" class="py-1 pl-0" field="user_phone" header="ID orden" frozen /> -->
        



        <Column style="" class="py-1 px-0" field="date" header="Action" frozen alignFrozen="right">
            <template #body="data">

                <div style="display: flex;gap:0.5rem;">
                    
                        <Button size="" v-if="route.params.request_status != 'aprobadas'" @click="open(data.data)" style="height: 1.8rem;width: 2rem;" severity="info" class="p-1" icon="pi pi-eye" />

                        <Button size="" v-if="route.params.request_status != 'aprobadas'" @click="show(data.data.order_id)" style="height: 1.8rem;width: 2rem;" severity="success" class="p-1" icon="pi pi-check" />
                        <!-- <Button v-if="route.params.request_status != 'rechazadas'" @click="show(false,data.data.id)" style="height: 1.8rem;width: 2rem;background:var(--primary-color);border:none"  severity="danger" class="p-1"
                        icon="pi pi-times" /> -->

                    
                </div>
                
            </template>
        </Column>


    </DataTable>



    <DialogoPedido>

</DialogoPedido>

    </div>




</template>

<script setup>

import {ref,onMounted,onBeforeMount,watch,onUnmounted} from 'vue'
import {PathService} from '@/service/pathService.js'
import { formatToColombianPeso, salesReport } from '@/service/valoresReactivosCompartidos';
import OrderItem from '../cocina/OrderItem.vue';
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import DialogoPedido from '../cocina/DialogoPedido.vue';
import {useRoute} from 'vue-router'
import {orderService} from '@/service/menu/orderService.js'
import {loginStore} from '@/store/user.js'
import { useOrderStore } from '../../../store/order';
import { months } from 'moment-timezone';
import {formatDateTime, extraerHora} from '@/service/formating/formatDate.js'







const store = useOrderStore()



const open = (order) => {
    store.setVisible('currentOrder',true)
    store.setOrder(order)
}


const authoize = async( order_id) => {
    const responsible_id = userStore.rawUserData.id
    await orderService.authorizeOrder(order_id,responsible_id)
    aceptDialogVisible.value = false
    fetchTransferRequests();

}


const cancelDialogVisible = ref(false)
const TransferRequests = ref([])
const aceptDialogVisible =ref(false)
const userStore = loginStore()
const cancelData = ref({

})



const sonido1 = new Audio('/sound/pip1.wav')
const sonido2 = new Audio('/sound/pip2.wav')
const sonido3 = new Audio('/sound/pip3.wav')
const sonido4 = new Audio('/sound/pip4.wav')
const orderStore = useOrderStore()

const intervalId = ref(null); // Guardar la referencia al intervalo

const requestMethods = {
    
    "revisar": orderService.getPendientsCancellationRequest,
    "aprobadas":orderService.getaceptedCancellationAcepted,
    "rechazadas":orderService.getPendientsCancellationRejected
}




const requestMethodsNoLoading = {
    
    "revisar": orderService.getPendientsCancellationRequestNoLoading,
    "aprobadas":orderService.getaceptedCancellationAceptedNoLoading,
    "rechazadas":orderService.getPendientsCancellationRejectedNoLoading
}



onBeforeMount(() => {
    initFilters();

});



watch(() => store.numberTransferRequests, () => {
    fetchTransferRequests();
  
})


const show = (id) => {
    
    aceptDialogVisible.value = true
    cancelData.value.order_id = id

}


const resolve = async(desition,id,observation) => {
 const  data = {
        "authorized": desition,
        "responsible_id": userStore.rawUserData.id,
        "responsible_observation": cancelData.value.reason || 'sin observaciones'
    }

    await orderService.resolveCancellationRequest(id,data)
    aceptDialogVisible.value = false
    cancelDialogVisible.value = false
    TransferRequests.value = await requestMethods['revisar']()


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



const route = useRoute()

const filters = ref()
const initFilters = () => {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    };
};

initFilters();

onMounted(() => {
    // Ejecutar inicialmente al montar el componente
    fetchTransferRequests();

    // Configurar el intervalo para actualizar los datos cada 10 segundos
    // intervalId.value = setInterval(() => {
    //     fetchTransferRequestsNoLoading();
    // }, 10000);



    


















});









onMounted(async() => {
    // Ejecutar inicialmente al montar el componente
    fetchTransferRequests();


});





















// Función para cargar las solicitudes de cancelación
const fetchTransferRequests = async () => {
    TransferRequests.value = await orderService.getOrdersTransfer();

};

const fetchTransferRequestsNoLoading = async () => {
    TransferRequests.value = await orderService.getOrdersTransferNoLoading();

};

const sounds = [sonido1, sonido2, sonido3]; // Array de sonidos

// const fetchTransferRequestsNoLoading = async () => {
//     TransferRequests.value = await requestMethodsNoLoading['revisar']();
//     const currentNumberCansellationRequests = orderStore.numberTransferRequests;
//     const newCansellationResquestNumber = TransferRequests.value.length;

//     if (currentNumberCansellationRequests < newCansellationResquestNumber) {
//         const randomSoundIndex = Math.floor(Math.random() * sounds.length); // Genera un índice aleatorio
//         sounds[randomSoundIndex].play(); // Reproduce el sonido seleccionado al azar

//         orderStore.numberTransferRequests = newCansellationResquestNumber; // Actualiza el store
//     }
// };


const isActive = PathService.isActiveRoute

watch(()=> route.params.request_status, async() => {
    TransferRequests.value = await requestMethods['revisar']()
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


</style>