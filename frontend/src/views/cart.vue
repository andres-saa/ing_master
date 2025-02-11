<template>
    <div>
        <div class="col-12 my-8 md:my-8 p-0">
            <h4 class="title">Carrito de compras</h4>

            <div class="mx-auto container" style="max-width:900px;">
                <div v-if="store.cart.products.length === 0" class="empty-cart-message">
                    <p>Tu carrito está vacío. ¡Agrega productos para comenzar!</p>
                </div>

                <div v-else
                    style="display: flex; flex-direction: column; position: sticky; top: 8rem; gap:1rem; justify-content: center;">
                    <div class="p-3 p-shadow" v-for="product in store.cart.products" :key="product.product.id"
                        style=" align-items:end; position: relative;box-shadow: 0 .5rem 2rem #00000010;border: 1px solid #00000030; gap:1rem; border-radius: 0.3rem;">


                        <div style="display: flex;gap: 1rem; justify-content: space-between;">
                            <img style="width:5rem; object-fit:cover; height:5rem ;background-color: ;"
                                :src="`${URI}/read-photo-product/${product.product.img_identifier}/600`" alt="">
                            <div style="display: flex; flex-direction:column; gap:0.4rem">
                                <div style="display: flex; flex-direction:column;align-items: end; gap:0.3rem; width:100%">
                                    <div
                                        style="display:flex;flex-direction: column; justify-content:end; align-items: end; width:100%; gap:0rem">
                                        <span class="p-0 m-0"> {{ product.product.product_name }} </span>
                                        <span style="; font-weight: bold;">{{
                                        product.product.category_name?.toLowerCase() }}</span>
                                    </div>
                                   

                                    <div style="display:flex">
                                        <div class="p-0"
                                            style="box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.2); background-color:#ff620000; border-radius: 5rem; display: flex;">
                                            <Button @click="store.removeProductInstance(product.product.id,product.flavors)"
                                                icon="pi pi-minus" severity="success"
                                                style="border:none; outline:none; width:2rem; height:1.5rem; border-radius: 0.4rem 0 0 0.4rem;">
                                            </Button>

                                            <InputText class="text-center"
                                                style="background-color:transparent; font-weight:bold; width:3rem; height:1.5rem; color:black; border:none"
                                                :modelValue="product.quantity" readonly></InputText>

                                     

                                            <Button @click="store.addProductToCart(product.product,1,[],product.flavors)" icon="pi pi-plus"
                                                severity="success"
                                                style="font-weight: bold; border:none; outline:none; width:2rem; height:1.5rem; border-radius:0 0.4rem 0.4rem 0;">
                                            </Button>
                                        </div>
                                    </div>



                                </div>
                            </div>
                        </div>


                        <Button class="ml-2" @click="store.removeProductFromCart(product.product.id,product.flavors)" icon="pi pi-times"
                            severity="danger" rounded
                            style="border:none; right: -.5rem; top: -.5rem; position: absolute; outline:none; width:2rem; height:2rem" />




                        <div
                            style="display: flex; gap:1rem;align-items: center;; width: 100%;margin-top: 1rem; flex-wrap: wrap;">
                            <h6 v-if="product?.flavors?.length > 1" style="margin: 0;"> <b
                                    style="">Sabores</b> </h6>
                            <h6 v-else-if="product?.flavors?.length > 0" style="margin: 0;"> <b>Sabor</b> </h6>
                            <div style="display: flex;gap: 1rem;flex-direction: row;">
                                <Tag v-for="flavor in product.flavors" style=""> {{ flavor.name}}</Tag>
                            </div>

                        </div>

                        <div
                            style="display: flex;gap:1rem;align-items: center;width: 100%;flex-wrap: wrap;" v-if="product.gaseosa?.name">

                            <h6  style="margin: 0;"> <b>Sabor de la gaseosa</b> </h6>
                            <div style="display: flex;gap: 1rem;flex-direction: row;">
                                <Tag severity="info" style=";"> {{ product.gaseosa?.name}}</Tag>
                            </div>

                        </div>


                        <h5 class="p-0 m-0" style="text-align: end;"> <b>{{ formatoPesosColombianos(product.total_cost)
                                }}</b> </h5>






                    </div>



                    <div class="p-0 mt-1">
                        <div class="col-12 p-0 mt-1">
                    <div class="p-shadow p-3 mb-4 " v-for="(items, grupo) in agrupados" :key="grupo" style="position: relative;border-radius: 0.3rem;">
                        
                        <Button class="ml-2" @click="deleteGroup(items)" icon="pi pi-trash"
                            severity="danger" rounded
                            style="border:none;right: -.5rem;top: -.5rem; position: absolute; outline:none;width:2rem; height:2rem" />

                        <div class="mb-2">
                            <span class="mb-2 text-center">
                                <b>{{ grupo }}</b>

                            </span>
                            
                            <div class="mt-2">
                                <div v-for="item in items" :key="item.aditional_item_instance_id"
                                    style="display: flex; gap: 1rem; align-items: center;">
                                    <Button text rounded @click="deleteAd(item)" class="p-0 m-0" severity="danger"
                                        style="width: 2rem;  height: 2rem;border: none;" icon="pi pi-trash m-0"></Button>
                                        

                                    <div style="display: flex; width: 100%; gap: 1rem; justify-content: space-between;">
                                        <span class="text adicion" style="text-transform: capitalize;">{{ item.name
                                        }}</span>
                                        <span style="display: flex; align-items: center;">







                                            <span v-if="item.price > 0" class="pl-2 py-1 text-sm">
                                                <b>{{ formatoPesosColombianos(item.price * item.quantity) }}</b>
                                            </span>

                                            <div v-if="grupo != 'SALSAS'" style="box-shadow: 0 0 5px rgba(0, 0, 0, 0.411);display: flex; border-radius: 0.3rem; " class="ml-2">

                                           
                                            <Button @click="decrement(item)"  severity="danger"
                                                style="width: 2rem; height: 1.5rem;border: none; border-radius: 0.3rem 0 0 0.3rem;"
                                                icon="pi pi-minus"></Button>
                                            <InputText :modelValue="item.quantity" readonly
                                                style="width: 2rem;border: none; height: 1.5rem;" class="p-0 text-center" />
                                            <Button @click="increment(item)" severity="danger"
                                                style="width: 2rem;height: 1.5rem; border: none;border-radius:0 0.3rem 0.3rem 0;"
                                                icon="pi pi-plus"></Button>
                                            </div>
                                        </span>

                                    </div>

                                </div>

                               

                            </div>
                            
                        </div>
                        
                    </div>
                    <div  @click="store.setVisible('addAdditionToCart',true)" class="col-12 p-0 m-0" style="display: flex; justify-content: end;">
                        <Button style="width: 2rem;left: .3rem; height: 2rem;" rounded severity="danger" icon="pi pi-plus"></Button>

                    </div>

                </div>

                    </div>
                </div>
                <resumen class="md:col-6"></resumen>
            </div>
        </div>

        <dialogAddAditions></dialogAddAditions>
    </div>
