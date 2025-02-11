<template>
    <banner style="width: 100%;"></banner>
    <h2 style="padding-top: 0;">Nuestro maravilloso catalogo</h2>
    <gridCategorias></gridCategorias>
    <!-- <category-view></category-view> -->


</template>


<script setup>

import gridCategorias from '@/components/gridCategorias.vue';
import Banner from '@/components/Banner.vue';
// import CategoryView from './CategoryView.vue';
</script>


<style scoped>
h2 {
    margin: 0;
    padding: 0;
    font-family: roboto;
    font-weight: 800;
    letter-spacing: .1cap;
    text-transform: uppercase;
    width: 100%;
    text-align: center;
    /* margin: 1rem 0; */
    margin-top: 3rem;
    font-size: 2rem;
    color: rgb(255, 252, 252);
    color: var(--primary-color);
    transition: all ease .3s;
    /* text-shadow:
    0 0 5px  #000000,
    0 0 10px #000000,
    0 0 15px #ff00dd,
    0 0 20px #ff0000,


    0 0 5px #ff0000ab; */

}


h2:hover {
    transform: scale(1.1);

}
</style>