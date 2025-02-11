<template>



<div style="margin: auto;max-width: 50rem;margin-top: 8rem;" >


    <h1><b> DOMICILIO: {{ domicilio }}</b></h1>
          <!-- <img src="/src/assets/images/logo.webp" alt="" style="width: 5rem; border-radius: 50%; margin: auto;" /> -->
          <div style="width: 100%">
            <!-- <h5>Validar Zona</h5> -->
            <div style="width: 100%;display: flex;flex-direction: column;gap: 1rem;">

                    <div >
                        <!-- <label for="direccion">Dirección:</label> -->
                        <InputText style="width: 100%;" type="text" v-model="user.address" placeholder="Ingresa una dirección" />
                    </div>


                    <div>
                        <!-- <label for="barrio">Barrio:</label> -->
                        <InputText style="width: 100%;" type="text" v-model="neigborhood.name" placeholder="Ingresa un barrio" />
                    </div>

                    <div style="display: flex;width: 100%;justify-content: end">
                        <Button severity="help" size="small" style="font-weight: bold;" @click="validarDireccion">Validar</Button>

                    </div>
                </div>
           
        </div>
  

        <div class="my-4" id="map" ref="mapContainer" style="aspect-ratio: 4 / 2; width: 100%; "></div>



  
</div>

            
  
</template>

<script setup>
import { onMounted, ref, watch,onBeforeMount,nextTick} from "vue";
import axios from "axios";

import { useSitesStore } from "../../store/site";
import { URI } from "../../service/conection";
// import InputText from "primevue/inputtext";

const domicilio = ref('')


onMounted(async () => {
  await inicializarMapa();
});

