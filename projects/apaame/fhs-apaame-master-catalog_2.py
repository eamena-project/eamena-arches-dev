# record the "APAAME Master Catalog" (AMC) file/folder hierarchical structure (FHS) in an XLSX file

#%% 
# variables
import os
from openpyxl import Workbook

# in file
AMC = "D:/APAAME Master Catalog"
# AMC = "C:/Rprojects/eamena-arches-dev/projects"
# AMC = "D:/TEMP"
# out file
FHS = "C:/Rprojects/eamena-arches-dev/projects/apaame/amc-fhs-2.xlsx"

wb = Workbook()
ws = wb.active
ws.title = "APAAME Master Catalog FHS"

# %%
n = 0
for root, dirs, files in os.walk(AMC):
	n = n + 1
	if (n % 250) == 0:
		print(" read record " + str(n))
	# Calculate the depth of the current directory
	depth = len(root.replace(AMC, '').strip(os.sep).split(os.sep))
	text = "- [ ] " + root 
	# Level 1 directories: full folder names in column A
	if depth == 1:
		ws.append([text, ""])  # Add the full path of level 1 folders to column A, leave column B empty
	# Level 2 directories: full subfolder names in column B
	elif depth == 2:
		ws.append(["", text])  # Leave column A empty, add the full path of level 2 folders to column B

# No processing for level 3 or beyond, as requested

# Save the workbook
wb.save(FHS)
print(f"{os.path.basename(FHS)} has been exported")


# %%
