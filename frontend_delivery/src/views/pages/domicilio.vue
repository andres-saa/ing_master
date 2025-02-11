<template>



    <div>
        
    </div>
    
    
    
        <Dialog v-model:visible="showDialog" style="width: auto" header="Confirmar eliminación" :modal="true" :closable="false">
            <p>¿Estás seguro de que quieres eliminar este barrio?</p>
            <Button label="Cancelar" @click="showDialog = false" class="p-button-text" />
            <Button label="Eliminar" @click="deleteNeighborhood" class="p-button-danger" />
        </Dialog>
    
        <Dialog style="width: 45rem;" class="mx-2" v-model:visible="showCreateDialog" header="Crear Nuevo Barrio" :modal="true" :closable="false">
    
            <div class="   grid" style=" ">
    
    
                <div class=" col-12 my-0 pb-0">
                    <Dropdown style="width: 100%;" v-model="newNeighborhoodCity" :options="cities" optionLabel="city_name"
                        placeholder="Ciudad" />
                </div>
    
                <div class="col-12 my-0 ">
                    <Dropdown style="width: 100%;" v-model="newNeighborhoodSite" :options="sites?.filter(site => site.show_on_web)" optionLabel="site_name"
                        placeholder="Sede" />
    
                </div>
    
    
            </div>
    
            <Divider> Nuevos barrios </Divider>
    
            <div v-for="(barrio, index) in barriosToAdd" :key="index" class="my-3">
        <div class=" grid m-0" style="width: 100%; ">
            <div class="col-12 md:col-6 p-0 md:pr-2">
                <InputText style="width: 100%;" v-model="barrio.name" placeholder="Nombre del Barrio" />
            </div>
    
            <div class="col-11 md:col-5 p-0 md:pl-2 my-2 md:my-0" style="display: flex;justify-content: end;">
                <InputNumber  style="width: 100%;"  prefix="$" v-model="barrio.delivery_price" placeholder="Precio del Domicilio" />
            </div>
            
           
            <Button icon="pi pi-trash text-2xl p-0"  text class=" col-1 p-0 m-0" size="small" severity="danger" @click="removeBarrio(index)">
                
            </Button>
        </div>
    </div>
    
            <div class="col-12 pl-0">
                <Button text class="p-0" @click="() => {barriosToAdd.push({})}">
                    <i class="text-4xl" :class="PrimeIcons.PLUS_CIRCLE"></i>
    
                </Button>
            </div>
    
    
    
    
    
            <template #footer>
                <Button severity="danger" label="Cancelar" @click="showCreateDialog = false" class="p-button-text" />
                <Button severity="help" label="Crear" @click="createNeighborhood" class="p-button m-0" />
            </template>
        </Dialog>
    
        <div class="col-12 m-auto  p-0" style="max-width: 700px;">
    
    
    
            <div class="col-12 p-0 m-0" style="display: flex; justify-content: end; border: none;">
        <Button style="" raised   severity="help"  size="small" class="  m-0 my-0" label="Nuevo Barrio"
                                @click="showCreateDialog = true"></Button>
    </div>
    
            <DataTable :class="neighborhoods.length > 0? 'apear' : 'hide'" stripedRows ref="dt" :value="neighborhoods" v-model:selection="selectedneighborhoods" dataKey="id" :paginator="true"
                :rows="10" :filters="filters" showGridlines
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25, 100]"
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} neighborhoods" responsiveLayout="scroll"
                scrollable :frozenValue="lockedCustomers">
                <template  class="p-0" #header style="z-index:200;padding: 0;">
    
    
    
                     
    
    
    
                    <div class="flex p-0 flex-column md:flex-row md:justify-content-between md:align-items-center">
                        
    
                        <span class="block mt-2 md:mt-0 p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText class="" v-model="filters['global'].value" placeholder="Buscar..." />
                        </span>
                    </div>
                </template>

    
                <Column class="px-2 py-0 m-0" field="name" header="Barrio" :sortable="true"
                    headerStyle="width:max-content; min-width:15rem ">
                    <template #body="neighborhood">
                        <span class="p-column-title p-0">Code</span>
                      
                        <InputText   :onchange="() => update(neighborhood.data)" style="width:100%; border: none; border-radius: 0; border-radius: 0;"
                            v-model="neighborhood.data.name"></InputText>
    
                    </template>
                </Column>
    
               <Column class="px-2 py-0 m-0" field="delivery_price" header="Precio del domicilio" :sortable="true"
                    headerStyle="width:15rem;min-width:15rem ">
                    <template #body="neighborhood">
    
                   
                        <InputNumber prefix="$"  style="width:10%;height: 100%; border: none !important; border-radius: 0;border-radius: 0;" v-model="neighborhood.data.delivery_price"
                            @update:modelValue="() => update(neighborhood.data)"/>
                    </template>
                </Column>
    
     
                <Column field="actions" header="" class="p-0" style="" frozen alignFrozen="right">
                    <template #body="data">
                        <Button   class="p-button-rounded p-button-danger p-0" style="width: 2rem;display: flex;align-items: center;margin: auto; justify-content: center; aspect-ratio: 1 / 1;" @click="confirmDelete(data.data)" >
    
                            <i :class="PrimeIcons.TRASH">
                                
                            </i>
                        </Button>
                    </template>
                </Column>
    
    
    
            </DataTable>
    
    
    
        </div>
    </template>
            
            
    <script setup>
    
    import { ref, onMounted, onBeforeMount, watch } from 'vue'
    import { URI } from '@/service/conection';
    import Loading from '@/components/Loading.vue'
    
    import {useReportesStore} from '@/store/reportes.js'
    const store = useReportesStore()
    
    const guardando  = ref(false)
    const barriosToAdd = ref([{}])
    const removeBarrio = (index) => {
        if (barriosToAdd.value.length > 1){
            barriosToAdd.value.splice(index, 1);
    
        }
    };
    import { FilterMatchMode, PrimeIcons } from 'primevue/api';
    
    import { useToast } from 'primevue/usetoast';
    // import { departamentos, findByDepartament } from '@/service/CountryService.js'
    // import { jsPDF } from "jspdf";
    
    // import { uploadUserPhotoProfile } from '@/service/sendFileService'
    import {
    
        getSites
    
    } from '@/service/dropDownAux';
    
    // // import logo from '@/images/logo.png'
    // import { getUserRole } from '@/service/valoresReactivosCompartidos.js'
    // import * as XLSX from 'xlsx';
    
    const showCreateDialog = ref(false);
    const newNeighborhood = ref({
        neighborhood_id: 0,
        name: "",
        delivery_price: 0,
        site_id: 0,
        city_id: 0
    })
    
    
    
    const newNeighborhoodSite = ref(0)
    const newNeighborhoodCity = ref(0)
    
    
    watch(newNeighborhoodCity, ( nuevo, viejo) => {
        if (nuevo != viejo){
            getSitesByCity().then(s => {
                sites.value = s
                newNeighborhoodSite.value = sites.value[0]
            } )
           
        }
    })
    
    
    watch(showCreateDialog, ( nuevo, viejo) => {
        if (nuevo == true){
            newNeighborhoodCity.value = {}
            barriosToAdd.value=[{}]
        }
    })
    
    const createNeighborhood = async () => {
    
       
        showCreateDialog.value = false;
       store.setLoading(true,'guardando barrios')
       
       
        try {
            // Iterate over each new neighborhood
            await Promise.all(barriosToAdd.value.map(async (barrio) => {
                // Include site_id and city_id in each neighborhood object
                barrio.site_id = newNeighborhoodSite.value.site_id;
                barrio.city_id = newNeighborhoodCity.value.city_id;
    
                const response = await fetch(`${URI}/neighborhood`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(barrio)
                });
    
                if (!response.ok) {
                    throw new Error(`Error creating neighborhood: ${barrio.name}`);
                }
            }));
    
            // After all neighborhoods are successfully added
            toast.add({ severity: 'success', summary: 'Created', detail: 'All neighborhoods created successfully', life: 3000 });
    
            // Reset the barriosToAdd array and close the dialog
            barriosToAdd.value = [{}];
            
    
            // Optionally, you can fetch and update the neighborhoods list after creation
            await getNeighborhoods().then(barrio => neighborhoods.value = barrio);
            store.setLoading(false,'guardando barrios')
    
    
        } catch (error) {
            console.error('Request error:', error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create some neighborhoods', life: 3000 });
            store.setLoading(false,'guardando barrios')
    
        }
    };
    
    
    
    const cities = ref([])
    const getCities = async () => {
        try {
            // spinnersView.value.ciudad = true
            const response = await fetch(`${URI}/cities`)
            if (response.ok) {
                const data = await response.json()
                // spinnersView.value.ciudad = false
                // cities.value = data
                return data
            }
    
        } catch (error) {
            // spinnersView.value.ciudad = false
    
        }
    
    }
    const deleteNeighborhood = async () => {
        const options = {
            method: 'DELETE', // Método HTTP para la eliminación
        };
    
        try {
            const response = await fetch(`${URI}/neighborhood/${neighborhoodToDelete.value.neighborhood_id}`, options);
            if (!response.ok) {
                throw new Error('Error al eliminar el barrio');
            }
            // Actualiza tu estado o lista de barrios aquí, por ejemplo, refrescando la lista de barrios
            await getNeighborhoods().then(data => neighborhoods.value = data);
            showDialog.value = false; // Cierra el diálogo después de la eliminación
            toast.add({ severity: 'success', summary: 'Eliminado', detail: 'Barrio eliminado con éxito', life: 3000 });
        } catch (error) {
            console.error('Error en la petición:', error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar el barrio', life: 3000 });
        }
    };
    onMounted(async () => {
        getCities().then(data => cities.value = data)
    })
    
    const neighborhoods = ref([])
    const visibleLoading = ref(false)
    const showDialog = ref(false);
    const neighborhoodToDelete = ref({});
    
    const confirmDelete = (neighborhood) => {
        neighborhoodToDelete.value = neighborhood;
        showDialog.value = true;
    };
    
    
    
    const getNeighborhoods = async () => {
    
        const site_id = 31
    
        try {
           
            store.setLoading(true,'cargando barrios')
    
            const response = await fetch(`${URI}/neighborhoods/by-site/${site_id}`)
    
            if (!response.ok) {
                visibleLoading.value = false
                store.setLoading(false,'cargando barrios')
    
            }
            if (response.ok) {
                const data = await response.json()
                store.setLoading(false,'cargando barrios')
    
                // cities.value = data
                return data
            }
    
        } catch (error) {
            store.setLoading(false,'cargando barrios')
    
    
        }
    }
    
    
    const getSitesByCity = async () => {
    
    if (!newNeighborhoodCity.value?.city_id){
        return
    }
    
    const city_id = newNeighborhoodCity.value.city_id
    
    try {
        // visibleLoading.value = true
        const response = await fetch(`${URI}/sites/city/${city_id}`)
    
        if (!response.ok) {
            // visibleLoading.value = false
            store.setLoading(false,'cargando barrios')
    
    
        }
        if (response.ok) {
            const data = await response.json()
            // visibleLoading.value = false
            store.setLoading(false,'cargando barrios')
    
            // cities.value = data
            return data
        }
    
    } catch (error) {
        store.setLoading(false,'cargando barrios')
    
        // visibleLoading.value = false
    
    
    }
    }
    
    onMounted(async () => {
    
        getNeighborhoods().then(data => {
            neighborhoods.value = data
        })
    
    
    
    })
    
    onBeforeMount(() => {
        store.setLoading(false)
    })
    
    
    
    
    
    // const userId = ref( await getUserId())
    
    
    
    
    
    
    const selectedneighborhoods = ref()
    
    const filters = ref(null);
    
    const initFilters = () => {
        filters.value = {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS }
        };
    
    };
    
    
    
    
    
    onBeforeMount(() => {
        initFilters()
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    import { computed } from 'vue'
    // import { URI } from '@/service/conection';
    import { useRoute } from 'vue-router';
    import { getUserId } from '@/service/valoresReactivosCompartidos';
    import router from '@/router';
    import InputNumber from 'primevue/inputnumber';
    // import { getUserId } from '@/service/valoresReactivosCompartidos';
    // import { getUsers } from '@/service/userServices'
    // import { siteDropValues } from '@/service/valoresReactivosCompartidos';
    // import {
    //     sitesDropValues,
    //     GenderDropValues,
    //     PositionDropValues,
    //     maritalStatusDropValues,
    //     epsDropValues,
    //     educationLevelDropValues,
    //     employmentContractTypeDropValues,
    //     pantSizesDropValues,
    //     shirtSizesDropValues,
    //     bloodTypesDropValues,
    //     housingTypesDropValues,
    //     statusDropValues,
    //     vehicleTypesDropValues,
    //     findSiteById,
    //     findSiteByName,
    //     getSites
    
    // } from '@/service/dropDownAux';
    
    
    // import { useToast } from 'primevue/usetoast';
    const sending = ref(false)
    
    const incluirLink = ref(false);
    const toast = useToast();
    const route = useRoute()
    const allUsers = ref(false)
    const groupedUsersBySite = ref([]);
    const groupedUsersByPosition = ref([]);
    const neighborhood = ref({})
    
    const esURLValida = (url) => {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    };
    const newneighborhood = ref({})
    const charging = ref(true)
    const checked = ref(false)
    const toggleUsersSelectionBySite = (siteName, isSelected) => {
        const siteGroup = groupedUsersBySite.value.find(group => group.site_name === siteName);
        if (!siteGroup) return;
    
        let updatedSelectedUsers = [...usersSelected.value];
    
        siteGroup.employers.forEach(user => {
            const userIndex = updatedSelectedUsers.indexOf(user.id);
            if (isSelected && userIndex === -1) {
                updatedSelectedUsers.push(user.id);
            } else if (!isSelected && userIndex !== -1) {
                updatedSelectedUsers.splice(userIndex, 1);
            }
        });
    
        usersSelected.value = updatedSelectedUsers;
    };
    
    
    // const areAllSelected = computed(() => {
    //     const allUserIds = groupedUsersBySite.value.reduce((acc, group) => {
    //         return acc.concat(group.employers.map(user => user.id));
    //     }, []);
    
    //     return allUserIds.every(userId => usersSelected.value.includes(userId));
    // });
    
    
    
    const usersSelected = ref([]);
    
    const update = async (neighborhood) => {
    
    
        const options = {
            method: 'PUT', // Método HTTP
            headers: {
                'Content-Type': 'application/json', // Indica que el cuerpo de la petición es un JSON
            },
            body: JSON.stringify(neighborhood) // Convertir el objeto de datos a una cadena JSON
        };
    
        // Realizar la petición PUT
        fetch(`${URI}/neighborhood/${neighborhood.neighborhood_id}`, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('La petición ha fallado');
                }
                return response.json(); // Convertir la respuesta a JSON
            })
            .then(responseData => {
                console.log('Respuesta del servidor:', responseData); // Manejar la respuesta del servidor
            })
            .catch(error => {
                console.error('Error en la petición:', error); // Manejar errores de la petición
            });
    }
    
    
    const createAttendeesData = (training_id) => {
        // const training_id = route.params.neighborhood_id
        return {
            attendees: usersSelected.value.map(userId => ({
                training_id: training_id, // Asegúrate de que sea un número
                attendee_id: userId,
                assigned: false, // o el valor por defecto que desees
                attendance_time: new Date().toISOString() // o una fecha/hora específica si es necesario
            }))
        };
    };
    
    
    
    
    
    
    
    async function fetchGroupedUsersBySite() {
    
        try {
            const response = await fetch(`${URI}/employers/grouped-by-site`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            let data = await response.json();
    
            // Agrupar adicionalmente por posición dentro de cada sede
    
            data = data.map(group => {
                const groupedByPosition = group.employers.reduce((acc, curr) => {
                    acc[curr.position] = acc[curr.position] || [];
                    acc[curr.position].push(curr);
                    return acc;
                }, {});
                return { ...group, positions: groupedByPosition };
    
            });
    
            groupedUsersBySite.value = data;
            charging.value = false
    
    
    
        } catch (error) {
            console.error('Error al obtener usuarios agrupados por sede:', error);
        }
    }
    
    // Función para obtener usuarios agrupados por posición
    async function fetchGroupedUsersByPosition() {
        try {
            const response = await fetch(`${URI}/employers/grouped-by-position`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            groupedUsersByPosition.value = await response.json();
        } catch (error) {
            console.error('Error al obtener usuarios agrupados por posición:', error);
        }
    }
    
    
    
    const sites = ref([])
    
    
    onBeforeMount(() => {
    
        // initFilters();
        getSites().then(data => sites.value = data)
        // getAsistentes()
    });
    
    
    onMounted(async () => {
        // Cargar datos agrupados al montar el componente
        await fetchGroupedUsersBySite();
        await fetchGroupedUsersByPosition();
    });
    
    const toggleUserSelection = (userId) => {
        const index = usersSelected.value.indexOf(userId);
        if (index > -1) {
            usersSelected.value.splice(index, 1); // Elimina el ID si ya está presente
        } else {
            usersSelected.value.push(userId); // Agrega el ID si no está presente
        }
    };
    
    
    
    
    
    
    
    
    
    
    watch(() => route.path, () => {
        // Llama a getNeighborhoods cada vez que cambia la ruta
        getNeighborhoods().then(data => {
            neighborhoods.value = data
        })
    });
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
    
    input {
        overflow-wrap: break-word;
        white-space: normal;
        overflow: hidden;
        background: transparent;
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
    
    
    
    
    .loading-enter-active,.loading-leave-active {
      transition: all ease  .3s;
      
    }
    
    
    
     .loading-leave-to{
      opacity: 0;
      transform: translateY(20rem);
    
    }
    
    
    .loading-leave-from  {
      opacity: 1;
      transform: translateY(20rem);
    
    }
     /*
    */
    
     .loading-enter-from {
      opacity: 0;
      transform: translateY(20rem);
      filter: blur(10px);
      /* filter: blur(0); */
      
    }
    
    
    .loading-enter-to {
      opacity: 1;
      filter: blur(0);
    
      
    } 
    
    
    
    
    
    
    
    .apear{
      transition: .3s all ease;
      opacity:1;
      max-height: 100vh;
    }
    
    .hide{
      opacity: 0;
      min-height: 100vh;
      max-height: 0rem;
      overflow: hidden;
    
    }
    
    
    
    
    
    
    
    
    </style>