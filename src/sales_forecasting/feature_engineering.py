import pandas as pd

# Lee un dataframe de la carpeta data que se llama raw_data
df = pd.read_csv("src/sales_forecasting/data/raw_data.csv")
print(df.head())
df = df[["Fecha", "MATERIAL", "Cantidad", "VENDEDOR"]]

# Convertir la columna Fecha a datetime
df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")

# Crear columna para el día de la semana
df["Día de la Semana"] = df["Fecha"].dt.day_name()

# Crear columna para el mes
df["Mes"] = df["Fecha"].dt.month

# Crear columna para el año
df["Año"] = df["Fecha"].dt.year


# Función para obtener la estación del año
def obtener_estacion(mes):
    if mes in [12, 1, 2]:
        return "Invierno"
    elif mes in [3, 4, 5]:
        return "Primavera"
    elif mes in [6, 7, 8]:
        return "Verano"
    else:
        return "Otoño"


# Agregar la columna de estación del año
df["Estación"] = df["Mes"].apply(obtener_estacion)

# Ventas acumuladas por día y material
df["Ventas Diarias"] = df.groupby(["Fecha", "MATERIAL"])["Cantidad"].transform("sum")

# # Crear características de rezago (lag)
df["Lag_1"] = df.groupby("MATERIAL")["Ventas Diarias"].shift(1)
df["Lag_2"] = df.groupby("MATERIAL")["Ventas Diarias"].shift(2)
df["Lag_3"] = df.groupby("MATERIAL")["Ventas Diarias"].shift(3)

# Eliminar filas con valores nulos creados por el rezago
df.dropna(inplace=True)

# Mostrar el dataframe resultante
df.reset_index(drop=True, inplace=True)

# Conversión de las columnas a tipo numérico, forzando errores a NaN
df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")
df["Ventas Diarias"] = pd.to_numeric(df["Ventas Diarias"], errors="coerce")
df["Lag_1"] = pd.to_numeric(df["Lag_1"], errors="coerce")
df["Lag_2"] = pd.to_numeric(df["Lag_2"], errors="coerce")
df["Lag_3"] = pd.to_numeric(df["Lag_3"], errors="coerce")

# Verificación de valores nulos después de la conversión
print("Valores nulos después de la conversión:")
print(df[["Cantidad", "Ventas Diarias", "Lag_1", "Lag_2", "Lag_3"]].isnull().sum())

# Opcional: Eliminar filas con valores nulos si es necesario
# df.dropna(subset=['Cantidad', 'Ventas Diarias', 'Lag_1', 'Lag_2', 'Lag_3'], inplace=True)

# Información actualizada del DataFrame
print("\nInformación actualizada del DataFrame:")
print(df.info())

df.to_csv("src/sales_forecasting/data/processed_data.csv", index=False)