</template>



<script setup>
import { useToast } from 'primevue/usetoast';
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue';
import resumen from './resumen.vue';
import { usecartStore } from '@/stores/shoping_cart';
import { formatoPesosColombianos } from '@/service/utils/formatoPesos';
import { useSitesStore } from '@/stores/site';
import { adicionalesService } from '@/service/restaurant/aditionalService';
import dialogAddAditions from './dialogAddAditions.vue'
import { useUserStore } from '@/stores/user';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Tag from 'primevue/tag';
import { URI } from '@/service/conection';
const store = usecartStore()
const siteStore = useSitesStore()
const selectedAdditions = ref({})
const agrupados = ref({})
const user = useUserStore()


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



watch(() => store.cart.additions, () => {
    update()
}, { deep: true })


const increment = (adition) => {
    const new_adition = { ...adition }
    new_adition.quantity = 1
    store.addAdditionToCart(new_adition)
}

const decrement = (adition) => {

    if (adition.quantity > 1) {
        store.removeAdditionFromCart(adition.id)
    }
}

const deleteAd = (adicion) => {
    store.removeAdditionCompletelyFromCart(adicion.id)
    update()
}

const deleteGroup = (items) => {
    items.forEach(item => {
        deleteAd(item)
    })
}

watch(() => store.visibles.addAdditionToCart, (newval) => {
    if (newval) {
        selectedAdditions.value = {}
    }
}, { deep: true })

const adicionales = ref([])
onMounted(async () => {


    if (user.user.payment_method_option?.id != 7)
        siteStore.setNeighborhoodPrice()
    else {
        siteStore.setNeighborhoodPriceCero()

    }


    const product_id = 53


    if (product_id) {
        adicionales.value = await adicionalesService.getAditional(product_id)
    }


    agrupados.value = store.cart.additions.reduce((acumulador, elemento) => {
        let grupo = elemento.group;

        if (!acumulador[grupo]) {
            acumulador[grupo] = [];
        }
        acumulador[grupo].push(elemento);

        return acumulador;
    }, {})


})


