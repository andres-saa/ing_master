

import { FilterMatchMode } from 'primevue/api';
import { ref, onMounted, onBeforeMount } from 'vue';
// import ProductService from '@/service/ProductService';
import { useToast } from 'primevue/usetoast';
import { URI } from './conection';
// import { roles } from './roles';

const sitesDropValues = ref([{}])
const curentSite = ref([])
const curentSiteDocuments = ref([])



const GenderDropValues = ref([
    'Masculino', 
    'Femenino', 
]);

const epsDropValues = ref([
    "COOSALUD EPS-S",
    "NUEVA EPS", 
    "MUTUAL SER",
    "ALIANSALUD EPS",
    "SALUD TOTAL EPS S.A.", 
    "EPS SANITAS", 
    "EPS SURA", 
    "FAMISANAR EPS", 
    "SERVICIO OCCIDENTAL DE SALUD EPS (SOS EPS)",
    "SALUD MIA EPS",
    "COMFENALCO VALLE EPS",
    "COMPENSAR EPS", 
    "EPM - EMPRESAS PUBLICAS DE MEDELLIN",
    "FONDO DE PASIVO SOCIAL DE FERROCARRILES NACIONALES DE COLOMBIA",
    "CAJACOPI ATLANTICO",
    "CAPRESOCA EPS", 
    "COMFACHOCO", 
    "COMFAORIENTE",
    "EPS FAMILIAR DE COLOMBIA",
    "ASMET SALUD",
    "EMSSANAR E.S.S.",
    "CAPITAL SALUD EPS-S",
    "SAVIA SALUD EPS",
    "DUSAKAWI EPSI",
    "ASOCIACION INDIGENA DEL CAUCA EPSI",
    "ANAS WAYUU EPSI",
    "MALLAMAS EPSI",
    "PIJAOS SALUD EPSI",
    "SALUD BÓLIVAR EPS SAS",
])


const maritalStatusDropValues = ref([
    "Soltero/a",
    "Casado/a",
    "Divorciado/a",
    "Union libre",
])

const educationLevelDropValues = ref([
    "Primaria",
    "Secundaria",
    "Técnico/tecnológico",
    "Universitario/a",
    "Posgrado",
])

const employmentContractTypeDropValues = ref([
    "Fijo 3 meses",
    "Turneros", 
    "Indefinido",
])


const housingTypesDropValues = ref([
    "Propia", 
    "Arrendada", 
    "Familiar", 
    "Otra",
  ]);

  const shirtSizesDropValues = ref([
    "XS", 
    "S",
    "M",
    "L",
    "XL", 
    "XXL",
  ]);
  
  const pantSizesDropValues = ref([
    "28", 
    "30", 
    "32", 
    "34", 
    "36", 
    "38", 
    "40", 
    "42",
  ]);

  const vehicleTypesDropValues = ref([
    "Carro",
    "Moto",
    // { name: "Camión", code: "TRUCK" },
    // { name: "Bicicleta", code: "BICYCLE" },
    // { name: "Otros", code: "OTHER" }
  ]);
  
// const PositionDropValues = ref([
//      'Coordinador de Sedes Cali',
//      'Coordinador de Sede Bogotá',
//      'Líder de Punto',
//      'Cajero',
//      'Cocinero',
//      'Mesero',
//      'Auxiliar de Cocina',
//      'Jefe de Cocina', 
//      'Domiciliario', 
//      'Gerencia General', 
//      'Jefe de Gestión Humana',
//      'gestion humana',
//      'SAAMOVAR',
//      'AUXILIAR CONTABLE',
//      'DIGITADORA',
//      'AUXILIAR DE LOGISTICA',
//      'AUXILIAR DE TESORERIA',
//      'TESORERO',
//      'PATINADOR',
//      'cajero dia',
//      'AUXILIAR DE PRODUCCION',
//      'Aprendiz SENA',
//      'Jefe de Producción',
//      'Líder de Producción', 
//      'Auxiliar de Producción', 
//      'Contadora', 
//      'Auxiliar de Contabilidad',
//      'Coordinador de Inventarios',
//      'Auxiliar de Logística',
//      'Conductor',
//      'JEFE DE PRODUCCION',
//      'FRITADOR',
//      ' LIDER DE CAJA',
//      'SUBGERENTE',
//      'LIDER DE PUNTO',
//      'CAJERO NOCHE',
//      'Jefe de Compras',
//      'Auxiliar de Compras',
//      'Gerente de Marketing',
//      'Diseñador',
//      'Community Manager',
//      'administrador',
     
// ]);



// const PositionDropValues = ref(

//   roles.todos 
// );


