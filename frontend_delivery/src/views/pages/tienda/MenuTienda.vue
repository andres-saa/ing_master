<template>





<div style="border-radius: 1rem;position:relative"  class="mx-auto mx-0 p-0 mt-0 ">
    <barraCategorias class="m-0" />
    <div  v-if="route.path != '/tienda-menu/productos/sabores'  &&  route.path != '/tienda-menu/productos/adiciones'  " class="mx-0 my0 mx-auto px-2" style="min-width: max-content;max-width: 1024px;justify-content: end; display: flex; align-items: end;">
        <!-- <span class="mr-4" > <b>SEDE</b>  </span> -->
        <!-- <Dropdown v-model="siteStore.site" :options="sites.filter(site => site.show_on_web)" optionLabel="site_name" class="" style="width: 100%;"/>  -->
          
        <Button  @click="open_to_add" class="ml-3 mr-2 my-3" style="min-width: max-content;" severity="help" label="Nuevo producto"></Button>
        <Button @click="open_to_gest_categorie" class="ml-3 mr-2 my-3" style="min-width: max-content;" severity="help" label="Gestionar categorias"></Button>

    </div>
    <router-view class=""></router-view>
    <dialogEditProduct class="m-3"></dialogEditProduct>
    <dialogDeleteProduct></dialogDeleteProduct> 
    <dialogAddProduct></dialogAddProduct>
    <dialogGestorCategorias></dialogGestorCategorias>
    


</div>

</template>

<script setup>



import { onMounted, ref } from 'vue';
import BarraCategorias from '@/components/BarraCategorias.vue';
import { siteService } from '@/service/siteService.js';
import dialogEditProduct from '../dialogEditProduct.vue';
import { useSitesStore } from '@/store/site';
import dialogAddProduct from '../dialogAddProduct.vue'
import dialogDeleteProduct from '../dialogDeleteProduct.vue';
import { watch } from 'vue';
import { useProductStore } from '@/store/productStore';
import { useRoute } from 'vue-router';
import dialogGestorCategorias from '../dialogGestorCategorias.vue';

const store = useProductStore();
const route = useRoute()
const siteStore = useSitesStore()

const sites = ref([])


const open_to_add = () => {
    // alert(store.visibles.dialogAddProduct)
    store.visibles.dialogAddProduct = true
}



const open_to_gest_categorie = () => {
    // alert(store.visibles.dialogAddProduct)
    store.visibles.dialogGestorCategoria = true
}

const update = async() =>{
    sites.value = await siteService.getSites()

}


onMounted(async() => {
   update()
 
})



</script>