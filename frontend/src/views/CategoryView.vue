<template>



    <div class="cantaniner" style="display: grid; ">




     
        <div class="sidebar">
            <SidebarMovil ></SidebarMovil>

        </div>

           
            <div>
                <h4 class="title" style="">{{ route.params.category_name }}</h4>


                <gridProduct></gridProduct>
            </div>
            

   


    </div>


</template>


<script setup>
import { ref } from 'vue';
import gridCategorias from '@/components/gridCategorias.vue';
import BarraCategorias from '@/components/BarraCategorias.vue';
import { useRoute } from 'vue-router';
import gridProduct from '@/components/gridProduct.vue';
import SidebarMovil from '@/components/SideBarMovil.vue'

const route = useRoute()
const categorias = ref([
    {
        name: 'Pizza',
        image: 'https://static.vecteezy.com/system/resources/previews/022/149/342/large_2x/hot-italian-pizza-cutout-png.png'
    },
    {
        name: 'Cocteles',
        image: 'https://static.vecteezy.com/system/resources/previews/048/723/424/non_2x/drinks-isolated-on-transparent-background-free-png.png'
    },
    {
        name: 'Hamburguesas',
        image: 'https://static.vecteezy.com/system/resources/previews/036/333/937/large_2x/ai-generated-yummy-street-food-burger-isolated-png.png'
    },
    {
        name: 'Postres',
        image: 'https://static.vecteezy.com/system/resources/previews/024/786/109/non_2x/pink-cake-with-cherries-the-theme-of-food-and-dessert-isolated-object-transparent-background-free-png.png'
    },
    {
        name: 'Ensaladas',
        image: 'https://static.vecteezy.com/system/resources/previews/036/397/406/large_2x/ai-generated-vegetable-salad-in-clear-bowl-isolated-on-transparent-background-png.png'
    }
])

</script>




<style scoped>
.banner-container {
    /* display: flex; */
    align-items: center;
    position: relative;
    /* margin-right: 2.5rem; */
    padding: .5rem;
    width: 100%;
    max-width: 100%;
    margin-top: 1rem;
}



.categories {
    display: flex;
    gap: 1rem;
    align-items: center;

}

.button {
    position: absolute !important;
    border-radius: 0;
    background-color: #cd1f3080 !important;
    border: none !important;

    aspect-ratio: 1 / 1;
}

.button:hover {
    border: none !important;
    background-color: var(--primary-color) !important;
}

i {
    color: #fff;
    font-size: 1.3rem;
    opacity: 1;
}


.title {
    margin: 0;
    padding: 0;
    font-family:roboto;
    font-weight: 900;
    letter-spacing: .1cap;
    width: 100%;
    text-align: center;
    margin: 2rem 0;
    font-size: 3rem;
    color: var(--primary-color);
    transition: all ease .3s;
}
.cantaniner{
    grid-template-columns: 20rem 1fr;
}

@media (width < 900px) {
    .title {
        font-size: 2rem;
    }

    .sidebar{
        display: none;
    }
    .cantaniner{
        grid-template-columns: 1fr;
    }
}

h2:hover {
    transform: scale(1.1);

}

.next {}

.preview {}



.categorie {
    /* padding: 1rem 0rem .2rem 1rem; */
    display: flex;
    align-items: center;
    background-color: #00000020;
    border-radius: 1rem;
    padding: 0 1rem;
    transition: all .2s ease;
    cursor: pointer;
}


.categorie:hover {
    background-color: var(--primary-color);
    color: #fff;
}
</style>