</script>


<style scoped>
*:focus {
    border: none;
}

.led {
    animation: cambiaColor 1s infinite;
    /* 3s de duración, animación infinita */
}

.name-product::first-letter {
    ;
}

img {
    border-radius: 5%;
}


    

.title {
    margin: 0;
    padding: 0;
    font-family: "Luckiest Guy", cursive;
    letter-spacing: .1cap;
    width: 100%;
    text-align: center;
    margin: 2rem 0;
    font-size: 3rem;
    color: var(--primary-color);
    transition: all ease .3s;
}



h2:hover {
    transform: scale(1.1);

}




.domi-name {
    text-transform: capitalize;
}

.descripcion::first-letter {
    ;
}

@keyframes cambiaColor {
    0% {
        background-color: rgb(0, 0, 0);
    }

    50% {
        background-color: rgb(30, 255, 0);
    }

    100% {
        background-color: var(--primary-color);
    }
}

.triangulo {
    width: 0;
    height: 0;
    border-left: 1rem solid transparent;
    border-right: 1rem solid transparent;
    border-bottom: 2rem solid #ffede1;
    /* Altura del triángulo dependiendo del ancho */
    transform: rotate(-65deg);
    position: absolute;
    top: -1rem;
    left: -1.2rem;
}


.container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.fixed {
    position: fixed;
    width: 25%;
}

.scrollit {
    float: left;
    width: 71%
}

.sumary {
    /* background-color: green; */
}

.izq {
    /* width: 100%; */

}

*:focus {
    /* outline: none; */
}


.contenedor-producto {
    align-items: center;
    border-radius: .5rem;
    overflow: hidden;
    height: 7rem;
    position: relative;
}

@media (max-width: 991px) {
    .contenedor-producto {
        /* background-color: #ffffffea;align-items: center;border-radius: rem;overflow: hidden;height: 7rem;position: relative; */
    }
}

.nombre-sesion {
    font-weight: bold;
    /* width: auto; */
    border-radius: 5rem;
}

.contenedor-principal {
    /* border-radius: 2rem; */
    /* position: sticky */
    /* top: 100px; */
    /* margin-bottom: 10rem; */
    /* background-color: var(--primary-color); */
    /* height: auto; */
}


.producto {
    border-bottom: 2px solid #00000020;
}



.cantidad:focus-visible {
    outline: none;

}

.imagen {
    height: 100px;
    object-fit: contain;
}

.contador {
    background-color: white;
    /* height: 3rem;  */

    display: flex;
    border-radius: 0.1rem;
    padding: 0.1rem 1rem;
    /* border: 1px solid var(--primary-color); */
    border-radius: 0.5rem;
    /* bottom: 0.5rem; */
    border: 1px solid;
    position: absolute;
    right: 1rem;
    bottom: 1rem;
    width: 8rem;
    height: 2.5rem;

}

i {
    font-weight: bold;
}

i:hover {
    color: var(--primary-color);
}

button:hover {
    cursor: pointer;
}

@media (min-width: 768px) and (max-width: 991px) {
    .clase {
        /* background-color: red; */
        min-width: 720px;
    }
}

@media (min-width: 1200px) and (max-width: 1920px) {
    .clase {
        /* background-color: red; */
        min-width: 1024px;

    }

    .productos-scroll {
        overflow-y: auto;
        border-radius: 2rem;
        /* height: 80vh; */
        overflow-y: auto;
        /* max-height: 720px */
    }
}

::-webkit-scrollbar {
    width: 1rem;
    /* Ancho de la barra de desplazamiento */
    padding-top: 1rem;
    position: absolute;
    display: none;
}

.clase {}

*:focus {
    outline: none;
}

* {
    text-transform: capitalize;
}

*::first-letter {
    ;
}



/* Estilo del pulgar de la barra de desplazamiento */
/* WebKit (Chrome, Safari) */
::-webkit-scrollbar-thumb {
    background-color: rgb(255, 0, 0);
    /* Color del pulgar de la barra de desplazamiento */
    border-radius: 9px;
    border: 5px solid var(--primary-color);
    height: 10rem;
    width: 10rem;
    /* display: none;  */
}

.p-shadow {
    box-shadow: 0 .2rem 5px rgba(0, 0, 0, 0.15);
}

@media (width < 800px) {
    .title {
        font-size: 2rem;
    }

    .container {
        display: flex;
        flex-direction: column;
    }


}

*{
    text-transform: lowercase;

}

*::first-letter{
    text-transform: uppercase;
}

</style>