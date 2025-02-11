<template>
    <div class="p-0 my-1 md:my col-12" v-if="store.cart?.products?.length > 0">
        <div style="position: sticky; top: 5rem;border-radius: 0.5rem; z-index: 100;box-shadow: 0 .5rem 1rem #00000020;border: 1px solid #00000040;"
            class="col-12 p-3 p-shadow m-0  ">

            <h5> <b>Resumen</b> </h5>

            <h5> <b>productos</b> </h5>

            <div v-for="product in store.cart.products"
                style="display: flex; justify-content: space-between; flex-direction: column; padding: 0; margin: 0; margin-bottom: 0;">

                <div style="display: flex; justify-content: space-between; padding: 0; margin: 0; margin-bottom: 0;">
                    <div style="display: flex; align-items: center; padding: 0; margin: 0;">
                        <span style="min-width: 2rem; font-weight: bold;">{{ product.quantity }}</span>
                        <span>{{ product.product.product_name }}</span>
                    </div>

                    <div style="text-align: right; padding: 0; margin: 0;">
                        <span>{{ formatoPesosColombianos(product.total_cost) }}</span>
                    </div>
                </div>

                <div
                    style="display: flex;gap: 0.3em;rem;align-items: center;justify-content: start;padding: 0; width: 100%; flex-wrap: wrap;">

                    <div style="display: flex; gap: 0.2rem; align-items: center;width: 100%; justify-content: space-between;" v-for="(flavor, index) in product.flavors"> 

                        <Tag  :key="index" style="padding: .3rem;">
                            <span style="color: black;">
                                {{ product.flavors.length > 1 ? `1/2` : 'sabor' }}
                            </span>
                            {{ flavor.name }} {{ product?.quantity > 1 && flavor.price > 0? `x ${product.quantity} =` : '' }} 

                        </Tag>
                        <p class="p-0 m-0">      <b> {{ flavor.price * product.quantity > 0 ? formatoPesosColombianos(flavor.price / 2 * product.quantity) : '' }}
                        </b>                     </p>
                    </div>

                    <div v-if="product?.gaseosa?.name" style="display: flex;width: 100%; gap: 0.2rem; align-items: start; flex-direction: column;">
                        <Tag style="padding: " severity="info">
                            <span style="">
                               <span style="color: black;padding: 0;margin:0;">  SABOR DE LA GASEOSA </span> {{ product.gaseosa?.name }}
                            </span>
                            <!-- {{ flavor.name }} {{ product?.quantity > 1 && flavor.price > 0? `x ${product.quantity} =` : '' }} {{ flavor.price * product.quantity > 0 ? formatoPesosColombianos(flavor.price / 2 * product.quantity) : '' }} -->
                        </Tag>
                    </div>
                </div>
            </div>





            <div class="col-12 p-0 mt-1">
                <div class="p-0 mb-2 " v-for="(items, grupo) in agrupados" :key="grupo"
                    style="position: relative;border-radius: 0.3rem;">


                    <div class="mb-0">
                        <span class="mb-1 text-center">
                            <b>{{ grupo }}</b>

                        </span>


                        <div v-for="item in items" :key="item.aditional_item_instance_id"
                            style="display: flex; gap: 1rem; align-items: center;">

                            <div style="display: flex; width: 100%; gap: 1rem; justify-content: space-between;">


                                <span class="text adicion" style="text-transform: ;"><span> <b> {{ item.quantity }}</b>
                                    </span> {{ item.name
                                    }}</span>



                                <span v-if="item.price > 0" class="pl-2  text-sm">
                                    <b>{{ formatoPesosColombianos(item.price * item.quantity) }}</b>
                                </span>






                            </div>

                        </div>




                    </div>

                </div>


            </div>








            <div style="display: flex; flex-direction: column;">
                <div style="display: flex; justify-content: space-between; padding: 0; margin: 0;">
                    <span><b>Subtotal</b></span>
                    <span><b>{{ formatoPesosColombianos(store.cart.total_cost) }}</b></span>
                </div>

                <div style="display: flex; justify-content: space-between; padding: 0; margin: 0;">
                    <span
                        :style="siteStore.location.neigborhood.delivery_price == 0 ? 'text-decoration: line-through;' : ''"><b>Domicilio</b></span>
                    <span style="color: var(--primary-color);"
                        v-if="siteStore.location.neigborhood.delivery_price == 0">
                        <b>Recoger en local</b>
                    </span>
                    <span v-else>
                        <b>{{ formatoPesosColombianos(siteStore.location.neigborhood.delivery_price) }}</b>
                    </span>
                </div>

                <div style="display: flex; justify-content: space-between; padding: 0; margin: 0;">
                    <span><b>Total</b></span>
                    <span><b>{{ formatoPesosColombianos(store.cart.total_cost +
                        siteStore.location.neigborhood.delivery_price) }}</b></span>
                </div>
            </div>



            <router-link to="/" v-if="route.path.includes('cart')">
                <Button outlined icon="pi pi-shopping-cart" label="Seguir comprando" class="mt-4" severity="danger"
                    style="outline: none;width: 100%;font-weight: bold; background-color: rgba(0, 0, 0, 0);"></Button>

            </router-link>

            <router-link to="/cart" v-else>
                <Button outlined icon="pi pi-arrow-left" label="Volver al carrito" class="mt-4" severity="danger"
                    style="outline: none;width: 100%;font-weight: bold; background-color: rgba(0, 0, 0, 0);"></Button>

            </router-link>

            <Tag v-if="siteStore.status.status == 'closed'" style="width: 100%;text-transform: capitalize; height: 2.5rem;" class="mt-2"
                severity="danger"> Cerrado, abrimos a las {{ siteStore.status.next_opening_time.split(':')?.slice(0,2).join(' : ') }} </Tag>

            <router-link to="/pay" v-if="route.path.includes('cart') && siteStore.status.status != 'closed'">
                <Button iconPos="right" icon="pi pi-arrow-right" label="Pedir" class="mt-2" severity="help"
                    style="outline: none;width: 100%; border: none;font-weight: bold; background-color: black;"></Button>
            </router-link>

            <router-link to="/pay" v-else-if="siteStore.status.status != 'closed'">
                <Button :disabled="store.sending_order || siteStore.status.status == 'closed'" @click="() => {
                    orderService.sendOrder()
                    sending = true
                }" iconPos="right" icon="pi pi-arrow-right" label="Finalizar pedido" class="mt-2" severity="help"
                    style="outline: none;width: 100%; border: none;font-weight: bold; background-color: black;"></Button>
            </router-link>

        </div>









    </div>
