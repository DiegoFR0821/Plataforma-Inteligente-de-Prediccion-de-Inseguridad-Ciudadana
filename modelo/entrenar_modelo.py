import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# CARGAR CSV
# ==========================================

df = pd.read_csv(
    "data/v_staging_5000.csv",
    sep=";"
)

# ==========================================
# RENOMBRAR COLUMNAS
# ==========================================

df.columns = [
    "Fecha",
    "Hora_Reporte",
    "Distrito",
    "Tipo_Delito",
    "Latitud",
    "Longitud",
    "Tiempo_Respuesta_Min",
    "Uso de Arma",
    "Captura Realizada",
    "Rango_Horario"
]

# ==========================================
# LABEL ENCODERS
# ==========================================

encoder_distrito = LabelEncoder()
encoder_horario = LabelEncoder()
encoder_arma = LabelEncoder()
encoder_captura = LabelEncoder()
encoder_delito = LabelEncoder()

df["Distrito"] = encoder_distrito.fit_transform(df["Distrito"])

df["Rango_Horario"] = encoder_horario.fit_transform(df["Rango_Horario"])

df["Uso de Arma"] = encoder_arma.fit_transform(df["Uso de Arma"])

df["Captura Realizada"] = encoder_captura.fit_transform(
    df["Captura Realizada"]
)

df["Tipo_Delito"] = encoder_delito.fit_transform(
    df["Tipo_Delito"]
)

# ==========================================
# VARIABLES
# ==========================================

X = df[
    [
        "Distrito",
        "Rango_Horario",
        "Uso de Arma",
        "Captura Realizada"
    ]
]

y = df["Tipo_Delito"]

# ==========================================
# MODELO
# ==========================================

modelo = RandomForestClassifier(

    n_estimators=250,

    random_state=42

)

modelo.fit(X, y)

# ==========================================
# GUARDAR
# ==========================================

joblib.dump(
    modelo,
    "modelo/modelo_delito.pkl"
)

joblib.dump(
    encoder_distrito,
    "modelo/encoder_distrito.pkl"
)

joblib.dump(
    encoder_horario,
    "modelo/encoder_horario.pkl"
)

joblib.dump(
    encoder_arma,
    "modelo/encoder_arma.pkl"
)

joblib.dump(
    encoder_captura,
    "modelo/encoder_captura.pkl"
)

joblib.dump(
    encoder_delito,
    "modelo/encoder_delito.pkl"
)

print()

print("="*50)

print("MODELO ENTRENADO CORRECTAMENTE")

print("="*50)