const getSites = async () => {
  try {
    const response = await fetch(`${URI}/sites`);
    if (response.ok) {
      const data = await response.json();
      sitesDropValues.value = data;
      return data;
    } else {
      console.error('Error al obtener los datos de la API');
      return []; // Devuelve un array vacío en caso de error
    }
  } catch (error) {
    console.error('Error al obtener los datos de la API', error);
    return []; // Devuelve un array vacío en caso de error
  }
};


  const getSite = async (id)=> {
    try {
    const response = await fetch(`${URI}/site/${id}`)
    if (response.ok) {
        const data = await response.json();
        curentSite.value = data[0]
        return data
    } else {
        console.error('Error al obtener los datos de la API');
    }
    } catch (error) {
    console.error('Error al obtener los datos de la API', error);
    }
};


const bloodTypesDropValues = ref([
    "A+", 
    "A-", 
    "B+", 
    "B-", 
    "AB+", 
    "AB-", 
    "O+", 
    "O-", 
  ]) 

  const statusDropValues = ref([
    'activo',
    'inactivo',
    'Por remplazar'
]);


const pensionFundDropValues = [
    "Porvenir",
    "Proteccion",
    "Colfondos",
    "Skandia",
    "OldMutual",
    "Horizonte",
    "AFPSantander",
    "PorvenirPensionesCesantias",
    "Colpensiones",
    "ProteccionSA",
    "AFPHorizonteSA",
    "AFPCrecerSA"
];


const findByName = (toFindName,where) => {
    return where.value.find(item => item.name == toFindName);
}


function findSiteById(id) {
    return sitesDropValues.value.find(item => item.site_id == id);
}


const  findSiteByName = async(name)=> {
  await getSites().then (data => {
    // console.log(data)
    // console.log(data.find(item => item.site_name?.includes(name)).site_id)
    return data.find(item => item.site_name?.includes(name).site_id) || 12;
  
  })
 
}

function findByType(type,where) {
    return where.value.find(item => item.type == type);
}


// function findPositionByName(nameToFind) {
//     return PositionDropValues.value.find(item => item.name == nameToFind);
// }




const getSiteDocument = async (document_id, file_name) => {
  try {
    // Construye la URL con los parámetros
    const url = `${URI}/get-document-file/${document_id}/${file_name}/`;

    // Realiza la solicitud GET
    const response = await fetch(url);
    if (response.ok) {
      // Crea un objeto Blob a partir de los datos de la respuesta
      const fileBlob = await response.blob();

      // Crea una URL del objeto Blob
      const fileUrl = URL.createObjectURL(fileBlob);

      // Genera un nombre de archivo para la descarga, sin reutilizar `filename`
      const downloadFileName = `${document_id}-${file_name}.${fileBlob.type.split('/')[1] || 'bin'}`;

      // Crea un enlace temporal para descargar el archivo
      const downloadLink = document.createElement('a');
      downloadLink.href = fileUrl;
      downloadLink.download = downloadFileName; // Asigna el nombre de archivo corregido
      document.body.appendChild(downloadLink); // Necesario para que Firefox soporte el click en el enlace
      downloadLink.click(); // Simula un click en el enlace para iniciar la descarga
      document.body.removeChild(downloadLink); // Limpia agregando y luego eliminando el enlace
    } else {
      // Si la respuesta no es exitosa, maneja el error
      console.error('Error en la solicitud:', response.status, response.statusText);
    }
  } catch (error) {
    console.error('Error al enviar la solicitud:', error);
  }
};




const getSiteDocumentInfo = async (site_id) => {
  try {
    // Construye la URL con los parámetros
    const url = `${URI}/get-site-documents-info/${site_id}`;

    // Realiza la solicitud GET
    const response = await fetch(url);
    console.log(response)
    if (response.ok) {
      const data = await response.json();
      curentSiteDocuments.value = data
      }

  } catch (error) {
    console.error('Error al enviar la solicitud:', error);
  }
};


// Llama a la función para obtener y abrir el PDF
// getSiteDocument("imperio modelia", "bomberos");

export {
    sitesDropValues,
    getSites,
    GenderDropValues,
    // PositionDropValues,
    maritalStatusDropValues ,
    epsDropValues,
    educationLevelDropValues ,
    employmentContractTypeDropValues ,
    pantSizesDropValues ,
    shirtSizesDropValues ,
    bloodTypesDropValues ,
    housingTypesDropValues ,
    statusDropValues,
    vehicleTypesDropValues,
    findByName,
    findSiteById ,
    findByType,
    pensionFundDropValues,
    curentSite,
    getSite,
    getSiteDocument,
    curentSiteDocuments,
    getSiteDocumentInfo,
    findSiteByName

  }