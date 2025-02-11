<template>
    <div class="banner-container" style="margin:2rem auto; position: relative;max-width: max-content;">
        <div class="title" style="max-width: 100%; margin: auto;">
            <div class="categories">
                <div @click="navigate_to_category(i.category_name, i.category_id)"
                    :style="route.params.category_id == i.category_id ? 'background-color: var(--primary-color); color: #fff;' : ''"
                    class="categorie" v-for="i in categories" :key="i.category_id">
                    <img :src="`${URI}/read-photo-product/${i.image_identifier}/600`"
                        style="height: 2rem; object-fit: cover;aspect-ratio: 1 / 1;background-color: var(--primary-color); border-radius: 50%; text-align: center; filter: brightness(1.2); margin-right:
                    0.5rem;" />
                    <h5 class="m-0 p-0">{{ i.category_name }}</h5>
            </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchService } from '@/service/utils/fetchService';
import { URI } from '@/service/conection';

const route = useRoute();
const router = useRouter();
const categories = ref([]);

onMounted(async () => {
    categories.value = await fetchService.get(`${URI}/categories/31/5`);
});

const navigate_to_category = (category_name, category_id) => {
    router.push(`/categoria/${category_name}/${category_id}`);
};
</script>

<style scoped>
.categories {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
    width: 100%;
}

img {
    aspect-ratio: 1 / 1;
    border: 50%;
    overflow: hidden;
}

.title {
    border: 0.3rem solid white;
    background-color: #fff;
    color: black;
    font-size: 1rem;
    /* box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.266); */
    text-align: center;
    border-radius: .5rem;
    overflow: auto;
    display: flex;
    align-items: center;
    /* padding: 1rem; */
    gap: 2rem;
}

.categorie {
    display: flex;
    align-items: center;
    background-color: #00000020;
    border-radius: .5rem;
    padding: .2rem .5rem;
    transition: all 0.2s ease;
    cursor: pointer;
    white-space: nowrap;
}

.categorie:hover {
    background-color: var(--primary-color);
    color: #fff;
}

h2,
h5 {
    margin: 0;
    padding: 0;
}
</style>