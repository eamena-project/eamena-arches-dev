# Grids with 0 Heritage places. Return a dataframe

#%%

import pandas as pd
import gspread

keys = "C:/Rprojects/eamena-arches-dev/data/keys/"
gsheet_key = "gsheet-407918-65ebbb9cb656.json" # a key from the Google API platform
gkey = keys + gsheet_key

gc = gspread.service_account(filename=gkey) # Google Client
spreadsheet = gc.open("EAMENA Final Grid Squares")
grid_square_values = []

# Loop over each worksheet in the Google Sheet
for worksheet in spreadsheet:
    print("Current Sheet:", worksheet.title)
    records = worksheet.get_all_records()
    for record in records:
        if record['Pins in GE'] == 0:
            grid_square_values.append(record['Grid Square'])
            
print("Grid Square values where 'Pins in GE' is 0:", grid_square_values)

vals = [0] * len(grid_square_values)

gs_with_0_hp = pd.DataFrame(
  {'nb_hp': vals,
   'grid_num': grid_square_values
  })

# %%
# read a dataframe with the number of HP summed by GS
eamena_gs_nb_hps = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/grids/eamena_hps_by_grids_231212.csv"
gs_nb_hps = pd.read_csv(eamena_gs_nb_hps)

# %%
# merge the two df

df = pd.concat([gs_nb_hps, gs_with_0_hp])


# %%
# write a CSV

df.to_csv("C:/Rprojects/eamena-arches-dev/data/grids/grids_nb_hp_231213.csv", index=False)
# %%