</template>

<script setup>
import { formatoPesosColombianos } from '@/service/utils/formatoPesos';
import { usecartStore } from '@/stores/shoping_cart';
import { useSitesStore } from '@/stores/site';
import { useRoute } from 'vue-router';
import { orderService } from '@/service/order/orderService';
import { onMounted, ref, watch } from 'vue'
import { useUserStore } from '@/stores/user';
import Button from 'primevue/button';
import Tag from 'primevue/tag';

const sending = ref(false)
const route = useRoute()
const store = usecartStore()
const siteStore = useSitesStore()
const user = useUserStore()



const agrupados = ref({})



const update = () => {
    agrupados.value = store.cart.additions.reduce((acumulador, elemento) => {
        let grupo = elemento.group;

        if (!acumulador[grupo]) {
            acumulador[grupo] = [];
        }
        acumulador[grupo].push(elemento);

        return acumulador;
    }, {})
}




onMounted(() => {
    update()

    if (user.user.payment_method_option?.id != 7)
        siteStore.setNeighborhoodPrice()
    else {
        siteStore.setNeighborhoodPriceCero()

    }

    if(siteStore.location?.neigborhood.delivery_price === null){
        siteStore.visibles.currentSite = true
    }


})


watch(() => store.cart.additions, () => {
    update()
}, { deep: true })



</script>
<style scoped>
.p-shadow {
    box-shadow: 0 .3rem 5px rgba(0, 0, 0, 0.15);
}

button {
    text-transform: uppercase;
}

* {
    text-transform: lowercase;
    font-size: 0.9rem;
}

*::first-letter {
    text-transform: uppercase;
}
</style>