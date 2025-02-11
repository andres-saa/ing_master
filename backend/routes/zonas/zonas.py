from fastapi import FastAPI,APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from pydantic import BaseModel
from shapely.geometry import Point, Polygon
from lxml import etree
import os
import zipfile
import io
import json
import re  # Importamos el módulo 're' para usar expresiones regulares

zona_rputer = APIRouter()

# Directorio donde se guardarán los archivos KML/KMZ y el archivo de zonas
UPLOAD_DIRECTORY = "./files/mapa"

# Ruta al archivo donde se almacenarán las zonas
ZONAS_FILE = "./files/zonas.json"

# Crear el directorio si no existe
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def extraer_valor_domicilio(nombre_zona):
    """
    Extrae el valor del domicilio del nombre de la zona.
    Por ejemplo, de "ZONA 1 - $3.500" extrae 3500.
    """
    # Expresión regular para encontrar el valor numérico en el formato $X.XXX
    match = re.search(r'\$([\d\.,]+)', nombre_zona)
    if match:
        # Eliminamos puntos y comas del valor y convertimos a entero
        valor_str = match.group(1).replace('.', '').replace(',', '')
        try:
            valor = int(valor_str)
            return valor
        except ValueError:
            return "Valor no definido"
    else:
        return "Valor no definido"

@zona_rputer.post("/upload_kml/")
async def upload_kml(file: UploadFile = File(...)):
    # Verificar la extensión del archivo
    if not (file.filename.endswith('.kml') or file.filename.endswith('.kmz')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un KML o KMZ")

    try:
        # Leer el contenido del archivo
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="El archivo está vacío")

        # Guardar el archivo en el sistema de archivos
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            f.write(content)

        # Procesar el archivo desde el sistema de archivos
        if file.filename.endswith('.kmz'):
            with zipfile.ZipFile(file_location, 'r') as kmz:
                # Buscar el archivo KML dentro del KMZ
                kml_filename = None
                for name in kmz.namelist():
                    if name.endswith('.kml'):
                        kml_filename = name
                        break
                if not kml_filename:
                    raise HTTPException(status_code=400, detail="El archivo KMZ no contiene un archivo KML")
                # Leer el contenido del archivo KML
                with kmz.open(kml_filename) as kml_file:
                    kml_content = kml_file.read()
        else:
            # Si es un archivo KML, leerlo desde el sistema de archivos
            with open(file_location, "rb") as f:
                kml_content = f.read()

        # Parsear el contenido del KML
        kml_root = etree.fromstring(kml_content)
        namespaces = {
            'kml': 'http://www.opengis.net/kml/2.2',
            'gx': 'http://www.google.com/kml/ext/2.2'
        }

        # Lista para almacenar las zonas
        zonas_list = []

        for placemark in kml_root.xpath('.//kml:Placemark', namespaces=namespaces):
            name_elem = placemark.find('kml:name', namespaces)
            name = name_elem.text.strip() if name_elem is not None else "Sin Nombre"

            # Extraer el valor del domicilio del nombre de la zona
            valor_domicilio = extraer_valor_domicilio(name)

            polygon = placemark.find('.//kml:Polygon', namespaces)
            if polygon is not None:
                outer_boundary = polygon.find('.//kml:outerBoundaryIs/kml:LinearRing/kml:coordinates', namespaces)
                if outer_boundary is None or outer_boundary.text is None:
                    continue
                coords_text = outer_boundary.text.strip()
                coords = []
                for coord in coords_text.split():
                    lon_lat = coord.strip().split(',')
                    if len(lon_lat) < 2:
                        continue
                    lon, lat = map(float, lon_lat[:2])
                    coords.append([lon, lat])
                if coords:
                    # Agregar la zona a la lista
                    zona = {
                        'nombre': name,
                        'valor_domicilio': valor_domicilio,
                        'polygon_coords': coords  # Lista de coordenadas
                    }
                    zonas_list.append(zona)

        # Guardar las zonas en el archivo JSON
        with open(ZONAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(zonas_list, f, ensure_ascii=False, indent=4)

        return {"message": "Archivo KML/KMZ procesado y guardado correctamente"}
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="El archivo KMZ está corrupto o no es un archivo ZIP válido")
    except etree.XMLSyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Error al parsear el archivo KML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

class Coordenadas(BaseModel):
    latitud: float
    longitud: float

@zona_rputer.post("/consultar_zona/")
def consultar_zona(coord: Coordenadas):
    punto = Point(coord.longitud, coord.latitud)

    # Verificar si el archivo d`e zonas existe
    if not os.path.exists(ZONAS_FILE):
        return {"message": "No hay zonas cargadas en el servidor"}

    # Cargar las zonas desde el archivo JSON
    with open(ZONAS_FILE, 'r', encoding='utf-8') as f:
        zonas_list = json.load(f)

    # Lista para almacenar las zonas que contienen el punto
    zonas_contienen_punto = []

    for zona in zonas_list:
        coords = zona['polygon_coords']
        polygon_shape = Polygon(coords)
        if polygon_shape.contains(punto):
            zonas_contienen_punto.append({
                "zona": zona['nombre'],
                "valor_domicilio": zona['valor_domicilio'],
                "area": polygon_shape.area,  # Calculamos el área de la zona
                "polygon_shape": polygon_shape
            })

    if not zonas_contienen_punto:
        return {"message": "No está en cobertura"}

    # Ordenar las zonas por área en orden ascendente para tomar la más pequeña
    zonas_contienen_punto.sort(key=lambda x: x['area'])

    # Seleccionar la zona más interna (la de menor área)
    zona_mas_interna = zonas_contienen_punto[0]

    return {
        "zona": zona_mas_interna['zona'],
        "valor_domicilio": zona_mas_interna['valor_domicilio']
    }


@zona_rputer.get("/zonas")
def get_zonas():
    if not os.path.exists(ZONAS_FILE):
        return []
    with open(ZONAS_FILE, 'r', encoding='utf-8') as f:
        zonas_list = json.load(f)
    return zonas_list


@zona_rputer.get("/get_map", response_class=FileResponse)
def get_map():
    # Busca el archivo KMZ más reciente en el directorio
    kmz_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith('.kmz')]
    if not kmz_files:
        raise HTTPException(status_code=404, detail="No hay archivos KMZ disponibles")
    
    # Selecciona el archivo más reciente
    latest_kmz = max(kmz_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_DIRECTORY, f)))
    file_path = os.path.join(UPLOAD_DIRECTORY, latest_kmz)

    return FileResponse(file_path, media_type="application/vnd.google-earth.kmz", filename=latest_kmz)