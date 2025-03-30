import os
import pandas as pd

# Carpeta donde están los csv 
carpeta_raw = "processed"
# Carpeta de salida para los CSV procesados
carpeta_processed = "modelo_datos"

# Crear la carpeta si no existe
if not os.path.exists(carpeta_processed):
    os.makedirs(carpeta_processed)
    
# Leer todos los archivos CSV en la carpeta
archivos_csv = [os.path.join(carpeta_raw, archivo) for archivo in os.listdir(carpeta_raw) if archivo.endswith('.csv')]

# Concatenar todos los CSVs en un solo DataFrame
df_concat = pd.concat([pd.read_csv(archivo) for archivo in archivos_csv], ignore_index=True)

# Reemplazar nombres de ciudades en el DataFrame
df_concat['Ciudad'] = df_concat['Ciudad'].replace({
    'Habana Libre': 'La Habana',
    'Mexico City': 'Ciudad de México',
    'Panama City': 'Ciudad de Panamá',
    'Guatemala City': 'Ciudad de Guatemala'
   
})

# Eliminar espacios en blanco al final de la columna 'Condicion'
df_concat["Condicion"] = df_concat["Condicion"].str.rstrip()

# Diccionario de traducción
df_concat['Condicion'] = df_concat['Condicion'].replace({
     "Partly Cloudy": "Parcialmente nublado",
    "Clear": "Despejado",
    "Patchy rain nearby": "Lluvia irregular cercana",
    "Sunny": "Soleado",
    "Thundery outbreaks in nearby": "Tormentas eléctricas cercanas",
    "Light rain shower": "Lluvia ligera",
    "Heavy rain at times": "Lluvia fuerte intermitente",
    "Heavy rain": "Lluvia fuerte",
    "Moderate or heavy rain shower": "Chubasco moderado o fuerte",
    "Overcast": "Nublado",
    "Patchy light drizzle": "Llovizna ligera irregular",
    "Light drizzle": "Llovizna ligera",
    "Light rain": "Lluvia ligera",
    "Patchy light rain": "Lluvia ligera irregular",
    "Mist": "Neblina",
    "Partly cloudy": "Parcialmente nublado",
    "Cloudy": "Nublado",
    "Fog": "Niebla",
    "Moderate rain at times": "Lluvia moderada intermitente",
    "Patchy light rain in area with thunder": "Lluvia ligera con tormenta",
    "Torrential rain shower": "Lluvia torrencial",
    "Moderate rain": "Lluvia moderada"
   
})




###################### crear el modelo dimensional y de hecho(Dim y Fact) #######################

# Crear DimUbicacion
df_ubicacion = df_concat[['Ciudad', 'Region', 'Pais', 'Latitud', 'Longitud', 'Fecha_Hora_local']].drop_duplicates().reset_index(drop=True)   
# Crear ID_Ubicacion único para cada ubicación
df_ubicacion['ID_Ubicacion'] = df_ubicacion.index + 1
# guardar el df en csv en la carpta modelo_datos
df_ubicacion.to_csv(os.path.join(carpeta_processed, 'DimUbicacion.csv'), index=False, encoding='utf-8')


# Crear DimCondicion
df_condicion = df_concat[['Condicion']].drop_duplicates().reset_index(drop=True)
# Crear ID_Condicion único para cada condición  
df_condicion['ID_Condicion'] = df_condicion.index + 1
# guardar el df en csv en la carpta modelo_datos
df_condicion.to_csv(os.path.join(carpeta_processed, 'DimCondicion.csv'), index=False, encoding='utf-8')


# Crear DimFecha   
df_fecha = df_concat[['Fecha']].drop_duplicates().reset_index(drop=True)
# Crear ID_Tiempo único para cada tiempo
df_fecha['ID_Fecha'] = df_fecha.index + 1
# guardar el df en csv en la carpta modelo_datos
df_fecha.to_csv(os.path.join(carpeta_processed, 'DimFecha.csv'), index=False, encoding='utf-8')

# Crear DimHora
df_hora = df_concat[['Hora']].drop_duplicates().reset_index(drop=True)  
# Crear ID_Hora único para cada hora
df_hora['ID_Hora'] = df_hora.index + 1
# guardar el df en csv en la carpta modelo_datos
df_hora.to_csv(os.path.join(carpeta_processed, 'DimHora.csv'), index=False, encoding='utf-8')



# Unir tablas Dimensionales con la tabla de hechos
df_concat = df_concat.merge(df_ubicacion[['Ciudad', 'Region', 'Pais', 'ID_Ubicacion']], on=['Ciudad', 'Region', 'Pais'], how='left')
df_concat = df_concat.merge(df_fecha[['Fecha', 'ID_Fecha']], on='Fecha', how='left')
df_concat = df_concat.merge(df_hora[['Hora', 'ID_Hora']], on='Hora', how='left')
df_concat = df_concat.merge(df_condicion[['Condicion', 'ID_Condicion']], on='Condicion', how='left')


# Selección de las columnas finales para FactPronostico
df_fact_pronostico = df_concat[['ID_Ubicacion', 'ID_Fecha', 'ID_Hora', 'ID_Condicion', 'Temperatura', 'Humedad', 'Lluvia', 'Prob_lluvia']]
# guardar el df en csv en la carpta modelo_datos
df_fact_pronostico.to_csv(os.path.join(carpeta_processed, 'FactPronostico.csv'), index=False, encoding='utf-8')

print("Modelo de datos creado y guardado en la carpeta modelo_datos")

