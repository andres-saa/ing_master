<template>
  <div class="container" style="background-color: red; min-width: 100%;">
    <!-- Botón para ir al banner anterior (sólo se muestra si hay más de un banner) -->
    <Button class="button-left" v-if="banners.length > 1" @click="prevBanner">
      <i class="pi pi-angle-left"></i>
    </Button>

    <!-- Contenedor (slider) con las imágenes -->
    <div class="slider" :style="sliderStyle">
      <img
        v-for="(banner, idx) in banners"
        :key="banner.id ?? idx"
        :src="`${URI}/read-photo-product/${banner.img_identifier}`"
        :alt="banner.title ?? `Banner ${idx}`"
      />
    </div>

    <!-- Botón para ir al banner siguiente (sólo se muestra si hay más de un banner) -->
    <Button class="button-right" v-if="banners.length > 1" @click="nextBanner">
      <i class="pi pi-angle-right"></i>
    </Button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
// import { Button } from 'primevue/button' // Ajusta si no usas PrimeVue
import { fetchService } from '../../service/utils/fetchService'
import { URI } from '../../service/conection'

/**
 * Estado local:
 * - banners: array de banners (ordenados por "index").
 * - currentIndex: índice del banner actualmente visible en el slider.
 * - intervalId: para manejar el autoplay.
 */
const banners = ref([])
const currentIndex = ref(0)
let intervalId = null

/** Intervalo de autoplay en milisegundos. Ajusta a tu gusto. */
const INTERVAL_TIME = 3000

/**
 * onMounted: carga los banners desde el backend, los ordena por index,
 * y arranca el autoplay.
 */
onMounted(async () => {
  await loadBanners()
  startAutoplay()
})

/** onBeforeUnmount: limpia el autoplay al desmontar el componente */
onBeforeUnmount(() => {
  stopAutoplay()
})

/**
 * Carga los banners del backend y los ordena por la propiedad "index".
 * Asegúrate de que el backend retorne un array con { index, img_identifier, id, ... }
 */
async function loadBanners() {
  try {
    const data = await fetchService.get(`${URI}/banners`)
    // Ordenar el array según la propiedad "index" (ascendente)
    banners.value = data.sort((a, b) => a.index - b.index)
    currentIndex.value = 0
  } catch (error) {
    console.error('Error al cargar banners:', error)
  }
}

/** Inicia el autoplay (pasa al siguiente banner cada INTERVAL_TIME ms) */
function startAutoplay() {
  if (!intervalId && banners.value.length > 1) {
    intervalId = setInterval(() => {
      nextBanner()
    }, INTERVAL_TIME)
  }
}

/** Detiene el autoplay */
function stopAutoplay() {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

/** Cambia al siguiente banner (cíclicamente) */
function nextBanner() {
  if (banners.value.length === 0) return
  currentIndex.value = (currentIndex.value + 1) % banners.value.length
}

/** Cambia al banner anterior (cíclicamente) */
function prevBanner() {
  if (banners.value.length === 0) return
  currentIndex.value =
    (currentIndex.value - 1 + banners.value.length) % banners.value.length
}

/**
 * Computed que calcula el estilo de desplazamiento (translateX)
 * en función de currentIndex.
 */
const sliderStyle = computed(() => {
  const translateX = -currentIndex.value * 100
  return `transform: translateX(${translateX}%); transition: all 0.3s ease;`
})
</script>

<style scoped>
/* Contenedor principal */
.container {
  overflow: hidden;
  display: flex;
  align-items: center;
  position: relative;
  margin-top: 0rem;
  padding: 0;
  width: 100%;
}

/* Slider (contenedor de imágenes) */
.slider {
  display: flex;
  width: 100%;
  /* La transición se maneja en "sliderStyle" (computed) */
  padding: 0;
  margin: 0;
}

/* Ajustes de imagen */
img {
  width: 100%;
  min-width: 100%;
  aspect-ratio: 16/7; /* Ajusta según tu preferencia */
  object-fit: cover;
}

/* Botones de navegación */
.button-left,
.button-right {
  position: absolute;
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  padding: 0.5rem;
  background-color: #00000070;
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-left {
  left: 1rem;
}

.button-right {
  right: 1rem;
}

i {
  font-size: xx-large;
}

/* Ajustes en pantallas más pequeñas */
@media (max-width: 1100px) {
  .button-right {
    right: 0.5rem;
  }
  .button-left {
    left: 0.5rem;
  }
}
</style>
