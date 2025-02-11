<template>
    <Toast />

    <div class="container2 p-shadow p-0" @click="open(props.product)"
        style="border-radius: 0.5rem; height: 100%;position: relative;box-shadow: 0 0 .5rem #00000020;">

        <div class="name-phone">
            
                    <span class="p-0" style="text-align: end;">
                        <b style="text-transform: uppercase;text-align: end;">
                            {{ props.product.product_name }}
                        </b>
                    </span>
                  
        </div>
        <div class="container p-0 ">
            
        <div class="imagen" style="display: flex;align-items: center; " >
            <img style="width: 100%; aspect-ratio: 5 / 5 ; border-radius: .5rem; background-color: rgb(255, 255, 255);object-fit: cover; border-radius: 0.3rem .3rem 0 0;"
                :src="currentImage(props.product.img_identifier)" @load="loadHighResImage(props.product.img_identifier)"
                alt="">
        </div>

        

        <div class="texto p-3" style="display: flex;justify-content: space-between; flex-direction: column;">
            <div style="display: flex;gap: 0rem; height: 100%;padding-bottom: 3rem; flex-direction: column;justify-content: space-between;">

             

                <div class="name-pc">
                    <p class="pt-0" style="">
                        <b style="text-transform: uppercase;">
                            {{ props.product.product_name }}
                        </b>
                    </p>
                    <!-- <Button text style="color: black;" icon="pi pi-ellipsis-v p-0 text-xl" /> -->
                    <!-- <img class="character" style="width:4rem;" :src="`/images/characters/${props.index}.png`" alt=""> -->
                </div>


                <h6 class="py-0 m-0" >
                    {{ truncatedDescription?.toLocaleLowerCase() }}
                </h6>


                 
                <div style="display: flex;justify-content: end;padding: 1rem; align-items: center;position: absolute;bottom: 0;text-align: end;width: 100%;right: 0;  gap: 1rem;justify-content:end;">
                        
                        <!-- <Button label="Ver mas" rounded></Button> -->
                        <h6 v-if="props.product?.last_price" class="text-2xl p-0 m-0"
                            style="text-decoration: line-through; opacity: .5;">
                            {{ props?.product?.last_price }}
                        </h6>
               
                        <h4 class="text-2xl p-0 m-0"><b>{{ formatoPesosColombianos(props.product.price +
                            (selected_size.price || 0)) }}</b></h4>
                    </div>
   




            </div>





        </div>

        
        </div>
  

       



            <!-- <Button style="position: absolute;right: -1rem; top: -1rem;aspect-ratio: 1 / 1;" icon="pi pi-plus" rounded></Button> -->

    </div>




</template>

<script setup>

import { formatoPesosColombianos } from '@/service/utils/formatoPesos';
import { computed, ref, onMounted } from 'vue';
import { usecartStore } from '@/stores/shoping_cart';
import router from '@/router/index.js'
import { useRoute } from 'vue-router'
import { URI } from '@/service/conection';
import Button from 'primevue/button';
import { useSitesStore } from '@/stores/site';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';
import { fetchService } from '@/service/utils/fetchService';
import Select from 'primevue/select';
import Tag from 'primevue/tag';
const toast = useToast()

const sitestore = useSitesStore()

const highResLoaded = ref({});
const currentImageSrc = ref({}); // Objeto para mantener la imagen actual de cada sede

const lowResImage = (product_name) => `${URI}/read-photo-product/${product_name}/96`;
const highResImage = (product_name) => `${URI}/read-photo-product/${product_name}/600`;

const currentImage = (site_id) => {
    return currentImageSrc.value[site_id] || lowResImage(site_id);
};

const loadHighResImage = (site_id) => {
    const img = new Image();
    img.src = highResImage(site_id);
    img.onload = () => {
        currentImageSrc.value[site_id] = highResImage(site_id); // Reemplaza el src de la imagen cuando está completamente cargada
        highResLoaded.value[site_id] = true;
    };
};


const route = useRoute()
const store = usecartStore()

