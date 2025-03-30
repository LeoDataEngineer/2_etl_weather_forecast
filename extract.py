import requests
import json
import os
# from config import *

# Credenciales API guardadas en github en sus variables de entorno
API_KEY_WAPI = os.environ['API_KEY_WAPI']


def get_data(ciudad, api_key, dias=3, carpeta_destino="raw"):
    """
    Obtiene el pronóstico del clima para una ciudad específica y lo guarda en un archivo JSON en la carpeta especificada.
    
    Parámetros:
    ciudad (str): Nombre de la ciudad a consultar.
    api_key (str): Clave de la API de WeatherAPI.
    dias (int): Número de días de pronóstico (por defecto 3).
    carpeta_destino (str): Carpeta donde se guardará el archivo JSON (por defecto "raw").
    
    Retorna:
    dict: Datos del pronóstico en formato JSON.
    """
    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    url_clima = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={ciudad}&days={dias}&aqi=no&alerts=no'
    response = requests.get(url_clima)
    
    if response.status_code == 200:
        datos_clima = response.json()
        nombre_archivo = os.path.join(carpeta_destino, f"{ciudad}_clima.json")
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_clima, archivo, indent=4, ensure_ascii=False)
        return datos_clima
    else:
        return {"error": f"No se pudo obtener el pronóstico. Código de estado: {response.status_code}"}
    
    
# Lista de capitales de América Latina
capitales_latinoamerica = [
    "Buenos Aires", "La Paz", "Brasilia", "Santiago", "Bogota", "Quito", "Asuncion",
    "Lima", "Montevideo", "Caracas", "Mexico city", "San Salvador", "Tegucigalpa",
    "Managua", "san jose, costa rica", "Panama city", "Guatemala City", "Santo Domingo",
    "Habana", "Port-au-Prince"
]

# Obtener el pronóstico para cada capital
for capital in capitales_latinoamerica:
    print(f"Obteniendo pronóstico para {capital}...")
    resultado = get_data(capital, API_KEY_WAPI, 3)
    if "error" in resultado:
        print(resultado["error"])
    else:
        print(f"Pronóstico de {capital} guardado correctamente.") 