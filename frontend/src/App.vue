<script setup>
import AppLayout from './AppLayout/AppLayout.vue';
import Button from 'primevue/button';
import VistaProducto from './views/VistaProducto.vue';
import siteDialog from './views/siteDialog.vue';
import router from './router';
import Toast from 'primevue/toast';
import Badge from 'primevue/badge';
import { useSitesStore } from './stores/site';
import { onMounted, watch, onBeforeUnmount, ref } from 'vue';
import { usecartStore } from './stores/shoping_cart';
import { URI } from './service/conection';
import Banner from './components/Banner.vue';

const store  = useSitesStore();
const cartStore = usecartStore();


// Para saber si el menú está oculto o visible
const isHidden = ref(false);
let scrollTimeout = null;

// Función que se ejecuta durante el scroll
function handleScroll() {
  // Oculta inmediatamente el menú al comenzar a hacer scroll
  isHidden.value = true;

  // Reiniciamos el temporizador cada vez que se produce scroll
  if (scrollTimeout) {
    clearTimeout(scrollTimeout);
  }

  // Pasado un tiempo sin scroll (por ejemplo 300 ms), mostramos de nuevo
  scrollTimeout = setTimeout(() => {
    isHidden.value = false;
  }, 500);
}

// Agregamos y removemos el eventListener del scroll
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});

// Función para obtener el status del sitio
const obtenerstatus = async () => {
  const siteStore = useSitesStore();

  try {
    const response = await fetch(`${URI}/site/${31}/status`);
    const data = await response.json();

    siteStore.status = data;
  } catch (error) {
    console.error('Error al obtener el status:', error);
    siteStore.status = 'cerrado';
  }
};

// Guardamos el ID del intervalo para poder limpiarlo
let intervalId;

onMounted(() => {
  // Ejecutamos inicialmente la función
  obtenerstatus();

  // Repetimos cada 5 segundos
  intervalId = setInterval(() => {
    obtenerstatus();
  }, 5000);
});

onBeforeUnmount(() => {
  // Limpiamos el intervalo al desmontar el componente
  clearInterval(intervalId);
});
</script>

<template>
  <!-- CARGANDO... -->
  <div
    class=""
    v-if="store.visibles.loading"
    style="width: 100vw;pointer-events: none;flex-direction: column; height: 100vh;position: fixed;display: flex;align-items: center;justify-content: center; left: 0;right: 0;z-index: 99999999;"
  >
    <div class="imagen" style="display: flex;gap: 1rem; flex-direction: column; align-items:center;">
      <img src="/public/images/logo.png" style="width:20vw ;max-width: 100px;" alt="">
      <h5 style="color: white;">Cargando...</h5>
    </div>
  </div>

  <Toast />
  <router-view />

  <!-- Menú inferior (visible en pantallas pequeñas) -->
  <div
    class="menu-button2"
    :class="{ 'menu-button2--hidden': isHidden }"
    style="position: fixed; box-shadow: 0 -.3rem 1rem #00000040; left: 0rem; bottom: 0; background-color:white; z-index: 900; width: 100%; justify-content: center;"
  >
    <div class="social-media2" style="padding: .5rem; overflow: hidden; width: min-content;">
      <a href="https://www.facebook.com/ingmaster.com.co/" style="background-color: var(--primary-color);">
        <Button
          style="padding: 0;border-radius: .5rem;overflow: hidden;"
          size="large"
          text
          class="menu-bars text-facebook p-2"
        >
          <i style="color: #fff !important;" class="pi pi-facebook text-icon p-0 m-0"></i>
        </Button>
      </a>

      <a href="https://www.instagram.com/ing_master_refrigeracion/" style="background-color: var(--primary-color);">
        <Button style="padding: 0;" size="large" text class="menu-bars text-instagram p-2">
          <i class="pi pi-instagram "></i>
        </Button>
      </a>

      <a href="https://wa.link/z72oac" style="background-color: var(--primary-color);">
        <Button style="padding: 0;" size="large" text class="menu-bars text-whatsapp p-2">
          <i class="pi pi-whatsapp"></i>
        </Button>
      </a>
    </div>
  </div>

  <!-- Vistas/Dialogs -->
  <VistaProducto />
  <siteDialog />

  <!-- Botón del carrito (ejemplo) 
    <div class="cart-button" style="">
      <Button class="botomcar" @click="router.push('/cart')" style="">
        <i class="pi pi-shopping-cart"></i>
      </Button>
      <Badge
        v-if="cartStore.cart.products.length > 0"
        style="position: absolute;left: 70% ; bottom:60%;aspect-ratio: 1  / 1;border-radius: 50%;"
      >
        {{ cartStore.cart.products.length }}
      </Badge>
    </div>
  -->
</template>

<style scoped>
.layout {
  margin: auto;
  position: relative;
}

.cart-button {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
  display: none;
}

.botomcar {
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  width: 4rem;
  background-color: var(--primary-color);
  border: none;
}

@media (width > 900px) {
  .cart-button {
    right: 3rem;
    bottom: 5rem;
    display: flex;
  }
}

.app-topbar-container {}

.logo-sesion {
  display: flex;
  align-items: center;
  justify-content: start;
  gap: 1rem;
}

.menu-bars {
  font-weight: bold;
  aspect-ratio: 1 / 1;
  padding: 9;
  color: var(--primary-color);
  min-width: max-content;
}

i {
  font-size: 1.8rem;
  padding: .1rem;
}

/* Barra inferior fija */
.menu-button2 {
  position: fixed;
  left: 0rem;
  bottom: 0;
  width: 100%;
  z-index: 900;
  display: flex;
  justify-content: center;
  background-color: white;
  box-shadow: 0 -.3rem 1rem #00000040;
  transition: transform 0.3s ease-in-out;
  transform: translateY(0); /* Por defecto, visible */
}

/* Clase que se activa cuando isHidden es true */
.menu-button2--hidden {
  transform: translateY(100%);
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: .5rem;
}

* {
  border-radius: .5rem;
}

.text-facebook {
  background: #fff;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-instagram {
  background: #fff;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-whatsapp {
  background: #fff;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.social-media2 {
  display: flex;
  gap: .5rem;
}

.social-media {
  display: flex;
  gap: .5rem;
}

.nav-bar {
  display: flex;
  width: 100%;
  gap: 1rem;
  align-items: center;
  height: 2.5rem;
  justify-content: end;
}

.search {
  width: 100%;
  max-width: 400px;
  background-color: white;
  border: none;
}

.header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-bottom: .5rem;
}

.imagen {
  animation: hithere 1s ease infinite;
  background-color: rgb(0 19 59 / 85%);
  backdrop-filter: blur(5px);
  padding: 1rem;
  aspect-ratio: 1 / 1;
}

@keyframes hithere {
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

h1 {
  font-family: "Luckiest Guy", cursive;
  letter-spacing: .1cap;
  font-size: 1.5rem;
  color: white;
  text-decoration: none;
}

.menu-button {
  display: flex;
  justify-content: end;
  padding: 0;
  margin: 0;
}

@media (width < 1400px) {
  .app-topbar-container {
    padding: 0 1rem;
  }
}

@media (width < 900px) {
  .app-topbar-container {
    padding: 0 1rem;
  }
  .menus {
    display: none;
  }
}

@media (width > 900px) {
  .button-barrras {
    display: none;
  }
  .menu-button2 {
    display: none;
  }
}

* {
  text-decoration: none;
}

.menu {
  display: flex;
}

@media (width < 900px) {
  .menu-button {
    display: none;
  }
}
</style>
