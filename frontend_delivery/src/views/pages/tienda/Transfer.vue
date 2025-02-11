<template>
    <div class="container">

        <nav  class="nav-bar shadow-1 ">
            <ul>
                <li class="nav-bar--item" v-for="(button, index) in navItems" :key="index">
                    <router-link :to="`/cancellation-requests/${button.path}/`">
                        <Button :icon="button.icon" text :class="isActive(button.path)? 'nav-var--item-button-selected': '' " severity="help" class=" nav-var--item-button" :label="button.label" />
                    </router-link>
                </li>
            </ul>
        </nav>


        <router-view/>



    </div>

</template>

<script setup>

import {ref} from 'vue'
import {PathService} from '@/service/pathService.js'

const isActive = PathService.isActiveRoute

const cancellationRequests = ref([])

    const navItems = [
    {
        label:'Por revisar',
        icon:'pi pi-history',
        path:'revisar'
    },
    {
        label:'Revisadas aprobadas',
        icon:'pi pi-check',
        path:'aprobadas'
    },
    {
        label:'revisadas rechazadas',
        icon:'pi pi-times',
        path:'rechazadas'
    },


]





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