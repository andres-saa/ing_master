<template>
  <Banner></Banner>

  <div style="padding: 3rem;">
    <h2><b>Arrastra y Reordena las Imágenes</b></h2>

    <Button
      style="margin:1rem 0;background-color: var(--primary-color);border: none;"
      label="Agregar Imágenes"
      icon="pi pi-upload"
      @click="openAddImageDialog"
    />

    <!-- Diálogo para agregar imágenes -->
    <Dialog
      header="Agregar Imágenes"
      v-model:visible="isAddImageDialogOpen"
      modal
      style="width: 40rem;"
    >
      <div class="image" style="display: flex; flex-direction: column; position: relative; justify-content: end; align-items: end;">
        <img v-if="imagePreview" :src="imagePreview" alt="Preview"
             style="width: 100%; aspect-ratio: 19 / 9; background-color: rgb(255, 255, 255); object-fit: cover; border-radius: 0.2rem;" />

        <div v-if="uploading" style="position: absolute; left: 0; top: 0; width: 100%; display: flex; justify-content: center; align-items: center; height: 100%; background-color: #ffffff80;">
          <ProgressSpinner strokeWidth="8" style="color: white;"></ProgressSpinner>
        </div>

        <Button class="my-3" severity="help" @click="triggerFileSelect">Agregar foto</Button>
        <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" multiple accept="image/*" />
      </div>

      <!-- Puedes agregar más campos si es necesario -->

      <template #footer>
        <div class="col-12 px-0 pb-0">
          <Button @click="confirmAddImages" severity="success" label="Guardar"></Button>
        </div>
      </template>
    </Dialog>

    <!-- Lista de imágenes arrastrables -->
    <div class="draggable-container">
      <div
        style="position:relative"
        v-for="(img, index) in sortedImages"
        :key="img.id"
        class="draggable-item"
        draggable="true"
        :class="{ 'drag-over': dragOverIndex === index }"
        @dragstart="onDragStart(index)"
        @dragenter.prevent="onDragEnter(index)"
        @dragover.prevent
        @dragleave="onDragLeave"
        @drop="onDrop(index)"
        :data-index="img.index"
      >
        <img :src="`${URI}/read-photo-product/${img.src}`" :alt="img.title" />
        
        <Button
          style="border-radius:50%; position:absolute;background-color:var(--primary-color);border:3px solid;aspect-ratio:1 / 1; right:-1.5rem;top:-1.5rem"
          icon="pi pi-times"
          severity="info"
          class="delete-button"
          @click.stop="openDeleteDialog(img)"
        />
      </div>

      <!-- Diálogo de confirmación de eliminación -->
      <Dialog
        header="Confirmar Eliminación"
        v-model:visible="isDeleteDialogOpen"
        modal
        :closable="false"
        style="width: 350px"
      >
        <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle" style="font-size: 2rem; color: #ff9800;"></i>
          <span class="message">¿Estás seguro de que deseas eliminar "{{ imageToDelete?.title }}"?</span>
        </div>
        <div class="dialog-footer">
          <Button label="Sí, eliminar" icon="pi pi-check" class="p-button-danger" @click="confirmDelete" />
          <Button label="Cancelar" icon="pi pi-times" class="p-button-secondary" @click="closeDeleteDialog" />
        </div>
      </Dialog>
    </div>
  </div>
</template>



<script setup>
import { ref, computed } from 'vue'
import Banner from './Banner.vue'
// import { ProgressSpinner } from 'primevue/progressspinner'
import { productService } from '@/service/ProductService';
import { URI } from '../../service/conection';
// Lista inicial de imágenes (id, src, title, index)
const images = ref([])

// Computed para ordenar las imágenes basado en el índice
const sortedImages = computed(() =>
  images.value.slice().sort((a, b) => a.index - b.index)
)

// Indica qué elemento estamos arrastrando
const draggedItemIndex = ref(-1)
// Para resaltar sobre qué elemento estamos “sobrevolando”
const dragOverIndex = ref(-1)

// Estado del diálogo de eliminación
const isDeleteDialogOpen = ref(false)
const imageToDelete = ref(null)

// Estado del diálogo de agregar imágenes
const isAddImageDialogOpen = ref(false)
const uploading = ref(false)
const selectedFiles = ref([])
const imagePreview = ref(null)

// Referencia al input de archivo
const fileInput = ref(null)

// Funciones de arrastrar y soltar
function onDragStart(index) {
  draggedItemIndex.value = index
}

function onDragEnter(index) {
  dragOverIndex.value = index
}

function onDragLeave() {
  dragOverIndex.value = -1
}

function onDrop(index) {
  if (index === draggedItemIndex.value) return

  const draggedItem = sortedImages.value[draggedItemIndex.value]
  const originalIndex = images.value.findIndex(img => img.id === draggedItem.id)

  images.value.splice(originalIndex, 1)
  images.value.splice(index, 0, draggedItem)

  images.value.forEach((img, idx) => {
    img.index = idx
  })

  draggedItemIndex.value = -1
  dragOverIndex.value = -1
}

// Funciones para el diálogo de eliminación
function openDeleteDialog(img) {
  imageToDelete.value = img
  isDeleteDialogOpen.value = true
}

function closeDeleteDialog() {
  isDeleteDialogOpen.value = false
  imageToDelete.value = null
}

function confirmDelete() {
  if (imageToDelete.value) {
    const indexToRemove = images.value.findIndex(img => img.id === imageToDelete.value.id)
    if (indexToRemove !== -1) {
      images.value.splice(indexToRemove, 1)
      images.value.forEach((img, idx) => {
        img.index = idx
      })
    }
  }
  closeDeleteDialog()
}

// Funciones para el diálogo de agregar imágenes
function openAddImageDialog() {
  isAddImageDialogOpen.value = true
}

function triggerFileSelect() {
  fileInput.value.click()
}

function handleFileUpload(event) {
  const files = event.target.files
  if (files.length === 0) return

  selectedFiles.value = Array.from(files)
  // Generar vista previa para la primera imagen seleccionada (puedes personalizar esto)
  if (selectedFiles.value.length > 0) {
    imagePreview.value = URL.createObjectURL(selectedFiles.value[0])
  }

  // Resetear el input para permitir subir la misma imagen nuevamente si se desea
  event.target.value = ''
}

async function confirmAddImages() {
  if (selectedFiles.value.length === 0) {
    alert('Por favor selecciona al menos una imagen.')
    return
  }

  uploading.value = true

  try {
    for (const file of selectedFiles.value) {
      const formData = new FormData()
      formData.append('file', file)

      // Aquí debes reemplazar `productService.uploadPhoto` por el servicio adecuado para tu caso
      const response = await productService.uploadPhoto(formData)

      const newImage = {
        id: Date.now() + Math.random(),
        src: response.image_identifier, // Asegúrate de que el backend devuelva la URL de la imagen
        title: file.name,
        index: images.value.length
      }

      images.value.push(newImage)
    }

    // Limpiar el estado
    selectedFiles.value = []
    imagePreview.value = null
    isAddImageDialogOpen.value = false
    // alert('Imágenes cargadas exitosamente!')
  } catch (error) {
    console.error('Error al subir las imágenes:', error)
    alert('Hubo un error al subir las imágenes.')
  } finally {
    uploading.value = false
  }
}
</script>


<style scoped>
.draggable-container {
  width: 100%;
  margin: 1rem auto;
  gap: 2rem;
  flex-wrap: wrap;
  display: flex;
  align-items: center;
  justify-content: start;
}

.upload-section {
  margin-bottom: 1rem;
}

.upload-section button {
  /* Los estilos del botón son manejados por PrimeVue */
}

.draggable-item {
  position: relative; /* Para posicionar el botón de eliminación */
  width: 100%;
  max-width: 15rem;
  border-radius: 4px;
  height: min-content;
  cursor: move; /* Indicador de arrastre */
  text-align: center;
  background-color: #fff;
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.draggable-item img {
  max-width: 15rem;
  display: block;
  margin: 0 auto 0.5rem;
  aspect-ratio: 19 / 9;
  object-fit: cover;
}

.draggable-item.drag-over {
  background-color: #f0f0f0;
  border-color: #aaa;
}

/* Estilos para el botón de eliminación */
.delete-button {
  position: absolute;
  top: 8px;
  right: 8px;
}

/* Estilos para el contenido de confirmación */
.confirmation-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.confirmation-content .pi-exclamation-triangle {
  flex-shrink: 0;
}

.confirmation-content .message {
  flex-grow: 1;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}
</style>
