# record the "APAAME Master Catalog" (AMC) file/folder hierarchical structure (FHS) in an XLSX file

def list_directories(path, excel_file='folder_arborescence.xlsx'):
    # Create a new Excel workbook
    

    # Traverse the directory and record the folder arborescence
    traverse_directory(path, ws)

    # Save the Excel workbook
    wb.save(excel_file)

def traverse_directory(path, ws, depth=0):
    try:
        # List all subdirectories

        # Record the current directory in the Excel sheet
        ws.append([os.path.basename(path)] + [""] * depth)



    except PermissionError:
        # Handle permission errors (you may want to log these)
        print(f"Permission error in directory: {path}")

#%% variables

import os
from openpyxl import Workbook

# in file
AMC = "D:/APAAME Master Catalog"
AMC = "C:/Rprojects/eamena-arches-dev/projects"
# out file
FHS = "C:/Rprojects/eamena-arches-dev/projects/apaame/amc-fhs.xlsx"

#%% create WS
wb = Workbook()
ws = wb.active
ws.title = "Folder Arborescence"

ws.append(["level1", "level2", "level3", "level4", "level5"])  # Adjust the number of depths as needed

#%% 

# level1
subdirectories = [d for d in os.listdir(AMC) if os.path.isdir(os.path.join(AMC, d))]

# for subdir in subdirectories:
# 	# Recursively traverse each subdirectory
# 	traverse_directory(os.path.join(path, subdir), ws, level+ 1)

subdir = 'aaa'


# %%
