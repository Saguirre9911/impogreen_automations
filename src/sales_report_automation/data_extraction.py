import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from sheets_reader import Sheetsreader

spreadsheetId = "1zDdwFmbb55Stu91UJHZPykqPCOHKBM90zHdCR36jN58"
range = "'LIQUIDACION NOMINA'!A1:Q18"
creds = "credentials.json"

sheets_reader_payroll = Sheetsreader(
    credentials_path=creds, spreadsheet_id=spreadsheetId, range_name=range
)
payroll_data = sheets_reader_payroll.transform_data_values()
print(payroll_data)
spreadsheetId = "1iBgRdWeMZ9Fq6QAjnNCvxp_5O9Q04dSm1gLTKVhhP4k"
range = "BDIMPORTADORA!A3:N29"
creds = "credentials.json"


sheets_reader_db = Sheetsreader(
    credentials_path=creds, spreadsheet_id=spreadsheetId, range_name=range
)
db_data = sheets_reader_db.transform_data_db()
print(db_data)

unifided_data = pd.merge(payroll_data, db_data, left_index=True, right_index=True)
# has que el nombre de la columna index sea Cod Empleado
unifided_data.index.name = "COD EMPLEADO"
print(unifided_data)
# save unified data to a excel file
unifided_data.to_excel("unifided_data.xlsx")
