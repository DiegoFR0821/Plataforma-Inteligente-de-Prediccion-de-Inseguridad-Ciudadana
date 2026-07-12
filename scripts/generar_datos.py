import pandas as pd
import numpy as np
import random

# =====================================
# CONFIGURACIÓN
# =====================================

TOTAL_REGISTROS = 5000

COLUMNAS = [
    "Fecha_Reporte",
    "Hora_Reporte",
    "Distrito",
    "Tipo_Delito",
    "Latitud",
    "Longitud",
    "Tiempo_Respuesta_Min",
    "Uso_Arma",
    "Captura",
    "Rango_Horario"
]

# =====================================
# LEER CSV ORIGINAL
# =====================================

df = pd.read_csv(
    "data/V_Staging_1000.csv",
    sep=";",
    header=None,
    names=COLUMNAS,
    dtype=str
)

# Convertir tipos
df["Latitud"] = df["Latitud"].astype(float)
df["Longitud"] = df["Longitud"].astype(float)
df["Tiempo_Respuesta_Min"] = df["Tiempo_Respuesta_Min"].astype(float)

# =====================================
# CREAR NUEVOS REGISTROS
# =====================================

while len(df) < TOTAL_REGISTROS:

    fila = df.sample(1).iloc[0].copy()

    # Fecha
    fecha = pd.to_datetime(fila["Fecha_Reporte"])
    fecha += pd.Timedelta(days=random.randint(-120,120))
    fila["Fecha_Reporte"] = fecha.strftime("%Y-%m-%d")

    # Hora
    h = random.randint(0,23)
    m = random.randint(0,59)
    s = random.randint(0,59)

    fila["Hora_Reporte"] = f"{h:02}:{m:02}:{s:02}.0000000"

    # Coordenadas
    fila["Latitud"] = round(fila["Latitud"] + np.random.normal(0,0.002),4)
    fila["Longitud"] = round(fila["Longitud"] + np.random.normal(0,0.002),4)

    # Tiempo
    tiempo = fila["Tiempo_Respuesta_Min"] + np.random.normal(0,2)

    if tiempo < 2:
        tiempo = 2

    fila["Tiempo_Respuesta_Min"] = round(tiempo,1)

    # TRUE/FALSE
    if random.random() < 0.10:
        fila["Uso_Arma"] = "TRUE" if fila["Uso_Arma"]=="FALSE" else "FALSE"

    if random.random() < 0.10:
        fila["Captura"] = "TRUE" if fila["Captura"]=="FALSE" else "FALSE"

    df.loc[len(df)] = fila

# =====================================
# EXPORTAR
# =====================================

df.to_csv(
    "data/V_Staging_5000.csv",
    sep=";",
    header=False,
    index=False
)

print("="*50)
print("CSV GENERADO")
print("="*50)
print(df.shape)