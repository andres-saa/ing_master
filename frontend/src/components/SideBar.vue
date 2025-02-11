<template>
    <div class="side-bar-container " ref="sidebarContainer">
        <div class="sidebar-content" style="position: relative;background-color: white;">
            <!-- <Button icon="pi pi-bars" @click="store.toggle_visible_categories" label="CATEGORIAS"


                class="category-toggle"></Button> -->


            <div class="selector"
                style="background-color: var(--primary-color);width: 100%; border-radius: 0;justify-content: space-between; gap:.5rem;padding: .5rem 1rem;position: sticky;top: 0;left: 0;right: 0;z-index: 99;"
                :style="!store.visible_categoires ? 'max-height:15rem' : 'max-height:0'">

                <router-link to="/">
                    <Button @click="() => store.side_bar_visible ? store.side_bar_visible = false : ''"
                        :style="is_active_router('/') ? 'box-shadow:0 .3rem white' : ''"
                        style="color:white;border-radius: 0;padding: 0 0 .3rem 0;" text label="Productos"></Button>
                </router-link>

                <router-link to="/carta">
                    <Button @click="() => store.side_bar_visible ? store.side_bar_visible = false : ''"
                        :style="is_active_router('/carta') ? 'box-shadow:0 .3rem white' : ''"
                        style="color:white;border-radius: 0;padding: 0 0 .3rem 0;" text label="Noticias"></Button>
                </router-link>

                <router-link to="/horarios">
                    <Button @click="() => store.side_bar_visible ? store.side_bar_visible = false : ''"
                        :style="is_active_router('/rastrear') ? 'box-shadow:0 .3rem white' : ''"
                        style="color:white;border-radius: 0;padding: 0 0 .3rem 0;" text label="Horarios"></Button>
                </router-link>


        
            </div>

            <div class="banner-container" style="margin: auto; position: relative; margin: auto;min-width: 100%;">
                <div class="title" style="max-width: 100%; margin: auto;">
                    <div class="categories p-2">
                        <div @click="navigate_to_category(i.category_name, i.category_id)"
                            :style="route.params.category_id == i.category_id ? 'background-color: var(--primary-color); color: #fff;' : ''"
                            class="categorie" v-for="i in categories" :key="i.category_id">
                            <img :src="`${URI}/read-photo-product/${i.image_identifier}/600`"
                                style="height: 2rem; object-fit: cover;aspect-ratio: 1 / 1;border-radius: 50%; text-align: center; filter: brightness(1.2); margin-right:
                    0.5rem;" />
                            <h5 class="" style="text-transform: capitalize;font-weight: 400;">{{
                                i.category_name?.toLowerCase() }}
                            </h5>
                        </div>
                    </div>
                </div>
            </div>





            <!-- 
            <div class="menu menu-carousel" style="padding: 0;">

                <div
                    style="background-color: #0d8342;padding:0 0rem  0rem .8rem; width: 100%; display: flex; align-items: center; justify-content: space-between;">

                    <p> <b>LO MAS NUEVO</b>
                    </p>


                    <div style="display: flex; gap: .5rem;">
                        <Button icon="pi pi-angle-left" class="arrow" />
                        <Button icon="pi pi-angle-right" class="arrow" />
                    </div>

                </div>



                <div class="news">

                </div>


            </div> -->

            <div class="menu menu-carousel" style="padding: 0; position: sticky;top:1rem;">

                <div
                    style="background: var(--instagram-gradient);padding: .8rem; width: 100%; display: flex;gap: 1rem; align-items: center; justify-content:start;color: #fff;">

                    <i style="height: 100%;" class="pi pi-instagram"></i>
                    <p class="p-0 m-0"> <b> NUEVO POST</b>
                    </p>




                </div>



                <div class="">




                    <iframe v-if="currentPost.link" :src="`${currentPost.link}embed`" width="100%" style="height: max-content ;min-height:600px"
                        frameborder="0" scrolling="no" allowtransparency="true">
                </iframe>

                </div>


            </div>

        </div>


    </div>
</template>

<style scoped>
.side-bar-container {
    min-width: 20rem;
    max-width: 80vw;
    height: 100%;
    min-height: 100%;
    /* background-color: black; */
    /* min-height: max-content; */
    /* position: f; */
    /* top: 0rem; */
    /* padding: 1rem; */
    /* z-index: 9999999999; */
}

