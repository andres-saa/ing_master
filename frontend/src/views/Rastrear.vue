<template>
    <div class="container" style="height: 100%;display: flex;flex-direction: column; min-height: 80vh;">
        <div style="width: 100%;height: 100%;padding: 4rem 0;">
            <div style="max-width: 100%;width: 100%;padding: 1rem;">

                <div style="width: 100%;display: flex;gap: 1rem;margin: auto;max-width: 30rem;">
                    <InputText v-model="order_id" class="search" filter="" style="border-radius: 10rem;"
                        placeholder="id del pedido ejemplo TEZ-0054...">
                    </InputText>
                    <Button rounded @click="get_status_history(order_id)"
                        style="aspect-ratio: 1 / 1;background-color: var(--primary-color);border: none;color: white;">
                        <i class="pi pi-search"></i>
                    </Button>
                </div>

                <header v-if="currentStatus">
                    <h1>¡Gracias por tu compra!</h1>
                    <p v-if="currentStatus.status === 'generada'">Tu pedido ha sido recibido y está en proceso de ser
                        atendido.</p>
                    <p v-else-if="currentStatus.status === 'en preparacion'">Su pedido se encuentra en preparación y en
                        breve estará listo para enviarse.</p>
                    <p v-else-if="currentStatus.status === 'enviada'">¡Tu pedido está en camino!</p>
                </header>

                <section v-if="currentStatus && currentStatus.status === 'enviada'">
                    <h2>¡Tu pedido está en camino!</h2>
                    <!-- <p>Hora estimada de entrega: 9:22 pm</p> -->
                </section>

                <section v-if="currentStatus">
                    <h3 >Historial de Estado</h3>
                    <ul>
                        <li v-for="stat in status[0].status_history" :key="stat.timestamp">
                            🔴 {{ stat.status }} - {{ stat.timestamp }}
                        </li>
                    </ul>
                </section>



                
            </div>
        </div>
        <banner></banner>

        <h2 class="invitacion">¡Antójate de algo bien rico!</h2>
        <gridCategorias></gridCategorias>
    </div>
</template>

<script setup>
import Select from 'primevue/select';
import gridCategorias from '@/components/gridCategorias.vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Banner from '@/components/Banner.vue';

import { URI } from '@/service/conection';
import { fetchService } from '@/service/utils/fetchService';
import { ref } from 'vue';

const order_id = ref('');
const status = ref([{}]);
const currentStatus = ref(null);

const get_status_history = async (order_id) => {
    const result = await fetchService.get(`${URI}/history-my-orden/${order_id}`);
    status.value = result;
    currentStatus.value = result[0]?.current_status || null;
};
</script>

<style scoped>
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    background-color: #f7f7f7;
    color: #333;
}

.search {
    width: 100%;
    height: 100%;
    max-width: 400px;
    background-color: white;
}

header,
section,
footer {
    background-color: #fff;
    padding: 20px;
    margin-bottom: 10px;
    border-radius: 5px;
    color: black;
}

header {
    color: #d60000;
    text-align: center;
    background-color: #cd1f301a;
    margin-top: 1rem;
}

h1,
h2 {
    color: #d60000;
}

.invitacion {
    margin: 3rem;
    padding-top: 3rem;
    width: 100%;
    text-align: center;
    margin: 0rem 0;
    font-size: 3rem;
    color: var(--primary-color);
    transition: all ease .3s;
    font-family: "Luckiest Guy", cursive;
    letter-spacing: .1cap;
}


@media (width < 900px) {

    .invitacion {
        font-size: 1.5rem;
    }

}

.invitacion:hover {
    transform: scale(1.1);

}

ul {
    list-style: none;
    padding: 0;
    color: black;
}

li {
    margin-bottom: 5px;
}
</style>
