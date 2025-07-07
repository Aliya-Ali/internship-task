import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Connect to Google Sheets
def connect_to_sheet(sheet_name: str):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # Connect to first sheet
    return sheet



# Update status and profile link after submission
def update_submission( sheet, row_number, profile_link):
    sheet.update_cell(row_number, 4, profile_link) 

def get_vertical_business_data(sheet):
    """
    Reads key-value business data from column A and B only (ignoring others).
    """
    rows = sheet.get_all_values()
    data = {}

    for row in rows:
        if len(row) >= 2:
            key = row[0].strip()  # Column A
            value = row[1].strip()  # Column B
            if key and value:
                data[key] = value

    return data

