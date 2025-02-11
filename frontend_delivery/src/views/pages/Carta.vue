<template>





  <div style="padding: 3rem;">
    <h2><b>Arrastra y Reordena las Imágenes de la carta</b></h2>

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
      <div
        class="image"
        style="
          display: flex;
          flex-direction: column;
          position: relative;
          justify-content: end;
          align-items: end;
        "
      >
        <!-- Vista previa de la primera imagen seleccionada -->
        <img
          v-if="imagePreview"
          :src="imagePreview"
          alt="Preview"
          style="
            width: 100%;
            aspect-ratio: 19 / 9;
            background-color: rgb(255, 255, 255);
            object-fit: cover;
            border-radius: 0.2rem;
          "
        />

        <!-- Spinner de carga mientras sube -->
        <div
          v-if="uploading"
          style="
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            background-color: #ffffff80;
          "
        >
          <ProgressSpinner strokeWidth="8" style="color: white" />
        </div>

        <Button class="my-3" severity="help" @click="triggerFileSelect"
          >Agregar foto</Button
        >
        <input
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
          style="display: none;"
          multiple
          accept="image/*"
        />
      </div>

      <template #footer>
        <div class="col-12 px-0 pb-0">
          <Button @click="confirmAddImages" severity="success" label="Guardar" />
        </div>
      </template>
    </Dialog>

    <!-- Lista de imágenes arrastrables -->
    <div class="draggable-container">
      <div
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
      >
        <!-- Muestra la imagen usando tu URI base -->
        <img
          :src="`${URI}/read-photo-product/${img.src}`"
          :alt="img.title"
        />

        <!-- Botón de eliminar -->
        <Button
          style="
            border-radius: 50%;
            position: absolute;
            background-color: var(--primary-color);
            border: 3px solid;
            aspect-ratio: 1 / 1;
            right: -1.5rem;
            top: -1.5rem;
          "
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
          <i class="pi pi-exclamation-triangle" style="font-size: 2rem; color: #ff9800"></i>
          <span class="message">¿Estás seguro de que deseas eliminar esta imagen?</span>
        </div>
        <div class="dialog-footer">
          <Button
            label="Sí, eliminar"
            icon="pi pi-check"
            class="p-button-danger"
            @click="confirmDelete"
          />
          <Button
            label="Cancelar"
            icon="pi pi-times"
            class="p-button-secondary"
            @click="closeDeleteDialog"
          />
        </div>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Componente opcional
// import carta from './carta.vue'

// Importa tu servicio y tu URI base
import { productService } from '@/service/ProductService'
import { URI } from '../../service/conection'

// -------------------- ESTADOS --------------------
const images = ref([])       // Lista de cartas en local
const draggedItemIndex = ref(-1)
const dragOverIndex = ref(-1)

// Diálogo de eliminación
const isDeleteDialogOpen = ref(false)
const imageToDelete = ref(null)

// Diálogo para agregar imágenes
const isAddImageDialogOpen = ref(false)
const uploading = ref(false)
const selectedFiles = ref([])
const imagePreview = ref(null)
const fileInput = ref(null)

// Ordenamos localmente las imágenes según index
const sortedImages = computed(() => {
  return images.value.slice().sort((a, b) => a.index - b.index)
})

// -------------------- CICLO DE VIDA --------------------
onMounted(async () => {
  await fetchcartas()
})

// -------------------- FUNCIONES A BACKEND --------------------
/** GET /cartas/ */
async function fetchcartas() {
  try {
    const response = await axios.get(`${URI}/carta/`)
    // Suponiendo que el backend retorna un array de objetos con al menos: id, index, img_identifier, etc.
    // Mapeas si necesitas adaptarlo a tu uso en `images`:
    images.value = response.data.map((carta, idx) => ({
      ...carta,
      // Asegúrate de que existan: "id", "index", "src" o "img_identifier", etc.
      // Si tu backend devuelve "img_identifier" en vez de "src", cambia la propiedad
      // o adáptalo para tu <img :src="...">
      // Ejemplo:
      id: carta.id ?? (Date.now() + Math.random()),
      index: carta.index ?? idx,
      src: carta.img_identifier, // para poder usar 'img.src' en el template
      title: carta.title ?? 'Sin título'
    }))
  } catch (error) {
    console.error('Error al obtener cartas:', error)
  }
}

/** POST /cartas/ con { index, img_identifier } */
async function createcarta(cartaData) {
  // cartaData = { index, img_identifier }
  const response = await axios.post(`${URI}/carta/`, cartaData)
  return response.data
}

/** POST /cartas/reorder con { cartas: [ { index, img_identifier }, ... ] } */
async function reordercartas(cartasArray) {
  // cartasArray = [ { index, img_identifier }, ... ]
  const response = await axios.post(`${URI}/carta/reorder`, cartasArray )
  return response.data
}

