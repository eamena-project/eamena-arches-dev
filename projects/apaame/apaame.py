
#%%
# match the content of an APAAME folder (ex: 1999-06-16/) with a list of metadata and highlight which files in the folder are absent in the RS. Useful for incomplete uploads

# def match_rs_and_hardrive():

import os
import pandas as pd

# Load the Excel file
xlsx_path = "D:/APAAME/inRS.xlsx"
folder_path = "C:/Rprojects/eamena-arches-dev/projects/apaame/www"
# image_ext = list(".png", ".tif", ".tiff", ".jpg", ".jpeg")

df = pd.read_excel(xlsx_path, engine='openpyxl')  # Ensure you use the correct sheet name or index
file_names = df['Original filename'].tolist()  # Replace 'column_name' with the name of your column
file_names = [x for x in file_names if str(x) != 'nan']
folder_files = os.listdir(folder_path)
# Normalize file names if needed (like trimming spaces, converting to lower case)
# file_names = [name.strip().lower() for name in file_names]
file_names = [name.strip() for name in file_names]
# folder_files = [file.strip().lower() for file in folder_files]
folder_files = [file.strip() for file in folder_files]

# Find common and unique files
common_files = [file for file in file_names if file in folder_files]
unique_to_folder = [file for file in folder_files if file not in file_names]
if verbose:
	print("Files in RS and hard drive:", common_files)
	print("Files only in hard drive:", unique_to_folder)
# return(unique_to_folder)



#%% 
# record the "APAAME Master Catalog" (AMC) file/folder hierarchical structure (FHS) in an XLSX file
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

# import os

# # Path to the directory you want to scan
# directory_path = 'D:/APAAME Master Catalog/1998/1998-05-12'

# # Initialize an empty set to hold unique filenames without extension
# unique_filenames = set()

# # List all files in the directory
# for filename in os.listdir(directory_path):
# 	# Check if the file is not a TIF file
# 	if not filename.lower().endswith(('.tif', '.tiff')):
# 		# Remove the file extension and add to the set
# 		unique_filename_without_extension = os.path.splitext(filename)[0]
# 		unique_filenames.add(unique_filename_without_extension)

# # Print the unique filenames
# l = list()
# for name in unique_filenames:
# 	l.append(name)
# l_sorted = sorted(l)

# print(l_sorted)


# %%

def apaame_list_file2convert():

	all_filenames = set()
	expected_filenames = set()
	not_expected_filenames = set()
	ext_to_keep = ('.tif', '.tiff') #, '.jpg', '.jpeg')

	all_items = os.listdir(directory_path)
	files_only = [item for item in all_items if os.path.isfile(os.path.join(directory_path, item))]

	# all files
	for filename in files_only:
		all_filenames.add(os.path.splitext(filename)[0])
		# expected (TIFs, maybe JPG)
		if filename.lower().endswith(ext_to_keep):
			expected_filenames.add(os.path.splitext(filename)[0])
		# not expected (not TIFs, maybe not JPG)
		if not filename.lower().endswith(ext_to_keep):
			not_expected_filenames.add(os.path.splitext(filename)[0])
	# check the missing TIFFs
	not_expected_filenames = set(not_expected_filenames) - set(expected_filenames)
	not_expected_filenames_list = sorted(list(not_expected_filenames))


	# print('\n'.join(not_expected_filenames_list))

	# for not_expect in not_expected_filenames_list:
	# 	print(not_expect)
	# %%

	import csv

	matched_files = list()

	for file in files_only:
		# Get the full path of the file
		# full_path = os.path.join(files_only, file)
		base_name = os.path.splitext(file)[0]
		# If the base name is in your list, store the full filename
		if base_name in not_expected_filenames_list:
			matched_files.append(file)

	# Path to your TSV file, the last subfolder
	root_path = "C:/Rprojects/eamena-arches-dev/projects/apaame/data"
	outFile = root_path + "/" + os.path.basename(directory_path) + "_to_convert.tsv"
	# tsv_file_path = os.path.basename(directory_path)

	# Open the TSV file in append mode
	with open(outFile, 'a', newline='') as file:
		# Create a csv writer object for a TSV file
		tsv_writer = csv.writer(file, delimiter='\t')
		for element in matched_files:
			tsv_writer.writerow([element])
# for base_name, full_filename in matched_files.items():
# 	print(f"{full_filename}")
# %%
