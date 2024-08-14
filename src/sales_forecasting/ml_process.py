import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Supongamos que tu DataFrame se llama df
df = pd.read_csv("src/sales_forecasting/data/processed_data.csv")

# 1. Manejar valores nulos en la variable objetivo y en las características

# Eliminar filas donde 'Cantidad' es NaN
df = df.dropna(subset=["Cantidad"])

# Imputar valores nulos en las columnas numéricas con la mediana
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Para columnas categóricas, llenamos NaNs con un valor específico
categorical_cols = df.select_dtypes(include=["object"]).columns
df[categorical_cols] = df[categorical_cols].fillna("desconocido")

# 2. Selección de características y variable objetivo
features_with_lags = df.drop(columns=["Cantidad", "Fecha"])  # Incluye los rezagos
features_without_lags = df.drop(
    columns=["Cantidad", "Fecha", "Lag_1", "Lag_2", "Lag_3"]
)  # Excluye los rezagos

# Codificación de variables categóricas
features_with_lags = pd.get_dummies(features_with_lags, drop_first=True)
features_without_lags = pd.get_dummies(features_without_lags, drop_first=True)

# Variable objetivo
target = df["Cantidad"]

# 3. División de datos en entrenamiento y prueba
X_train_lags, X_test_lags, y_train, y_test = train_test_split(
    features_with_lags, target, test_size=0.2, random_state=42
)
X_train_no_lags, X_test_no_lags = train_test_split(
    features_without_lags, test_size=0.2, random_state=42
)[0:2]

# 4. Entrenamiento del modelo Random Forest (con rezagos)
model_lags = RandomForestRegressor(n_estimators=100, random_state=42)
model_lags.fit(X_train_lags, y_train)

# 5. Predicción y evaluación del modelo (con rezagos)
y_pred_lags = model_lags.predict(X_test_lags)

# Métricas para el modelo con rezagos
mae_lags = mean_absolute_error(y_test, y_pred_lags)
rmse_lags = np.sqrt(mean_squared_error(y_test, y_pred_lags))
r2_lags = r2_score(y_test, y_pred_lags)

print(f"Modelo con rezagos - MAE: {mae_lags}")
print(f"Modelo con rezagos - RMSE: {rmse_lags}")
print(f"Modelo con rezagos - R²: {r2_lags}")

# 6. Entrenamiento del modelo Random Forest (sin rezagos)
model_no_lags = RandomForestRegressor(n_estimators=100, random_state=42)
model_no_lags.fit(X_train_no_lags, y_train)

# 7. Predicción y evaluación del modelo (sin rezagos)
y_pred_no_lags = model_no_lags.predict(X_test_no_lags)

# Métricas para el modelo sin rezagos
mae_no_lags = mean_absolute_error(y_test, y_pred_no_lags)
rmse_no_lags = np.sqrt(mean_squared_error(y_test, y_pred_no_lags))
r2_no_lags = r2_score(y_test, y_pred_no_lags)

print(f"Modelo sin rezagos - MAE: {mae_no_lags}")
print(f"Modelo sin rezagos - RMSE: {rmse_no_lags}")
print(f"Modelo sin rezagos - R²: {r2_no_lags}")
