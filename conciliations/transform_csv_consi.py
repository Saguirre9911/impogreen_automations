import os

import pandas as pd

# Directory containing the CSV file
directory = "data/"

# Find the CSV file in the directory
for file_name in os.listdir(directory):
    if file_name.endswith(".csv"):
        csv_file_path = os.path.join(directory, file_name)
        break

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)


# Select only the columns 3, 5, and 7 (zero-indexed: columns 2, 4, and 6)
selected_columns = df.iloc[:, [3, 5, 7]]


# Convertir las columnas en la primera fila
selected_columns.loc[-1] = (
    selected_columns.columns
)  # Agregar las columnas como primera fila
selected_columns.index = selected_columns.index + 1  # Desplazar el índice
selected_columns = selected_columns.sort_index()  # Reordenar el índice
# Rename the columns
selected_columns.columns = ["fecha", "valor", "descripcion"]
print(selected_columns)
# Copiar el valor de la segunda fila en la columna "fecha" a la primera fila
selected_columns.iloc[0, 0] = selected_columns.iloc[1, 0]
# Convert the first column to date format DD/MM/YYYY
selected_columns.iloc[:, 0] = pd.to_datetime(
    selected_columns.iloc[:, 0], format="%Y%m%d", errors="coerce"
).dt.strftime("%d/%m/%Y")

# Save the selected columns to an Excel file
excel_file_path = os.path.join(directory, "CSV_to_Excel_Output_Selected_Columns2.xlsx")
selected_columns.to_excel(excel_file_path, index=False)

print(f"Selected columns from CSV file have been converted to {excel_file_path}")
