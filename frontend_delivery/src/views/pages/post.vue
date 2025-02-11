<template>
    <div class="m-auto my-7" style="max-width: 50rem; height: 60vh">
        <div style="display: flex; gap: 2rem;">
            <InputText v-model="inputLink" placeholder="Inserta aquí el link de tu último post de Instagram" style="width: 100%;"></InputText>
            <Button @click="sendToServer" severity="help" style="width: 30%;" label="Realizar cambio"></Button>
        </div>
        
        <div style="display: flex; gap: 2rem;justify-content: center;">
            <div style="width: 100%;max-width: 25rem;">
                <h3 style="text-transform: uppercase;text-align: center;" class="my-4"><b>ACTUAL</b></h3>
                <iframe v-if="currentPost.link" :src="`${currentPost.link}embed`" width="100%" style="height: 900px;"
                        frameborder="0" scrolling="no" allowtransparency="true">
                </iframe>
            </div>
       
            <div style="width: 100%;" v-if="last_post.includes('http')">
                <h3 style="text-transform: uppercase;text-align: center;" class="my-4"><b>Nuevo</b></h3>
                <iframe :src="`${last_post}embed`" width="100%" style="height: 900px;"
                        frameborder="0" scrolling="no" allowtransparency="true">
                </iframe>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { fetchService } from '@/service/utils/fetchService';
import { URI } from "../../service/conection";

const inputLink = ref('');
const last_post = ref('');
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

// Watch to update iframe preview on link change
watch(inputLink, (newLink) => {
    if (newLink.includes('http')) {
        const url = new URL(newLink);

        // Convert URL to /p/ format for iframe preview
        if (url.pathname.includes('/reel/')) {
            url.pathname = url.pathname.replace('/reel/', '/p/');
        } else if (!url.pathname.includes('/p/')) {
            url.pathname = `/p${url.pathname}`;
        }

        last_post.value = `${url.origin}${url.pathname}`;
    } else {
        last_post.value = ''; // Clear iframe if link is invalid
    }
});

const sendToServer = async () => {
    try {
        // Enviar el nuevo enlace al servidor
        const response = await fetchService.put(`${URI}/update-last-post`, { link: last_post.value });
        console.log('Enlace enviado al servidor:', response);

        // Actualizar currentPost con el nuevo enlace
        currentPost.value.link = last_post.value;
        console.log('Enlace actual actualizado en la vista');

        // Limpiar inputLink y last_post
        inputLink.value = '';
        last_post.value = '';
    } catch (error) {
        console.error('Error al enviar el enlace al servidor:', error);
    }
};
</script>
