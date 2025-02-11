<template>





    <div class="container4 " style="margin-top: 3rem;">

        <product_card v-for="(category) in products" :key="category.id" class="card" :product="category" />

    </div>
</template>

<script setup>
import { fetchService } from '@/service/utils/fetchService';
import product_card from './cards/product_card.vue';
import { onMounted, ref, watch } from 'vue';
import { URI } from '@/service/conection';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';

const route = useRoute()
const products = ref([])
const show_sizes = ref(false)
const selected_size = ref({ id: 7 })

const router = useRouter();
const categories = ref([]);

onMounted(async () => {
    categories.value = await fetchService.get(`${URI}/sizes`);
});

const navigate_to_category = (category) => {
    selected_size.value = category
};


const update = async () => {


    const category_id = route.params.category_id
    products.value = await fetchService.get(`${URI}/products-active/category-id/${category_id}/site/31/5`)


}

onMounted(async () => {
    update()
})




watch(() => route.params.category_id, async (newval) => {
    update()
})




</script>

<style scoped>
.container4 {
    display: grid;
    gap: 2rem;
    grid-template-columns: repeat(4, 1fr);
    margin-top: 1rem;
    padding: 0 1rem;
    max-width: 1280px;
    margin: auto;
    height: 100;
}

.card {
    width: 100%;
    display: block;
}

.item {
    width: 100%;
}


h2 {
    margin: 0;
    padding: 0;
    font-family: "Luckiest Guy", cursive;
    letter-spacing: .1cap;
    width: 100%;
    text-align: center;
    margin: 2rem 0;
    font-size: 2rem;
    color: var(--primary-color);
    transition: all ease .3s;
}


h2:hover {
    transform: scale(1.1);

}


@media (width < 1100px) {
    .container4 {

        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }
}


@media (width < 600px) {
    .container4 {

        grid-template-columns: repeat(1, 1fr);
        gap: 2rem;
        padding: 0 .7rem;
    }

    .name {
        font-size: .6rem;
    }


    .container4 {
        margin-top: .35rem;
    }
}
</style>
