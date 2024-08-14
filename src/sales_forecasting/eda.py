import math

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Supongamos que tu DataFrame se llama df
df = pd.read_csv("src/sales_forecasting/data/processed_data.csv")

# 1. Información general del DataFrame
print("Información general del DataFrame:")
print(df.info())

# 2. Resumen estadístico de las columnas numéricas
print("\nResumen estadístico de las columnas numéricas:")
print(df.describe())

# 3. Visualización de valores nulos
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.title("Mapa de calor de valores nulos")
plt.show()

# 4. Distribución de cada variable numérica
df.hist(figsize=(14, 10), bins=30, edgecolor="black")
plt.suptitle("Distribución de variables numéricas", fontsize=16)
plt.show()

# 5. Boxplot para detectar outliers en las columnas numéricas
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
n_cols = len(numeric_cols)
n_rows = math.ceil(
    n_cols / 3
)  # Ajuste dinámico de las filas según el número de columnas

fig, axes = plt.subplots(n_rows, 3, figsize=(16, 4 * n_rows))
fig.suptitle("Boxplots de variables numéricas", fontsize=16)

for i, col in enumerate(numeric_cols):
    row = i // 3
    col_pos = i % 3
    sns.boxplot(data=df, y=col, ax=axes[row, col_pos])

# Ajuste para el caso de menos gráficos que el espacio disponible
for j in range(i + 1, n_rows * 3):
    fig.delaxes(axes.flatten()[j])

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# 6. Análisis de correlación entre variables numéricas
numeric_df = df.select_dtypes(
    include=["float64", "int64"]
)  # Seleccionar solo columnas numéricas
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Matriz de correlación")
plt.show()

# 7. Análisis de variables categóricas (si tienes alguna)
# Cambia 'columna_categorica' por el nombre de la columna categórica si la tienes
# sns.countplot(x='columna_categorica', data=df)
# plt.title("Distribución de la columna categórica")
# plt.show()

# 8. Series temporales (si una de tus columnas es temporal)
# Asegúrate de que la columna de fecha esté en formato datetime
if "Fecha" in df.columns:
    plt.figure(figsize=(10, 6))
    df.groupby("Fecha")["Cantidad"].sum().plot()
    plt.title("Ventas por Fecha")
    plt.ylabel("Metros Vendidos")
    plt.show()

# 9. Análisis de la relación entre variables

# Selección de columnas numéricas específicas
selected_cols = numeric_df.columns[
    :3
]  # Limitar a las primeras 3 columnas numéricas (ajusta según sea necesario)

# Muestreo de los datos para pairplot
sampled_df = numeric_df[selected_cols].sample(
    n=300, random_state=42
)  # Muestreo de 300 filas

# Desactivar histogramas y cambiar a gráficos de densidad (kde)
sns.pairplot(sampled_df, kind="kde")
plt.suptitle("Pairplot de una muestra de datos (KDE)", y=1.02)
plt.show()

#### TOP 10 MATERIALES ####

# Asegúrate de que la columna Fecha esté en formato datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Convertir la columna 'Cantidad' a numérico, forzando errores a NaN (en caso de que haya datos no numéricos)
df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")

# Verifica si hay valores nulos después de la conversión
print(f"Valores nulos después de la conversión: \n{df['Cantidad'].isnull().sum()}")

# Crear columnas de mes y año
df["Mes"] = df["Fecha"].dt.month
df["Año"] = df["Fecha"].dt.year

# Agrupar por material para calcular las ventas totales por material
ventas_por_material = df.groupby("MATERIAL")["Cantidad"].sum().reset_index()

# Ordenar para obtener los 10 materiales más vendidos
top_10_materiales = ventas_por_material.sort_values(
    by="Cantidad", ascending=False
).head(10)

# Filtrar el DataFrame original para solo incluir los materiales del top 10
df_top_10 = df[df["MATERIAL"].isin(top_10_materiales["MATERIAL"])]

# Agrupar por material, año y mes para calcular las ventas mensuales y anuales
ventas_mensuales = (
    df_top_10.groupby(["MATERIAL", "Año", "Mes"])["Cantidad"].sum().reset_index()
)

# Pivotar la tabla para una mejor visualización
ventas_mensuales_pivot = ventas_mensuales.pivot_table(
    index=["MATERIAL", "Año"], columns="Mes", values="Cantidad", fill_value=0
)

# Mostrar el DataFrame resultante
print(ventas_mensuales_pivot)

# Visualización de las ventas por mes y año para el top 10 de materiales
plt.figure(figsize=(14, 8))
for material in top_10_materiales["MATERIAL"]:
    df_plot = ventas_mensuales[ventas_mensuales["MATERIAL"] == material]
    plt.plot(df_plot["Mes"], df_plot["Cantidad"], marker="o", label=material)

plt.title("Ventas Mensuales del Top 10 de Materiales")
plt.xlabel("Mes")
plt.ylabel("Cantidad Vendida")
plt.legend(title="Materiales")
plt.grid(True)
plt.show()
