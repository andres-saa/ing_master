<template>
    <div class="px-3" style="">
        <div class="p-2 mx-auto"
            style=" max-width: 540px;overflow: hidden;background-color: var(--primary-color);border-bottom: 2px solid #00000050; border-radius: .5rem .5rem 0 0;  box-shadow:  0 1rem 1rem #00000030;overflow: hidden; gap: 1rem; padding:  0 3rem;margin: auto;display: flex;justify-content: space-between;align-items: center;">
            <p class="text-center pl-3 text-xl p-0 m-0"
                style="font-weight: bold;width:min-content;color: white; gap: 1rem; align-items: center;">
                SABORES
            </p>

            <div style="display: flex;gap: .5rem;align-items: center;">
                <Button @click="visibleDialogAddFlavor = true" icon="pi pi-plus" size="small"
                    style="height: 2.5rem;background-color: var(--primary-color);border: none;border-radius: .3rem;r"
                    label="Nuevo sabor"></Button>

                    <h6 class="m-0 text-white p-0">|</h6>
                <Button @click="visibleDialogAddFlavorGroup = true" icon="pi pi-plus" size="small"
                    style="height: 2.5rem;background-color: var(--primary-color);border: none;border-radius: .3rem;r"
                    label="Nuevo Grupo"></Button>
            </div>

        </div>


    </div>


    <div class="m-auto col-12 m-0 p-0" style="max-width: 540px;box-shadow:  0 1rem 1rem #00000030; border-bottom: 2px solid #00000050; overflow: hidden;" v-for="grupo in flavors">
        <div class="my-1 px-2" style="display: flex;justify-content: space-between;align-items: center;gap: 1rem;">

            <Button @click="visible_groups[grupo.group_id] = !visible_groups[grupo.group_id]" text  style="color: var(--primary-color)"> <b> 
                
                

                <i v-if="visible_groups[grupo.group_id]" class="pi pi-angle-up text-2xl"></i> 
                <i v-else class="pi pi-angle-down text-2xl"></i> 
            
            
            </b>  </Button>


            <Tag style="width: 1rem;height: 1rem; border-radius:50%;" severity="success" v-if="grupo.gaseosa"></Tag>
            <h6 class="text-center text-xl m-0" style="font-weight: bold;text-transform: capitalize;">{{
                grupo.group_name }}</h6>

            <b><i class="pi pi-arrow-left"> </i></b>
            <div style="display: flex;gap: .5rem;justify-content: end;">
                <Button @click="openFalvorGroupEdit(grupo)" style="width: 2.5rem;height: 2.5rem;border-radius: .3rem;"
                    severity="warning" class="p-1 m-0" rounded icon=" pi pi-pencil"></Button>
                <Button v-if="!grupo.gaseosa" @click="openGroupDeleteDialog(grupo)" style="width: 2.5rem;height: 2.5rem;border-radius: .3rem;" severity="danger" class="p-1" rounded
                    icon=" pi pi-trash"></Button>
            </div>

        </div>




        <DataTable v-if="visible_groups[grupo.group_id]" showGridlines stripedRows :value="grupo?.flavors">
            <Column style="text-transform: capitalize;" class="p-0 px-2" field="aditional_item_name" header="NOMBRE">

                <template #body="adicion">

                    <h6 class="m-0 " style="text-transform: uppercase;"> {{ adicion.data.flavor_name }} </h6>

                </template>

            </Column>


            <Column class="p px-2 " field="aditional_item_price" header="PRECIO"
                style="text-transform: capitalize;display: flex;justify-content: center;">
                <template #body="adicion">
                    <h6 class="m-0" style="font-weight: bold;text-align: end;" v-if="adicion.data.flavor_price != 0">
                        {{ formatoPesosColombianos(adicion.data.flavor_price) }}
                    </h6>
                </template>

            </Column>



            <Column class="p-0 py-1 pl-3 px-2" field="" header="PREMIUM">

                <template #body="adicion">
                    <Tag style="border-radius: .2rem;" v-if="adicion.data.is_premium" severity="success"> Premium</Tag>
                </template>
            </Column>




            <Column style="width: 2rem;" class="p-0  py-1 pl-3 px-2" header="Interactuar">
                <template #body="adicion">
                    <div style="display: flex;gap: .5rem;justify-content: end;">
                        <Button @click="openFlavorEdit(adicion.data)"
                            style="width: 2.5rem;height: 2.5rem;border-radius: .3rem;" severity="warning"
                            class="p-1 m-0" rounded icon=" pi pi-pencil"></Button>



                        <Button @click="openFlavorDeleteDialog(adicion.data)" style="width: 2.5rem;height: 2.5rem;border-radius: .3rem;" severity="danger" class="p-1"
                            rounded icon=" pi pi-trash"></Button>
                    </div>
                </template>
            </Column>
        </DataTable>
    </div>



    <Dialog v-model:visible="visibleDialogEditFlavor" header="Editar sabor" modal style="width: 30rem;">


        <div class="py-3">

            <div style="display: flex;gap: 1rem;flex-direction: column;">


                <h6 class="m-0 p-0"><b>Nombre</b> </h6>
                <InputText v-model="falvor_to_edit.flavor_name" style="width: 100%;"></InputText>
                <h6 class="m-0 p-0"><b>precio</b> </h6>
                <InputNumber v-model="falvor_to_edit.flavor_price" prefix="$ " style="width: 100%;"></InputNumber>

                <!-- <div style="display: flex;justify-content: space-between;align-items: center;">
                    <h6 class="m-0 p-0"><b>premium</b> </h6>
                    <InputSwitch v-model="falvor_to_edit.is_premium"></InputSwitch>
                </div> -->

            </div>
        </div>

        <template #footer>
            <div style="display: flex;justify-content: end;">

                <Button @click="edit_flavor()"
                    style="background-color: var(--primary-color);border: none;border-radius: .3rem;"
                    label="Guardar"></Button>
            </div>
        </template>

    </Dialog>

    <Dialog v-model:visible="visibleDialogDeleteFlavor" header="Eliminar sabor" modal style="width: 30rem;">
    <p>¿Estás seguro de que deseas eliminar el sabor <b>{{ flavorToDelete.flavor_name }}</b>?</p>
    <template #footer>
        <div style="display: flex;justify-content: end;">
            <Button @click="visibleDialogDeleteFlavor = false" label="Cancelar" class="p-button-text" />
            <Button @click="deleteFlavor" label="Eliminar" severity="danger" style="margin-left: 1rem;" />
        </div>
    </template>
