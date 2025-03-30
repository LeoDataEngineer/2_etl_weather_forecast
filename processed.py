import os
import json
import pandas as pd

# Carpeta donde están los JSON crudos
carpeta_raw = "raw"
# Carpeta de salida para los CSV procesados
carpeta_processed = "processed"

# Crear la carpeta si no existe
if not os.path.exists(carpeta_processed):
    os.makedirs(carpeta_processed)

# Función para extraer los datos del pronóstico
def get_forecast(response, i, j):
    fecha = response['forecast']['forecastday'][j]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][j]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][j]['hour'][i]['condition']['text']
    tempe = float(response['forecast']['forecastday'][j]['hour'][i]['temp_c'])
    humedad = float(response['forecast']['forecastday'][j]['hour'][i]['humidity'])
    rain = response['forecast']['forecastday'][j]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][j]['hour'][i]['chance_of_rain']
    name_city = response['location']['name']
    name_region = response['location']['region']
    name_country = response['location']['country']
    lat = response['location']['lat']
    lon = response['location']['lon']
    localtime = response['location']['localtime']
    
    
    
    return fecha, hora, condicion, tempe, rain, prob_rain, humedad, name_city, name_region, name_country, lat, lon, localtime

# Procesar cada archivo JSON en la carpeta "raw"
for archivo in os.listdir(carpeta_raw):
    if archivo.endswith("_clima.json"):
        ruta_json = os.path.join(carpeta_raw, archivo)

        with open(ruta_json, "r", encoding="utf-8") as f:
            response = json.load(f)

        datos = []
        for j in range(3):  # Iterar sobre los días del pronóstico
            for i in range(len(response['forecast']['forecastday'][0]['hour'])):  # Iterar sobre las horas
                datos.append(get_forecast(response, i, j))

        col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'Prob_lluvia','Humedad', 'Ciudad', 'Region', 'Pais', 'Latitud', 'Longitud', 'Fecha_Hora_local']
        df = pd.DataFrame(datos, columns=col)
        df = df.sort_values(by='Hora', ascending=True)
        
        # Guardar CSV en la carpeta "processed"
        nombre_ciudad = archivo.replace("_clima.json", "")
        ruta_csv = os.path.join(carpeta_processed, f"{nombre_ciudad}_clima_procesado.csv")
        df.to_csv(ruta_csv, index=False, encoding="utf-8")

        print(f"Procesado y guardado: {ruta_csv}")
