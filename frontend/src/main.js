import './assets/main.css'
import 'primeicons/primeicons.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import persistedState from 'pinia-plugin-persistedstate'
import PrimeVue from 'primevue/config'
import App from './App.vue'
import router from './router'

import Aura from '@primevue/themes/aura'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js' // Incl
import ToastService from 'primevue/toastservice'

const app = createApp(App)

const pinia = createPinia()
pinia.use(persistedState) // Usa el plugin de persistencia

app.use(PrimeVue, {
  // Default theme configuration
  theme: {
      preset: Aura,
      options: {
          prefix: 'p',
          darkModeSelector: 'light',
          cssLayer: false
      }
  }
});

app.use(ToastService) // Registra el servicio ToastService

app.use(pinia)
app.use(router)
app.mount('#app')
