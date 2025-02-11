<template>
   
<div>


    <DataTable  showGridlines stripedRows :value="categories" style="max-width: 50rem;" class="mx-auto mt-8" >

        <template #header>


    <h3>

<b>
    Reorganizar categoiras
</b>
</h3>

        </template>
            <Column style="text-transform: capitalize;" class="p-2 px-2 " field="aditional_item_name" header="NOMBRE">

                <template #body="data">

                    <h6 class="m-0 " style="text-transform: uppercase;"> {{ data.data.category_name }} </h6>

                </template>


            </Column>


            <Column style="text-transform: capitalize;max-width:5.6rem;" class="p-0 px-2" field="aditional_item_name" header="POSICION" >

            <template #body="data">

                <!-- <h6 class="m-0 " style="text-transform: uppercase;"> {{ data.data.index }} </h6> -->
                <inputText @change="update(data.data.category_id, data.data)" v-model="data.data.index" />
            </template>


            </Column>

        </DataTable>

</div>



</template>>

<script setup>


import { onMounted, ref } from 'vue';
import { fetchService } from '../../service/utils/fetchService';
import { URI } from '../../service/conection';




const update = async(category_id,data) => {
    fetchService.put(`${URI}/product-categories/${category_id}`,{
  "name": data.category_name,
  "index":data.index,
  "resturant_id": data.restaurant_id
})

categories.value = await fetchService.get(`${URI}/categories/${31}/${5}`)
    console.log(categories)
}



const categories = ref()


onMounted( async() => {
    categories.value = await fetchService.get(`${URI}/categories/${31}/${5}`)
    console.log(categories)
})

</script>