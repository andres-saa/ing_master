<template>



    <div class="container">


        <category-card v-for="(category, index) in categories" :key="index" class="card" :category="category"
            :title="category.category_name"> </category-card>

    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import CategoryCard from './cards/CategoryCard.vue';
import { fetchService } from '@/service/utils/fetchService';
import { URI } from '@/service/conection';

const categories = ref([])






onMounted(async () => {
    categories.value = await fetchService.get(`${URI}/categories/31/5`)
})
</script>

<style scoped>
.container {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(4, 1fr);
    margin-top: 1rem;
    padding: 0 1rem;
    max-width: 1400px;
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
    .container {

        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }
}


@media (width < 600px) {
    .container {

        grid-template-columns: repeat(1, 1fr);
        gap: 2rem;
        padding: 0 1rem;
    }

    .name {
        font-size: .6rem;
    }


    .container {
        margin-top: .35rem;
    }
}
</style>