const addToCart = (productToAdd) => {
    if (!sitestore.location.neigborhood?.name) {
  
        return;
    }

    store.addProductToCart(productToAdd);

    // Mostrar un toast de confirmación
    toast.add({
        severity: 'success',
        summary: 'Producto agregado',
        detail: `${productToAdd.product_name} se ha agregado al carrito.`,
        life: 3000 // Duración del toast en milisegundos (3 segundos)
    });
};


const loaded = ref(false)

const see = () => {
    loaded.value = true
}

const open = (product) => {



    store.setCurrentProduct(product)
    store.setVisible('currentProduct', true)


    // if (route.path != '/') {


    //     const category_name = route.params.menu_name
    //     const category_id = route.params.category_id

    //     const ruta = `/${category_name}/${category_id}/${product.product_name}/${product.id}`
    //     router.push(ruta)



    // }



}





function speak() {
    var text = props.product.price
    var msg = new SpeechSynthesisUtterance(text);

    // Obtiene todas las voces disponibles
    var voices = window.speechSynthesis.getVoices();

    // Filtra para encontrar una voz femenina en español
    var femaleVoice = voices.find(voice => voice.lang === 'es-ES' && voice.gender === 'female');

    // Si no encuentra una voz femenina específica, intenta al menos una en español
    if (!femaleVoice) {
        femaleVoice = voices.find(voice => voice.lang === 'es-ES');
    }

    // Asigna la voz encontrada al mensaje
    if (femaleVoice) {
        msg.voice = femaleVoice;
    } else {
        console.log('No se encontró una voz femenina en español.');
    }

    // Establece el idioma (aunque ya debería ser el correcto si la voz es correcta)
    msg.lang = 'es-ES';
    msg.rate = 1.2

    window.speechSynthesis.speak(msg);
}

const props = defineProps({
    product: {
        type: Object,
        default: {}
    },




});


onMounted(() => {



    highResLoaded.value = {};
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                loaded.value[img.dataset.index] = true; // Marca como cargado
                observer.unobserve(img); // Detiene la observación una vez cargada la imagen
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('img.lazy').forEach((img, index) => {
        img.dataset.index = index; // Asigna un índice a cada imagen para controlar su estado
        observer.observe(img);
    });
});



const truncatedDescription = computed(() => {
    const description = props.product.product_description;
    return description.substring(0, 100) + '...'
});




const imagenError = (Event) => {
    Event.target.src = 'https://salchimonster.com/images/logo.png'
}

const selected_size = ref({
    "id": 1,
    "name": "HAWAIANA",
    "price": null,
    "premium": false
})
const sizes = ref([])



</script>



<style scoped>
.container {
    display: grid;
    gap: 1rem;
    /* Spacing between grid items */
    grid-template-columns: 1fr;
    align-items: start;
    margin: 0;
    padding: 1rem;
    /* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); */
    border-radius: 0.5rem 0.5rem 1.4rem 0.6rem;
}

.container2{
    transition: all .2s ease;
}

.container2:hover{
    background-color:var(--primary-color);
    transform: translatey(-.5rem);
    color: white;
    cursor: pointer;

}

.character {
    display: none;
}


.name-phone{
    display: none;
}

/* Responsive adjustments */
/*  */


/* Responsive adjustments */


.imagen img {
    width: 100%;
    height: auto;
    /* Maintain aspect ratio */
    background-color: #fff;
    object-fit: contain;
    border-radius: 0.2rem;
}

.texto {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.rating {
    width: 1rem;
    /* Adjust based on your design */
}




.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to

/* .fade-leave-active in <2.1.8 */
    {
    opacity: 0;
}

/* Add additional styles for buttons, text, etc., as needed */





@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-100px);
        /* transform: scale(.5); */
        /* background-color: rgb(255, 255, 0); */
        /* filter: blur(1px); */
    }

    to {
        opacity: 1;
        /* filter: blur(1px); */

    }
}

.cargado {
    opacity: 0;
    /* Inicialmente invisible */
    animation: fadeIn .1s ease-out forwards;
    /* Duración de 1 segundo, 'ease-out' para desacelerar hacia el final, y 'forwards' para mantener el estado final visible */
}
</style>