</Dialog>


<Dialog v-model:visible="visibleDialogDeleteFlavorGroup" header="Eliminar grupo" modal style="width: 30rem;">
    <p>¿Estás seguro de que deseas eliminar el grupo <b>{{ groupToDelete.group_name }}</b>?</p>
    <template #footer>
        <div style="display: flex;justify-content: end;">
            <Button @click="visibleDialogDeleteFlavorGroup = false" label="Cancelar" class="p-button-text" />
            <Button @click="deleteFlavorGroup" label="Eliminar" severity="danger" style="margin-left: 1rem;" />
        </div>
    </template>
</Dialog>



    <Dialog v-model:visible="visibleDialogAddFlavorGroup" header="Nuevo grupo de sabores" modal style="width: 30rem;">


        <div class="py-3">

            <div style="display: flex;gap: 1rem;flex-direction: column;">

                <h6 class="m-0 p-0"><b>Nombre</b> </h6>
                <InputText v-model="new_flavor_group.name" style="width: 100%;"></InputText>

            </div>
        </div>

        <template #footer>
            <div style="display: flex;justify-content: end;">

                <Button @click="create_flavor_group()"
                    style="background-color: var(--primary-color);border: none;border-radius: .3rem;"
                    label="Guardar"></Button>
            </div>
        </template>

    </Dialog>



    <Dialog v-model:visible="visibleDialogAddFlavor" header="Nuevo sabor" modal style="width: 30rem;">


        <div class="py-3">

            <div style="display: flex;gap: 1rem;flex-direction: column;">
                <h6 class="m-0 p-0"><b>Grupo</b> </h6>
                <Dropdown v-model="new_flavor.flavor_group_id" optionLabel="name" optionValue="id"
                    :options="types_flavor">
                </Dropdown>
                <h6 class="m-0 p-0"><b>Nombre</b> </h6>
                <InputText v-model="new_flavor.name" style="width: 100%;"></InputText>
                <h6 class="m-0 p-0"><b>precio</b> </h6>
                <InputNumber v-model="new_flavor.price" prefix="$ " style="width: 100%;"></InputNumber>

                <!-- <div style="display: flex;justify-content: space-between;align-items: center;">
                    <h6 class="m-0 p-0"><b>premium</b> </h6>
                    <InputSwitch v-model="new_flavor.premium"></InputSwitch>
                </div> -->

            </div>
        </div>

        <template #footer>
            <div style="display: flex;justify-content: end;">

                <Button @click="create_flavor()"
                    style="background-color: var(--primary-color);border: none;border-radius: .3rem;"
                    label="Guardar"></Button>
            </div>
        </template>

    </Dialog>



    <Dialog v-model:visible="visibleDialogEditFlavorGroup" header="Editar grupo" modal style="width: 30rem;">


        <div class="py-3">

            <div style="display: flex;gap: 1rem;flex-direction: column;">

                <h6 class="m-0 p-0"><b>Nombre</b> </h6>
                <InputText v-model="group_to_edit.group_name" style="width: 100%;"></InputText>

            </div>
        </div>

        <template #footer>
            <div style="display: flex;justify-content: end;">

                <Button @click="edit_flavor_group()"
                    style="background-color: var(--primary-color);border: none;border-radius: .3rem;"
                    label="Guardar"></Button>
            </div>
        </template>

    </Dialog>


</template>

<script setup>
import { adicionalesService } from '@/service/restaurant/aditionalService';
import { onMounted, ref, watch } from 'vue';
import { formatoPesosColombianos } from '../../../service/formatoPesos';
import { useRoute } from 'vue-router';
import { useSitesStore } from '../../../store/site';
import { nextTick } from 'vue';
import { fetchService } from '@/service/utils/fetchService.js'
import { URI } from '../../../service/conection';

