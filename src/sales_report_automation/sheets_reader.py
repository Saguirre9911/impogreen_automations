import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


# Replace 'your_credentials.json' with the path to your credentials file
# Replace 'your_spreadsheet_id' with the actual ID of your Google Sheet
# Replace 'your_range' with the range of cells you want to read, e.g., 'Sheet1!A1:D5'
class Sheetsreader:

    def __init__(self, credentials_path, spreadsheet_id, range_name):
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name

    def read_data(self):
        creds = Credentials.from_service_account_file(self.credentials_path)
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range=self.range_name,
            )
            .execute()
        )
        values = result.get("values", [])
        return values

    def transform_data_values(self):
        values = self.read_data()
        values = pd.DataFrame(values[1:], columns=values[0])
        values.set_index("CE", inplace=True)
        values.drop(columns=["FP"], inplace=True)
        values.drop(columns=["OBSERVACIONES"], inplace=True)
        values.drop(columns=["ESTADO"], inplace=True)
        return values

    def transform_data_db(self):
        values = self.read_data()
        values = pd.DataFrame(values[1:], columns=values[0])
        values.set_index("COD COL", inplace=True)
        return values
