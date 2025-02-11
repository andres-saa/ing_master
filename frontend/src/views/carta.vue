<template>
    <div class="noticias" style="max-width: 1300px; margin: auto;">
      <!-- <h2> Noticias Master</h2> -->
  
      <!-- Indicador de carga -->
      <div v-if="loading" class="loading">
        <p>Cargando imágenes...</p>
        <!-- Puedes reemplazar esto con un spinner o cualquier otro indicador de carga -->
      </div>
  
      <!-- Mensaje si no hay imágenes -->
      <div v-else-if="images.length === 0" class="no-images">
        <p>No hay imágenes en la noticias.</p>
      </div>
  
      <!-- Contenedor de imágenes -->
      <div v-else class="images-container">
        <img 
          v-for="img in images" 
          :key="img.id" 
          :src="`${URI}/read-photo-product/${img.src}`" 
          :alt="img.title" 
          class="img"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { fetchService } from '@/service/utils/fetchService' // Asegúrate de que la ruta es correcta
  import { URI } from '@/service/conection'
  
  // Estado reactivo para almacenar las imágenes
  const images = ref([])
  
  // Estado para manejar la carga
  const loading = ref(false)
  
  // Función para obtener las imágenes desde el backend
  const fetchImages = async () => {
    loading.value = true
    try {
      // Realiza la solicitud GET a la URI correspondiente
      const response = await fetchService.get(`${URI}/carta/`)
      
      // Asumiendo que la respuesta es un array de objetos con al menos: id, img_identifier, title
      images.value = response.map(noticias => ({
        id: noticias.id,
        src: noticias.img_identifier, // Asegúrate de que 'img_identifier' es la propiedad correcta
        title: noticias.title || 'Sin título'
      }))
    } catch (error) {
      console.error('Error al obtener las imágenes de la noticias:', error)
      // Puedes manejar el error mostrando una notificación al usuario
    } finally {
      loading.value = false
    }
  }
  
  // Ejecuta fetchImages cuando el componente se monta
  onMounted(() => {
    fetchImages()
  })
  </script>
  
  <style scoped>
  .noticias {
    max-width: 900px;
    margin: auto;
    /* padding: 2rem; */
  }
  
  .images-container {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    /* gap: 1rem; */
    justify-content: center;
    /* margin: auto; */
  }
  
  .img {
    width: 100%;
    /* border-radius: 1rem; */
    overflow: hidden;
    object-fit: cover;
  }
  
  .loading, .no-images {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
    font-size: 1.2rem;
    color: #555;
  }
  
  h2 {
    margin: 2rem 0;
    font-family: roboto;
    font-weight: bold;
    text-align: center;
    font-size: 3rem;
    color: black;
    transition: all ease 0.3s;
  }
  </style>
  