const siteStore = useSitesStore()
const route = useRoute()


const visibleDialogAddFlavor = ref(false)
const visibleDialogAddFlavorGroup = ref(false)
const visibleDialogEditFlavor = ref(false)
const visibleDialogEditFlavorGroup = ref(false)




const visibleDialogDeleteFlavor = ref(false);
const visibleDialogDeleteFlavorGroup = ref(false);

const flavorToDelete = ref({});
const groupToDelete = ref({});

const openFlavorDeleteDialog = (flavor) => {
    flavorToDelete.value = { ...flavor };
    visibleDialogDeleteFlavor.value = true;
};

const openGroupDeleteDialog = (group) => {
    groupToDelete.value = { ...group };
    visibleDialogDeleteFlavorGroup.value = true;
};

const deleteFlavor = async () => {
    try {
        await fetchService.delete(`${URI}/delete_flavor/${flavorToDelete.value.flavor_id}`);
        update();
        visibleDialogDeleteFlavor.value = false;
    } catch (error) {
        console.error('Error eliminando el sabor:', error);
        alert('Hubo un error eliminando el sabor.');
    }
};

const deleteFlavorGroup = async () => {
    try {
        await fetchService.delete(`${URI}/delete_flavor_group/${groupToDelete.value.group_id}`);
        update();
        visibleDialogDeleteFlavorGroup.value = false;
    } catch (error) {
        console.error('Error eliminando el grupo:', error);
        alert('Hubo un error eliminando el grupo.');
    }
};



const types_flavor = ref({})

const new_flavor = ref({
    name: '',
    price: 0,
    flavor_group_id: null
})

const new_flavor_group = ref({
    name: ''
})


const visible_groups = ref({})

const group_to_edit = ref({})
const falvor_to_edit = ref({})



const openFlavorEdit = (falvor) => {

    falvor_to_edit.value = {...falvor}
    visibleDialogEditFlavor.value = true
}


const openFalvorGroupEdit = (grup) => {

    group_to_edit.value = {...grup}
    visibleDialogEditFlavorGroup.value = true
}


const flavors = ref({});


const create_flavor = async () => {
   
     if (!new_flavor.value.name || !new_flavor.value.flavor_group_id ) {

        alert("Llena los datos obligatorios")

     }

     console.log(new_flavor.value)

    
    const data = {
        name:new_flavor.value.name,
        price:new_flavor.value.price || 0
    }


    await fetchService.post(`${URI}/create-flavor/${new_flavor.value.flavor_group_id}`,data)
    update()
    visibleDialogAddFlavor.value = false
     
}


const create_flavor_group = async () => {

    if (!new_flavor_group.value.name) {
        alert("No puedes crear un grupo sin nombre")
    }

    await fetchService.post(`${URI}/create-flavor-grouped`, new_flavor_group.value)
    update()
    visibleDialogAddFlavorGroup.value = false
}



const edit_flavor_group = async () => {

    if (!group_to_edit.value.group_name) {
        alert("No puedes crear un grupo sin nombre")
    }

    const data = {
        name:group_to_edit.value.group_name,
        id:group_to_edit.value.group_id
    }

    console.log(group_to_edit.value)

    await fetchService.post(`${URI}/edit-flavor-grouped`, data)
    update()
    visibleDialogEditFlavorGroup.value = false
}



const edit_flavor = async () => {

if (!falvor_to_edit.value.flavor_name) {
    alert("No puedes crear un grupo sin nombre")
}

const data = {
    name:falvor_to_edit.value.flavor_name,
    price:falvor_to_edit.value.flavor_price
}

await fetchService.post(`${URI}/edit-flavor/${falvor_to_edit.value.flavor_id}`, data)
    update()
    visibleDialogEditFlavor.value = false

}


const update = async () => {
    flavors.value = await fetchService.get(`${URI}/get-flavor-grouped`);
    types_flavor.value = await fetchService.get(`${URI}/get-aditional-category`)
}


onMounted(async () => {
    await update()
});







const updateStatus = async (aditional_item_instance_id, status) => {
    try {
        const updateData = { status }; // This can be expanded to include other fields if necessary
        const result = await adicionalesService.toggleAditionalStatus(aditional_item_instance_id, updateData);
        if (!result) {
            throw new Error("Failed to update the status");
        }
        console.log('Status updated successfully:', result);
    } catch (error) {
        console.error('Error updating status:', error);
    }
}





watch(() => route.path, async () => {
    if (route.params.category_id) {
        flavors.value = await adicionalesService.getAllAditions();
        await nextTick();
    }
}, { deep: true });


watch(() => siteStore.site, async () => {
    if (siteStore.site) {
        flavors.value = await adicionalesService.getAllAditions();
        await nextTick();
    }
}, { deep: true });


watch(visibleDialogAddFlavor,() => {
    new_flavor.value = {}

})

watch(visibleDialogAddFlavorGroup, () => {
    new_flavor_group.value = {}

})


</script>


<style scoped>
* {
    text-transform: uppercase;
}
</style>