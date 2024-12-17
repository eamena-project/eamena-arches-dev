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

def apaame_fhs(AMC = "D:/APAAME Master Catalog", FHS = "C:/Rprojects/eamena-arches-dev/projects/apaame/amc-fhs-3.xlsx"):
	"""
	Creates an XLSX file with two levels of subfolders from the APAAME external hard drive
 
	Usefull to create a Markdown checkboxes list for the upload from the external hard drive to the ResourceSpace / ArchDAMS server 
	
	:param AMC: The root of the external hard drive
	:param FHS: The output file
	:return: An XLSX file
	"""
	import os
	from openpyxl import Workbook
	wb = Workbook()
	ws = wb.active
	# ws.title = "APAAME Master Catalog FHS"
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
	wb.save(FHS)
	print(f"{os.path.basename(FHS)} has been exported")

apaame_fhs()
# %%

def apaame_metadata(file_path = 'D:/APAAME Master Catalog/1998/1998-05-12/APAAME_19980512_RHB-0142D.tif'):
	"""
	Read the metadata of an image
 	
	:param file_path: The path to the image
	:return: Print the metadata
	"""
	import exifread

	# file_path = 'D:/APAAME Master Catalog/1998/1998-05-12/APAAME_19980512_RHB-0172.tif'
	# file_path = 'D:/APAAME Master Catalog/1998/1998-05-12/APAAME_19980512_RHB-0142D.tif'

	# Open the image file
	with open(file_path, 'rb') as f:
		# Read EXIF data
		tags = exifread.process_file(f)
		
		# Print all EXIF data found
		for tag in tags.keys():
			if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
				print(f"{tag}: {tags[tag]}")

apaame_metadata()

# %%


