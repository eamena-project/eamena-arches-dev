# Grids with 0 Heritage places

#%% 
import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import pandas as pd

keys = "C:/Rprojects/eamena-arches-dev/data/keys/"
gsheet_key = "gsheet-407918-65ebbb9cb656.json" # a key from the Google API platform
gkey = keys + gsheet_key

gc = gspread.service_account(filename=gkey) # Google Client
#%% 

spreadsheet = gc.open("EAMENA Final Grid Squares")
grid_square_values = []

# Loop over each worksheet in the Google Sheet
for worksheet in spreadsheet:
    print("Current Sheet:", worksheet.title)
    # Get all records from the current worksheet as a list of dictionaries
    records = worksheet.get_all_records()
    # Loop over each record in the worksheet
    for record in records:
        # Check if 'Pins in GE' is 0 and collect 'Grid Square' values
        if record['Pins in GE'] == 0:
            grid_square_values.append(record['Grid Square'])
            
# Print the final list of 'Grid Square' values
print("Grid Square values where 'Pins in GE' is 0:", grid_square_values)

