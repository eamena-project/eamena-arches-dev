# Grids with 0 Heritage places

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by URL
url = 'https://docs.google.com/spreadsheets/d/1r2VLLiyJMaCl8l7C4sKilQ4ZMqEfAwhQAwYC7wGzmk0/edit#gid=1142334803'
spreadsheet = client.open_by_url(url)

# Create an empty list to store 'Grid Square' values
grid_square_values = []

# Loop over each worksheet in the Google Sheet
for worksheet in spreadsheet.worksheets():
    # Get the worksheet data as a DataFrame
    df = pd.DataFrame(worksheet.get_all_records())

    # Filter rows where 'Pins in GE' is 0 and get 'Grid Square' values
    filtered_data = df[df['Pins in GE'] == 0]['Grid Square'].tolist()

    # Extend the list with the values from the current worksheet
    grid_square_values.extend(filtered_data)

# Print the final list of 'Grid Square' values
print("Grid Square values where 'Pins in GE' is 0:", grid_square_values)
