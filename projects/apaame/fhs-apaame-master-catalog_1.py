# record the "APAAME Master Catalog" (AMC) file/folder hierarchical structure (FHS) in an XLSX file

#%% variables

import os
from openpyxl import Workbook

# in file
AMC = "D:/APAAME Master Catalog"
# AMC = "C:/Rprojects/eamena-arches-dev/projects"
# out file
FHS = "C:/Rprojects/eamena-arches-dev/projects/apaame/amc-fhs-1.xlsx"

#%% run

l = [x[0] for x in os.walk(AMC)]

wb = Workbook()
ws = wb.active
ws.title = "APAAME Master Catalog FHS"

n = 0
for row_num, item in enumerate(l, start=1):
	n = n + 1
	columns = item.split('\\')
	ws.append(columns)
	if (n % 100) == 0:
		print(" read record " + str(n))
      
wb.save(FHS)
# %%
