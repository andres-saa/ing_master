<template>
    
    <div class="app-topbar-container " style="background-color: var(--primary-color);box-shadow: 0 0rem 2rem black;">
            

        <div class="header" style="max-width: 1280px;margin: auto;">


           

            <div class="header-container">

                <router-link to="/" style="text-decoration: none;max-width: 17rem; overflow: hidden;text-overflow: ellipsis;">
                    <div class="logo-sesion">
                        <img src="/src/assets/images/logo.png"  alt="">
                        <div style="display: flex;">
                            <h1 class="title roboto-thin m-0 p-0" style="padding: 0;margin: 0;font-size: 1.2rem;  ">
                            <b style="display: flex;flex-direction: column;">
                                ING MASTER
                              

                              

                            <Tag v-if="siteStore.status.status == 'open'"  severity="sucess"   style="padding: .1rem .3rem ;width: min-content;  margin: 0;background-color: green;border-radius: 20rem; color: white; display: flex;align-items: center; font-family: roboto;    animation:  blink .5s ease infinite;">
                                    <Tag class="ubicacion2" style="height: 1rem;width: 1rem;border-radius: 50%;padding: 0;"></Tag>
                                Abierto
                            </Tag>
                            

                            <Tag v-else severity="danger"   style="padding: .1rem .3rem ;width: min-content;  margin: 0;background-color: red;border-radius: 20rem; color: white; display: flex;align-items: center; font-family: roboto;    animation:  blink .5s ease infinite;">
                                    <Tag class="ubicacion3" style="height: 1rem;width: 1rem;border-radius: 50%;padding: 0;"></Tag>
                                Cerrado
                            </Tag>
                       
                            </b>

         
                           
                        </h1>
                        
                        
                        </div>
                    </div>
                </router-link>



                <div class="menus" v-if="true" style="">

                    <router-link to="/">
                        <Button   :style="is_active_router('/') ? 'box-shadow:0 .3rem white' : ''"
                            style="color:white;border-radius: 0;background-color: var(--primary-color);border: none;"  label="Productos y servicios"></Button>
                    </router-link>

                    <router-link to="/carta">
                        <div>
                            <Button :style="is_active_router('/carta') ? 'box-shadow:0 .3rem white' : ''"
                            style="color:white;border-radius: 0;background-color: var(--primary-color);border: none;"   label="Noticias"></Button>

                        </div>
                     

                    </router-link>
<!-- 
                    <router-link to="/rastrear">
                        <Button :style="is_active_router('/rastrear') ? 'box-shadow:0 .3rem white' : ''"
                        style="color:white;border-radius: 0;background-color: var(--primary-color);border: none;"   label="Rastrear Pedido"></Button>
                    </router-link> -->


                    <router-link to="/horarios">
                        <Button :style="is_active_router('/horarios') ? 'box-shadow:0 .3rem white' : ''"
                        style="color:white;border-radius: 0;background-color: var(--primary-color);border: none;"   label="Nuestros horarios"></Button>
                    </router-link>

                    <!-- <Button style="text-transform: capitalize;" @click="siteStore.visibles.currentSite = true" class="py-0 px-3" icon="pi pi-map-marker" :label="`${siteStore.location.neigborhood?.name} - ${formatoPesosColombianos(siteStore.location.neigborhood?.delivery_price) }`">
                    </Button> -->


                    <!-- <Button style="color:white" text label="Nosotros"></Button>
                    <Button style="color:white" text label="PQRS"></Button> -->
                </div>



                <div class="menu-button">
                    <div class="social-media"
                        style="padding: .1rem;overflow: hidden;">


                        <a class="p-0 m-0" href="https://www.facebook.com/ingmaster.com.co/" style="padding: 0;line-height: 0;">
                            <Button style="padding: 0; line-height: 0;color: white;" size="large" text
                                class="menu-bars p-0 m-0">

                                <i class="pi pi-facebook text-icon" style="color: ;"></i>
                            </Button>
                        </a>


                        <a class="p-0 m-0" href="https://www.instagram.com/ing_master_refrigeracion/" style="padding: 0;line-height: 0;color: ;">
                            <Button style="padding: 0;line-height: 0;color: white;" size="large" text class="menu-bars   p-0 m-0">
                                <i class="pi pi-instagram "></i>
                            </Button>
                        </a>

                        <a class="p-0 m-0" href="https://wa.link/z72oac" style="padding: 0;line-height: 0;">
                            <Button style="padding: 0;line-height: 0;color: white;" size="large" text class="menu-bars  p-0 m-0">
                                <i class="pi pi-whatsapp"></i>
                            </Button>
                        </a>

                        
                    </div>

                </div>