const loadGoogleMaps = async() => {
  return new Promise((resolve, reject) => {
    if (typeof google !== "undefined") {
      resolve(); // The API is already loaded
      return;
    }

    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=marker`;
    script.async = true;
    script.defer = true;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
};


const inicializarMapa = async () => {
    try {
        await loadGoogleMaps(); // Asegúrate de que la API esté cargada

        if (!map.value) {
            map.value = new google.maps.Map(mapContainer.value, {
                
                center: { lat: 6.2717264431772985, lng: -75.55841542945669 }, // Coordenadas iniciales
                zoom: 14,
                minZoom: 13, // Zoom mínimo permitido
                maxZoom: 15,
             
            });
        }

        // Agregar el mapa KML desde el enlace público de Google My Maps
        const kmlLayer = new google.maps.KmlLayer({
            url: "https://www.google.com/maps/d/kml?mid=1fAENw6dNOT4jjL4tNdUtRX4Cqor1iVD5&ehbc=2E312F=en", // Enlace público del mapa
            map: map.value,
            preserveViewport: true, // Mantener la vista actual del mapa
        });

        // Manejar errores al cargar el archivo KML
        kmlLayer.addListener("status_changed", () => {
            if (kmlLayer.getStatus() !== google.maps.KmlLayerStatus.OK) {
                console.error("Error al cargar el mapa desde KML:", kmlLayer.getStatus());
            }
        });

    } catch (error) {
        console.error("Error al inicializar el mapa:", error);
    }
};

const store = useSitesStore()
const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
const direccion = ref("");
const map = ref(null);
const marker = ref(null);
const mapContainer = ref(null);
const barrio = ref()
const user = ref({})
const visible = true



const geocodeAddress = async (address) => {
    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(
        address
    )}&key=${GOOGLE_MAPS_API_KEY}`;
    try {
        const response = await axios.get(url);
        const results = response.data.results;
        if (results.length === 0) {
            throw new Error("No se pudo encontrar la dirección");
        }
        const { lat, lng } = results[0].geometry.location;
        console.log(response)
        return { lat, lng };
    } catch (error) {
        console.error("Error al geocodificar la dirección:", error);
        throw error;
    }
};

const validarDireccion = async () => {
    try {
        if (!user.value.address || !neigborhood.value) {
            alert("Por favor ingresa la dirección y el barrio.");
            return;
        }

        const complete = `${user.value.address}, ${neigborhood.value.name}, Medellín, Colombia`;
       
        const { lat, lng } = await geocodeAddress(complete);

        // Crear un marcador en el mapa
        if (marker.value) {
            marker.value.setMap(null); // Elimina el marcador anterior, si existe
        }

        marker.value = new google.maps.Marker({
            position: { lat, lng }, // Posición del marcador
            map: map.value, // Agrega el marcador al mapa actual
            title: direccion.value, // Título del marcador
            animation: google.maps.Animation.DROP, // Animación al aparecer
        });


        // Centrar el mapa en la dirección ingresada inicialmente
        map.value.setCenter({ lat, lng });
        map.value.setZoom(14);

        // Consultar la zona en el backend
        const response = await axios.post(`${URI}/consultar_zona/`, {
            latitud: lat,
            longitud: lng,
        });

        const result = response.data;
        if (result.zona) {
            // Mostrar información de la zona
            alert(`Zona: ${result.zona}. Valor domicilio: ${result.valor_domicilio}`);

            domicilio.value = result.zona
            // Centrar el mapa en las coordenadas de la zona
            if (result.latitud && result.longitud) {
                map.value.setCenter({ lat: result.latitud, lng: result.longitud });
                map.value.setZoom(15); // Ajusta el nivel de zoom según sea necesario
            }

       
        } else {
            alert("No se encontró cobertura.");
        }
    } catch (error) {
        alert(error.message || "Error al procesar la dirección.");
    }
};


const neigborhood = ref({
    delivery_price:0,
    name:''
})



const updateNeighborhood = async(valor, direccion) => {

    neigborhood.value = valor
    store.location.neigborhood.delivery_price = neigborhood.value.delivery_price
    store.visibles.currentSite = false

    user.value.address = direccion
    console.log(valor)
}


</script>


<style scoped>
@keyframes rot {
    0% {
        transform: translatey(-50%) scale(1.25, 0.75);
    }

    50% {
        transform: translatey(-150%) scale(1, 1);
    }

    100% {
        transform: translatey(-50%) scale(1.25, 0.75);
    }
}

* *:focus {
    outline: none;
    border: none;
}

.imagen {
    margin: 200px;
    width: 100px;
    /* overflow: hidden;  */
    animation: rot 0.7s infinite;
    transform-origin: center bottom;
}

.img-cart:hover {
    transform: scale(1.3);
}



.img-cart {
    transition: all .3s ease;
}







@media (min-width: 767px) {
    .scroll {
        max-height: 45rem;
        overflow-y: auto;

    }

    .add-car {
        width: 50%;
    }
}

.led {
    animation: cambiaColor 1s infinite;
    /* 3s de duración, animación infinita */
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

.img-before {
    /* background-color: rgba(0, 0, 0, 0.235); */
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0%;
    left: 0;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;

}

.carro:hover {
    /* transform: scalex(1.2); */
    background-color: #ff62004a;
    cursor: pointer
}

.menu-button-new {
    background-color: var(--primary-color);
    /* padding: 1rem; */
    /* margin: 0 1rem; */
    border: none;
    font-size: 20px;
    /* transition: all  0.3s; */
    /* font-weight: bold; */
    border-radius: 10px;
    color: #fff;
    width: 300px;
    transition: all 0.3s ease;
    text-align: center;

}

.fondo-movil {
    background-color: var(--primary-color);
}

.fondo-pc {
    background-color: #626262;
    /* overflow-x: hidden; */
}

.img-cont {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    position: relative;
    overflow: hidden;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;


}

.default-image {
    filter: blur(10px);
    position: relative;
}

*:focus {
    border: none;
    outline: none;
}

.default-image::before {
    content: 'hola';
    width: 100%;
    /* background-color: rgba(177, 99, 9, 0.1); */
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
}

.selected {
    background-color: #ff620050
}

.menu-button-new:hover {
    /* filter: brightness(1.5);  
   */
    background-color: black;
    cursor: pointer;

}




.cart {

    /* box-shadow: 0px 0px 30px rgba(0, 0, 0, 0.4); */



}

.img-cont {
    /* background-color:rgb(255, 255, 255); */
    /* display: flex; */
    /* justify-content: flex-start; */
    align-items: start;

    /* box-shadow: 30px 0px 30px rgba(0, 0, 0, 0.5); */
    height: 100%;
    /* flex-direction: column; */
}



.imagen {
    /* position: fixed; */
    width: 100%;
    height: auto;
    object-fit: contain;
    transition: all ease 0.5s;
    /* margin-left: 1vw; */
    border-radius: 50px;

    /* filter: drop-shadow(-2px 2px 15px rgba(0, 0, 0, 0.7)); */

}

.imagen:hover {
    transform: scale(1.1);
    ;

    /* box-shadow: 0px 0px 30px rgba(0, 0, 0, 1); */
    filter: brightness(1.2) drop-shadow(-2px 2px 15px rgba(0, 0, 0, ));
    /* filter: drop-shadow(-2px 2px 15px rgba(0, 0, 0, 0.7)); */

}

.producto {
    /* filter: brightness(1.2); */
}

.info {
    /* padding-left: 10%; */

    /* padding-top: 5%; */
    display: flex;
    flex-direction: column;
    align-items: fle;
    /* gap: 10px; */
    /* box-shadow: 0px 0px 30px rgba(0, 0, 0, 1); */
}

.ordenar {
    transition: all 0.2s ease;
    border: 2px solid var(--primary-color);
    /* // font-weight: bold; */
    font-size: 20px;
    /* // margin-bottom: 200px; */
    background-color: transparent;
    border-radius: 5px;
}

.carro {

    border: none;
    /* // font-weight: bold; */
    /* font-size: 20px; */
    /* // margin-bottom: 200px; */
    background-color: transparent;
    border-radius: 5px;
    margin: auto;
    /* border-radius:; */
}

.whatsapp:hover {
    transform: scale(1.1);
}

.ver-mas:hover {
    background-color: var(--primary-color);
    transform: scale(1.1);



    color: #fff;
    cursor: pointer;
}


/* // .icono{
//     color: var(--primary-color);
// } */
.ver-mas:hover>.icono {
    /* // background-color: var(--primary-color);

// display: none; */
    color: #fff;
    transform: translateX(5px);
}

.info-header {
    display: flex;
    justify-content: space-between;
    /* align-items: center; */
    /* gap: 20px; */
}

.salsa {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: start;
    padding: 0;

    margin: 0;


}

.salsa:hover {
    color: var(--primary-color);
}

.salsas {
    display: flex;
    padding: 0;
    margin: 0;


}

.whatsapp {
    /* background-color: red; */
    /* min-width: 1024px; */
    width: 3rem;
    height: 3rem;
    display: flex;
    transition: all ease .3s;
    right: 5rem;
    bottom: 9rem;

    /* align-items: center; */
    justify-content: center;
    background-color: #25D366;
    border-radius: 50%;
    position: absolute;

}

@media (max-width:500px) {
    .whatsapp {
        /* background-color: red; */
        /* min-width: 1024px; */
        width: 4rem;
        height: 4rem;
        right: 5%;
        bottom: 130%;

    }
}


.led {
    animation: cambiaColor 1s infinite;
    /* 3s de duración, animación infinita */
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

.adiciones {
    display: flex;
    padding: 0;
    margin: 0;

}

a {
    text-decoration: none;
}

* {
    text-transform: uppercase;
}

.texto {
    /* width: 40%; */
    /* min-width: 200px; */
    padding-right: 20px;
    /* min-width: 200px; */
    /* margin-right: 20px; */
}

.icono {
    transition: all 0.2s ease;
    color: var(--primary-color);
    transform: translateX(-5px);
    font-weight: bold;
}

.title {}

.nombre-salsa::after {}


.animador {
    animation: para-aca 1s infinite ease;

}


@keyframes para-aca {
    0% {
        transform: translateX(0%);
    }

    50% {
        transform: translateX(100%)
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




.fondo-pc {
    background-color: rgb(247, 247, 247);
}

dialog {
    ::-webkit-scrollbar {
        width: 0.5rem;
        /* Ancho de la barra de desplazamiento */
        padding-top: 1rem;
        position: absolute;
        /* display: none; */
    }

    .clase {}

    /* Estilo del pulgar de la barra de desplazamiento */
    /* WebKit (Chrome, Safari) */
    ::-webkit-scrollbar-thumb {
        background-color: var(--primary-color);
        /* Color del pulgar de la barra de desplazamiento */
        border-radius: 9px;
        /* border: 5px solid var(--primary-color); */
        height: 10rem;
        width: 10rem;
        /* display: none;  */
    }
}
</style>
