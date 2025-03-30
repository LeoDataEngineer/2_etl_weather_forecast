import os
import pandas as pd
from sqlalchemy import create_engine, text
from config import USER, PASSWORD, HOST, PORT, DATABASE

USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
DATABASE = os.environ['DATABASE']

# Crear la conexión con SQLAlchemy
engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# Definir carpeta de origen
carpeta_origen = "modelo_datos"

# Cargar DataFrames
ruta_DimCondicion = os.path.join(carpeta_origen, "DimCondicion.csv")
df_DimCondicion = pd.read_csv(ruta_DimCondicion)

ruta_DimFecha = os.path.join(carpeta_origen, "DimFecha.csv")
df_DimFecha = pd.read_csv(ruta_DimFecha)

ruta_DimHora = os.path.join(carpeta_origen, "DimHora.csv")
df_DimHora = pd.read_csv(ruta_DimHora)

ruta_DimUbicacion = os.path.join(carpeta_origen, "DimUbicacion.csv")
df_DimUbicacion = pd.read_csv(ruta_DimUbicacion)

ruta_FactPronostico = os.path.join(carpeta_origen, "FactPronostico.csv")
df_FactPronostico = pd.read_csv(ruta_FactPronostico)


# Conectar a la base de datos
with engine.connect() as connection:
    # 1️⃣ Deshabilitar las restricciones de clave foránea
    connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

    # 2️⃣ Vaciar las tablas sin eliminar su estructura
    connection.execute(text("TRUNCATE TABLE DimCondicion;"))
    connection.execute(text("TRUNCATE TABLE DimFecha;"))
    connection.execute(text("TRUNCATE TABLE DimHora;"))
    connection.execute(text("TRUNCATE TABLE DimUbicacion;"))
    connection.execute(text("TRUNCATE TABLE FactPronostico;"))

    # 3️⃣ Insertar los datos en la tablas
    df_DimCondicion.to_sql(name="DimCondicion", con=engine, if_exists="append", index=False)
    df_DimFecha.to_sql(name="DimFecha", con=engine, if_exists="append", index=False)
    df_DimHora.to_sql(name="DimHora", con=engine, if_exists="append", index=False)
    df_DimUbicacion.to_sql(name="DimUbicacion", con=engine, if_exists="append", index=False)
    df_FactPronostico.to_sql(name="FactPronostico", con=engine, if_exists="append", index=False)

    # 5️⃣ Volver a habilitar las restricciones de clave foránea
    connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

print("Datos enviados correctamente en MySQL")