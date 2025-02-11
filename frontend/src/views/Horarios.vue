<template>
              <h4 class="title">Horarios Master</h4>


              <div>
                <div style="max-width: 500px;padding:.5rem; margin:auto">
                <DataTable 
        style="box-shadow: 0 0 1rem #00000030;"
      :value="horario"
      dataKey="id"
      :rows="7"
      :rowsPerPageOptions="[5, 10, 25, 100]"
      currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} horarios"
      responsiveLayout="scroll"

    >
      <!-- Día -->
      <Column field="day_of_week" header="Día" headerStyle="width:2rem;">
        <template #body="slotProps">
          {{ dias[slotProps.data.day_of_week - 1] }}
        </template>
      </Column>
  
      <!-- Apertura -->
      <Column field="opening_time" header="Apertura" headerStyle="width:2rem;">
        <template #body="slotProps">
          {{ formatearHora(slotProps.data.opening_time) }}
        </template>
      </Column>
  
      <!-- Cierre -->
      <Column field="closing_time" header="Cierre" headerStyle="width:5rem;">
        <template #body="slotProps">
          {{ formatearHora(slotProps.data.closing_time) }}
        </template>
      </Column>
    </DataTable>
            </div>


            <h4 class="title">Talvez te pueda interesar</h4>


              </div>
     
<grid-categorias></grid-categorias>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import CategoryView from './CategoryView.vue'
  // PrimeVue components
  import DataTable from 'primevue/datatable'
  import Column from 'primevue/column'
  import gridCategorias from '@/components/gridCategorias.vue'
  
  // Your API URI
  import { URI } from '@/service/conection'
  
  // Reactive references
  const horario = ref([])
  const dias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
  
  // Utility to format time from a Date object into 12-hour format
  function formatearHora(fecha) {
    if (!(fecha instanceof Date)) return fecha
  
    let hora = fecha.getHours()
    let minutos = fecha.getMinutes()
  
    const ampm = hora >= 12 ? 'PM' : 'AM'
    hora = hora % 12
    hora = hora ? hora : 12 // if hour is 0, convert to 12
  
    return hora + ':' + minutos.toString().padStart(2, '0') + ' ' + ampm
  }
  
  // Fetch horario data on mount
  onMounted(async () => {
    await getHorarios()
  })
  
  async function getHorarios() {
    try {
      const response = await fetch(`${URI}/site-schedule/31/`)
      if (!response.ok) {
        throw new Error('Error al obtener los datos')
      }
      const data = await response.json()
  
      // Convert string times to Date objects
      data.forEach(item => {
        item.opening_time = new Date(`1970-01-01T${item.opening_time}`)
        item.closing_time = new Date(`1970-01-01T${item.closing_time}`)
      })
  
      horario.value = data
    } catch (error) {
      console.error(error)
    }
  }
  </script>
  
  <style scoped>
  /* Add your styling here if needed */




.title {
    margin: 0;
    padding: 0;
    font-family:roboto;
    font-weight: bold;
    letter-spacing: .1cap;
    width: 100%;
    text-align: center;
    margin: 4rem 0;
    font-size: 2rem;
    color: var(--primary-color);
    transition: all ease .3s;
}
  </style>
  