/** DELETE /cartas/{carta_id} */
async function deletecarta(cartaId) {
  const response = await axios.delete(`${URI}/carta/${cartaId}`)
  return response.data
}

// -------------------- DRAG & DROP --------------------
function onDragStart(index) {
  draggedItemIndex.value = index
}

function onDragEnter(index) {
  dragOverIndex.value = index
}

function onDragLeave() {
  dragOverIndex.value = -1
}

async function onDrop(index) {
  if (index === draggedItemIndex.value) return

  // Hallamos el item arrastrado
  const draggedItem = sortedImages.value[draggedItemIndex.value]
  const originalIndex = images.value.findIndex((img) => img.id === draggedItem.id)

  // Lo quitamos y lo insertamos en la nueva posición
  images.value.splice(originalIndex, 1)
  images.value.splice(index, 0, draggedItem)

  // Reasignamos los índices
  images.value.forEach((img, idx) => {
    img.index = idx
  })

  // Limpiamos estados de drag
  draggedItemIndex.value = -1
  dragOverIndex.value = -1

  // Envía el nuevo orden al backend
  try {
    // Prepara el array que tu endpoint necesita
    const reorderData = images.value.map((img) => ({
      id:img.id,
      index: img.index,
      img_identifier: img.src  // Si tu backend espera "img_identifier", se lo pasamos así
    }))
    await reordercartas(reorderData)
  } catch (error) {
    console.error('Error al reordenar cartas:', error)
  }
}

// -------------------- ELIMINAR --------------------
function openDeleteDialog(img) {
  imageToDelete.value = img
  isDeleteDialogOpen.value = true
}

function closeDeleteDialog() {
  isDeleteDialogOpen.value = false
  imageToDelete.value = null
}

async function confirmDelete() {
  if (!imageToDelete.value) return
  try {
    await deletecarta(imageToDelete.value.id)

    // Removemos local
    const indexToRemove = images.value.findIndex((img) => img.id === imageToDelete.value.id)
    if (indexToRemove !== -1) {
      images.value.splice(indexToRemove, 1)
      // Reasignamos índices
      images.value.forEach((img, idx) => {
        img.index = idx
      })
    }
  } catch (error) {
    console.error('Error al eliminar carta:', error)
  }
  closeDeleteDialog()
}

// -------------------- AGREGAR NUEVOS cartaS --------------------
function openAddImageDialog() {
  isAddImageDialogOpen.value = true
}

// Dispara la selección de archivos en el input
function triggerFileSelect() {
  fileInput.value.click()
}

// Maneja los archivos seleccionados
function handleFileUpload(event) {
  const files = event.target.files
  if (!files || files.length === 0) return

  selectedFiles.value = Array.from(files)
  // Muestra preview sólo de la primera
  if (selectedFiles.value.length > 0) {
    imagePreview.value = URL.createObjectURL(selectedFiles.value[0])
  }

  // Para poder volver a seleccionar la misma imagen
  event.target.value = ''
}

async function confirmAddImages() {
  if (selectedFiles.value.length === 0) {
    alert('Por favor selecciona al menos una imagen.')
    return
  }

  uploading.value = true
  try {
    // Sube cada archivo y crea un carta en el backend
    for (const file of selectedFiles.value) {
      // 1) Subir la imagen al backend usando productService
      //    Asumiendo que `uploadPhoto` devuelve un objeto con { image_identifier: '...' }
      const formData = new FormData()
      formData.append('file', file)

      const response = await productService.uploadPhoto(formData)
      // Asegúrate de que `response.image_identifier` exista
      const { image_identifier } = response

      // 2) Crear el carta con ese identificador
      //    El backend espera cartaAppSchema: { index: number, img_identifier: string }
      const cartaData = {
        index: images.value.length,
        img_identifier: image_identifier
      }
      const created = await createcarta(cartaData)

      // 3) Agregar a la lista local
      images.value.push({
        id: created.id ?? Date.now() + Math.random(),
        index: created.index ?? images.value.length - 1,
        src: created.img_identifier, // usar 'src' local para tu <img>
        title: file.name
      })
    }

    // Limpieza de estado
    selectedFiles.value = []
    imagePreview.value = null
    isAddImageDialogOpen.value = false
  } catch (error) {
    console.error('Error al subir las imágenes o crear cartas:', error)
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

.draggable-item {
  position: relative;
  width: 100%;
  max-width: 15rem;
  border-radius: 4px;
  cursor: move;
  text-align: center;
  background-color: #fff;
  transition: background-color 0.2s ease, border-color 0.2s ease;
  margin-bottom: 1rem;
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

/* Botón de eliminar en la esquina superior derecha */
.delete-button {
  position: absolute;
  top: 8px;
  right: 8px;
}

/* Diálogo de confirmación */
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