.category-toggle {
    width: 100%;
    border-radius: .2rem;
    background-color: #fff;
    border: none;
    /* color: white; */

}

.news {
    padding: 1rem;
}

h3 {
    background-color: #0d8342;
}

.card-carousel-new {
    /* background-color: rgba(255, 0, 0, 0.342); */
    /* box-shadow: 0 0 1rem; */
    /* padding: 1rem; */
    border-radius: .5rem;
    display: flex;
    flex-direction: column;
    gap: .5rem;
}

.category-toggle:hover {

    filter: brightness(1.1);
    background-color: var(--primary-color) !important;
    border: none !important;
    color: white !important;
    outline: 1px solid;
}

.arrow {
    background-color: rgba(0, 0, 0, 0.399);
    border-radius: .3rem;
    border: none;
    aspect-ratio: 1 / 1;
    color: white;
}

.arrow:hover {
    border: none !important;
    background-color: rgba(0, 0, 0, 0.399) !important;
    filter: brightness(1.1);
}


.carrito {

    width: 100%;
    border-radius: .3rem;
    display: flex;
    justify-content: start;
    color: #999;
    border: none;

}


.price {
    font-size: 1.5rem;
    text-align: end;

}

.carrito:hover {
    background: var(--primary-color) !important;
    border: none !important;
    filter: brightness(1.1);
}

.product_image {
    width: 100%;
    width: 100%;
    border-radius: 0;
    display: flex;
    justify-content: start;
    color: #999;

}

.category {}

.sidebar-content {

    /* height: 100%; */
    min-height: max-content;
    display: flex;
    flex-direction: column;
    gap: 1rem;

}

.menu {
    background-color: #fff;
    /* border-radius: .3rem; */
    overflow: hidden;
    /* box-shadow: 0 0 1rem rgba(0, 0, 0, 0.113); */
    transition: all ease .3s;
    padding: 0rem;
}

.menu-carousel {
    padding: 1rem;
}

.selector {
    display: flex;
    align-items: center;
}
    

@media (width > 900px) {

    .selector {
        display: none;
    }

    .categories {
        display: none;
    }

}


.categorie {
    display: flex;
    align-items: center;
    background-color: #00000020;
    border-radius: .5rem;
    padding: .2rem .5rem;
    margin-bottom: .5rem;
    transition: all 0.2s ease;
    cursor: pointer;
    white-space: nowrap;
}

.categorie:hover {
    background-color: var(--primary-color);
    color: #fff;
}
</style>

<script setup>
import Button from 'primevue/button';
import { useSidebarStore } from '@/stores/sidebar';
import { onMounted, ref } from 'vue';
import { URI } from '@/service/conection';
import { onBeforeMount } from 'vue';
import { onBeforeUnmount } from 'vue';
const store = useSidebarStore()

import { useRoute, useRouter } from 'vue-router';
const sidebarContainer = ref(null);

const route = useRoute()

const currentPost = ref({ link: '' });

onMounted(async () => {
    try {
        const response = await fetchService.get(`${URI}/last-post`);
        if (response.link) {
            const url = new URL(response.link);

            // Convert URL to /p/ format for iframe preview
            if (url.pathname.includes('/reel/')) {
                url.pathname = url.pathname.replace('/reel/', '/p/');
            } else if (!url.pathname.includes('/p/')) {
                url.pathname = `/p${url.pathname}`;
            }

            currentPost.value.link = `${url.origin}${url.pathname}`;
        }
    } catch (error) {
        console.error('Error al obtener el enlace actual:', error);
    }
});

const is_active_router = (r) => {
    return route.path === r
}


const handleClickOutside = (event) => {
  if (sidebarContainer.value && !sidebarContainer.value.contains(event.target) && store.side_bar_visible) {
    store.toggle(); // Cierra el sidebar usando toggle
  }
};

onMounted(() => {
    document.body.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
    document.body.removeEventListener('click', handleClickOutside);
});

import router from '@/router';
import { fetchService } from '@/service/utils/fetchService';



const navigate_to_category = (categor_name, category_id) => {
    router.push(`/categoria/${categor_name}/${category_id}`)
    store.side_bar_visible ? store.side_bar_visible = false : ''
}


const categories = ref([]);

onMounted(async () => {
    categories.value = await fetchService.get(`${URI}/categories/31/5`);
});


</script>