<template>

  <div style="position: sticky;top: 3rem; z-index: 999; background-color: white;" class="col-12 shadow-3 d-flex p lg:justify-content-center align-items-center mb-1 p-0 md:p-0">


      <div class="col-12  d-flex p lg:justify-content-center align-items-center  p-0 md:p-1"
      style="overflow-x: auto;background-color: rgba(255, 255, 255, 0.913)">

      

      <div v-for="section in categories" :key="section.category_id" class="p-1">
          <button @click="navigateToCategory(section.to)"
              :class="checkSelected(section.to) ? 'selected menu-button' : 'menu-button'"
              class="p-0 text-lg titulo" style="font-weight: 400; text-transform: uppercase;min-width: max-content;">
              <span class="text-lg" style="min-width: max-content;">{{ section.category_name }}</span>
          </button>
      </div>
  </div>
  </div>
  

  <router-view></router-view>

</template>





<script setup>
import { ref, onMounted, watch } from 'vue';
import router from '@/router/index.js';
import { useRoute } from 'vue-router';
import { categoriesService } from '@/service/restaurant/categoriesService'

import { useSitesStore } from '@/store/site';

const store = useSitesStore()

const categories = ref([
  {
    category_id:1,
    category_name:'Insumos',
    to:'/tienda-menu/'
  },
  { 
    category_id:2,
    category_name:'Ultimo post',
    to:'/admin/post'
  },
  { 
    category_id:2,
    category_name:'Banners',
    to:'/admin/banners'
  },

  { 
    category_id:2,
    category_name:'Organizar Categorias',
    to:'/admin/reorder_categories'
  },
  { 
    category_id:2,
    category_name:'Noticias',
    to:'/admin/carta'
  },
  

]);


const navigateToCategory = (to) => {

      router.push(to)
 
};



const checkSelected = (section) => {
  const route = useRoute(); // Asegúrate de que tienes acceso a useRoute aquí
  return route.fullPath.includes(section) // Verifica si el path actual contiene la cadena section
};



</script>


<style scoped>
.boton-menu {
  margin: 0;
  border: none;
  background-color: transparent;
  font-size: 20px;
  padding: 0 20px;
}

* {
  text-transform: lowercase;
}

*::first-letter {
  text-transform: uppercase;
}

.menu-button {
  background-color: transparent;
  padding: 1rem;
  margin: 0 1rem;
  border: none;
  font-size: 20px;
  outline: none;

}

.menu-button:hover {

  cursor: pointer;


}

*:focus {
  outline: none;
}


.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.titulo {
  text-transform: lowercase;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.selected {
  box-shadow: 0 0.5rem var(--primary-color);

}
.col-12 {
  width: 100vw;
  /* position: absolute; */
  left: 0;
  padding: 1.5rem;
}
</style>