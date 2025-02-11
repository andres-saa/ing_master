<template>
    <Dialog
        :closable="false"
        v-model:visible="store.visibles.currentSite"
        :style="{ width: '100vw' }"
        header="Selección del Barrio"
        :modal="true"
        class="p-fluid m-3 p-2"
        @show="onDialogShow"
        style="background-color: white; position: relative; border-radius: .5rem; padding-top: 2rem; max-width: 35rem;"
    >
        <template #header>
            <div style="width: 100%">
                <div style="width: 100%; display: flex; flex-direction: column; gap: 1rem;">
                    <div>
                        <InputText style="width: 100%;" type="text" v-model="temp_dir" placeholder="Ingresa una dirección" />
                    </div>
                    <div>
                        <InputText style="width: 100%;" type="text" v-model="temp_barrio" placeholder="Ingresa un barrio" />
                    </div>
                </div>
            </div>
        </template>

        <div class="my-0" id="map" ref="mapContainer" style="aspect-ratio: 4 / 2; width: 100%;"></div>

        <template #footer>
            <div style="width: 100%; display: flex; flex-direction: column; align-items: center;">
                <div class="field col-12 p-0" style="width: 100%; display: flex; flex-direction: column; gap: 0.5rem;">
                    <Tag>
                        <h5 v-if="neigborhood?.delivery_price">Domicilio: {{ formatoPesosColombianos(neigborhood?.delivery_price) }}</h5>
                        <h6 class="m-0" v-else>Selecciona una dirección para ver el valor del domicilio o presiona recoger en el local</h6>
                    </Tag>
                    <Button
                        size="small"
                        v-if="validado"
                        @click="updateneigborhood(temp_barrio, temp_dir)"
                        label="Guardar"
                        style="width: 100%; text-align: center; background-color: black; color: white; border: none; padding: 10px 20px;"
                    ></Button>
                    <Button
                        v-else
                        size="small"
                        @click="validarDireccion"
                        label="Validar"
                        style="width: 100%; text-align: center;"
                    ></Button>
                    <Button
                        size="small"
                        @click="recogerLocal"
                        label="Recoger en el local"
                        style="width: 100%; text-align: center;"
                        severity="danger"
                    ></Button>
                </div>
            </div>
        </template>

        <Button
            style="position: absolute; right: -1rem; top: -1rem;"
            icon="pi pi-times"
            rounded
            severity="danger"
            @click="store.visibles.currentSite = false"
        ></Button>
    </Dialog>
</template>

<script setup>
import { ref, watch, nextTick } from "vue";
import axios from "axios";
import { useUserStore } from '@/stores/user';
import { useSitesStore } from "@/stores/site";
import InputText from "primevue/inputtext";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import { formatoPesosColombianos } from "@/service/utils/formatoPesos";
import Tag from "primevue/tag";

// Estados reactivos
const temp_barrio = ref('');
const temp_dir = ref('');
const map = ref(null);
const marker = ref(null);
const mapContainer = ref(null);
const neigborhood = ref({ delivery_price: 0, name: '' });
const validado = ref(false);

// Acceso a las tiendas
const store = useSitesStore();
const user = useUserStore();
const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

// Implementación del singleton para cargar Google Maps API
let googleMapsPromise = null;

const loadGoogleMaps = () => {
    if (googleMapsPromise) {
        return googleMapsPromise;
    }

    googleMapsPromise = new Promise((resolve, reject) => {
        if (typeof google !== "undefined" && google.maps) {
            resolve(); // La API ya está cargada
            return;
        }

        const script = document.createElement("script");
        script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=marker`;
        script.async = true;
        script.defer = true;
        script.onload = () => {
            resolve();
        };
        script.onerror = () => {
            reject(new Error("Failed to load Google Maps"));
        };
        document.head.appendChild(script);
    });

    return googleMapsPromise;
};

// Inicializar el mapa
const inicializarMapa = async () => {
    try {
        await loadGoogleMaps(); // Carga la API si aún no está cargada

        if (mapContainer.value) {
            map.value = new google.maps.Map(mapContainer.value, {
                center: { lat: 6.2717264431772985, lng: -75.55841542945669 }, // Coordenadas iniciales
                zoom: 14,
                minZoom: 13, // Zoom mínimo permitido
                maxZoom: 15,
            });

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
        } else {
            console.error("mapContainer no está disponible en el DOM.");
        }
    } catch (error) {
        console.error("Error al inicializar el mapa:", error);
    }
};

// Geocodificar una dirección
const geocodeAddress = async (address) => {
    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${GOOGLE_MAPS_API_KEY}`;
    try {
        const response = await axios.get(url);
        const results = response.data.results;
        if (results.length === 0) {
            throw new Error("No se pudo encontrar la dirección");
        }
        const { lat, lng } = results[0].geometry.location;
        return { lat, lng };
    } catch (error) {
        console.error("Error al geocodificar la dirección:", error);
        throw error;
    }
};

// Validar la dirección ingresada
const validarDireccion = async () => {
    try {
        if (!temp_dir.value || !temp_barrio.value) {
            alert("Por favor ingresa la dirección y el barrio.");
            return;
        }

        const complete = `${temp_dir.value}, ${temp_barrio.value}, Medellín, Colombia`;
        const { lat, lng } = await geocodeAddress(complete);

        // Crear un marcador en el mapa
        if (marker.value) {
            marker.value.setMap(null); // Elimina el marcador anterior, si existe
        }

        marker.value = new google.maps.Marker({
            position: { lat, lng }, // Posición del marcador
            map: map.value, // Agrega el marcador al mapa actual
            title: temp_dir.value, // Título del marcador
            animation: google.maps.Animation.DROP, // Animación al aparecer
        });

        // Centrar el mapa en la dirección ingresada inicialmente
        map.value.setCenter({ lat, lng });
        map.value.setZoom(14);

        // Consultar la zona en el backend
        const response = await axios.post("https://tezos-back.arhook.com/consultar_zona/", {
            latitud: lat,
            longitud: lng,
        });

        const result = response.data;
        if (result.zona) {
            // Centrar el mapa en las coordenadas de la zona
            if (result.latitud && result.longitud) {
                map.value.setCenter({ lat: result.latitud, lng: result.longitud });
                map.value.setZoom(15); // Ajusta el nivel de zoom según sea necesario
            }

            neigborhood.value = {
                name: temp_barrio.value,
                delivery_price: result.valor_domicilio
            };
            validado.value = true;
        } else {
            alert("No se encontró cobertura.");
        }
    } catch (error) {
        alert(error.message || "Error al procesar la dirección.");
    }
};

// Actualizar el barrio seleccionado
const updateneigborhood = async (valor, direccion) => {
    store.location.neigborhood.name = valor;
    store.location.neigborhood.delivery_price = neigborhood.value.delivery_price;
    store.visibles.currentSite = false;

    user.user.address = direccion;
    console.log(valor);

    store.location.neigborhood = neigborhood.value;
};

// Recoger en el local
const recogerLocal = async () => {
    store.location.neigborhood.name = 'Recoger en el local';
    store.location.neigborhood.delivery_price = 0;
    store.visibles.currentSite = false;

    user.user.address = '';
};

// Función para manejar la apertura del diálogo
const onDialogShow = async () => {
    validado.value = false;
    await nextTick();
    await inicializarMapa();
};
</script>
<style scoped>
/* Tus estilos aquí */
</style>