<!-- 

                <RouterLink to="/cart" class="button-barrras">
                    <div style="padding: 0;color: #fff;margin: 0;position: relative;">
                        <Button size="large" style="color: white;padding: 1rem" text="" class="menu-bars p-0">
                            <i class="pi pi-shopping-cart"></i>
                        
                        </Button>
                        <Badge style="position: absolute;left: 70% ; bottom:60%;aspect-ratio: 1  / 1;border-radius: 50%;">{{ cart.cart.products?.length }}</Badge>
                    </div>
                </RouterLink> -->

                <Button @click="toggleSidebar" size="large" style="padding: 0;color: #fff;margin: 0;" text
                    class="menu-bars button-barrras">
                    <i class="pi pi-bars"></i>
                </Button>
            </div>


        </div>



        <div style="color: white;align-items: center; justify-content:center ;display: flex; text-overflow: ellipsis; text-transform: capitalize;"> 


            <a href="https://wa.link/z72oac" style="background-color: var(--primary-color);">   
<Button  style="text-transform: capitalize;position: absolute;top: 100%;right:0 ; border-radius: 0 0 0rem 10rem; "  class="py-0 px-3 ubicacion" icon="pi pi-bill" label="Cotiza con nosotros">
</Button>
            </a>
</div>
    </div>





</template>

<script setup>


import { useSidebarStore } from '@/stores/sidebar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Select from 'primevue/select';
import { useRoute, useRouter } from 'vue-router';
import Tag from 'primevue/tag';
import Badge from 'primevue/badge';
import { usecartStore } from '@/stores/shoping_cart';
import { useSitesStore } from '@/stores/site';
import { formatoPesosColombianos } from '@/service/utils/formatoPesos';
import { computed } from 'vue';


const truncatedDescription =  (Description) => {
    return `${Description?.slice(0,29)}...`
}

const cart = usecartStore()
const route = useRoute()
const siteStore = useSitesStore()

const toggleSidebar = (event) => {
  event.stopPropagation(); // Evita que el clic se propague
  store.toggle(); // Alterna el estado del sidebar
};

const is_active_router = (r) => {
    return route.path === r
}

is_active_router()

const store = useSidebarStore()
</script>

<style scoped>
.app-topbar-container {
    padding: .3rem;
}

.logo-sesion {
    display: flex;
    align-items: center;
    justify-content: start;
    gap: 1rem;

}



i {

    font-size: 1.8rem;
    padding: .1rem;
}


.menus{
    display: flex;
    padding: .3rem;
}

.header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    /* padding-top: .5rem; */
}

.text-facebook {
    background: var(--facebook-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.text-instagram {
    background: var(--instagram-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.text-whatsapp {
    background: var(--whatsapp-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}



.social-media2 {
    display: flex;
    flex-direction: column;
    gap: .5rem;
}


.social-media {
    display: flex;
    gap: .5rem;
    align-items: center;
    /* border-radius: 10rem; */
}


.nav-bar {
    display: flex;
    /* grid-template-columns: 1fr 5fr 2fr; */
    width: 100%;
    gap: 1rem;
    align-items: center;
    height: 2rem;

    justify-content: end;
}

.search {
    width: 100%;
    height: 100%;
    max-width: 400px;
    background-color: white;
    border: none;
}


.header {

    display: flex;
    flex-direction: column;
    gap: .5rem;
    /* align-items: center; */
    /* padding-bottom: .5rem; */

}

h1 {
    font-family: roboto;
    letter-spacing: .1cap;
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;




}

img {
    width: 30%;
    max-width: 3rem;
    /* border-radius: 50%; */
    overflow: hidden;
    padding: .5rem;
}

.menu-button {
    display: flex;
    justify-content: end;
    padding: 0;
    margin: 0;
    background-color: none;
}




@media (width < 1400px) {
    .app-topbar-container {
        padding: 0 1rem;



    }




}

.ubicacion{
    animation:  blink .5s ease infinite !important;
}

.ubicacion2{
    animation:  blink2 .5s ease infinite !important;
}

.ubicacion3{
    animation:  blink3 .5s ease infinite !important;
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
    border: none;
  }
  50% {
    opacity: .8;
    /* background-color: var(--primary-color); */
    /* filter: brightness(1.2); */
    border: none;
  }
}


@keyframes blink2 {
  0%, 100% {
    opacity: 1;
    background-color: rgb(0, 255, 21);
    border: none;
  }
  50% {
    opacity: 1;
    background-color: yellow;
    filter: brightness(1.2);
    border: none;
  }
}

@keyframes blink3 {
  0%, 100% {
    opacity: 1;
    background-color: rgb(255, 255, 255);
    border: none;
  }
  50% {
    opacity: 1;
    background-color: rgb(255, 0, 0);
    filter: brightness(1.2);
    border: none;
  }
}



@media (width < 900px) {
    .app-topbar-container {
        padding: .3rem 1rem;



    }


    .menus {
        display: none
    }


}



@media (width > 900px) {
    .button-barrras {
        display: none;
    }
}


* {
    text-decoration: none;
}

.menu {
    display: flex;
}


@media (width < 900px) {
    .menu-button {
        display: none;
    }
}


@media (width > 900px) {
    .menu-button2 {
        display: none;
    }
}


</style>