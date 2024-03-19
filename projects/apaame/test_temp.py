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

# import os

# # Path to the directory you want to scan
# dir2read = 'D:/APAAME Master Catalog/1998/1998-05-12'

# # Initialize an empty set to hold unique filenames without extension
# unique_filenames = set()

# # List all files in the directory
# for filename in os.listdir(dir2read):
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

def apaame_list_file2convert(dir2read = 'D:/APAAME Master Catalog/1998/1998-05-12', ext_to_keep = ('.tif', '.tiff', 'jpg', '.jpeg'), dirOut = "C:/Rprojects/eamena-arches-dev/projects/apaame/data"):
	"""
	List all images in a folder, find those which do not have the appropriate extension (.tif, or maybe .jpg). Return a TSV file with listed images that need a conversion

	The TSV file will take the name of the dir2read input (ex: `1998-05-12_to_convert`)
 	
	:param dir2read: The path to the folder containing the images
	:param ext_to_keep: The extensions considered to be appropriate to be uploaded to the server (TIF and maybe JPG)
	:param dirOut: The output path to the TSV

	:return: A TSV file
	"""
	import csv

	all_filenames = set()
	expected_filenames = set()
	not_expected_filenames = set()
	

	all_items = os.listdir(dir2read)
	files_only = [item for item in all_items if os.path.isfile(os.path.join(dir2read, item))]

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

	matched_files = list()

	for file in files_only:
		base_name = os.path.splitext(file)[0]
		if base_name in not_expected_filenames_list:
			matched_files.append(file)

	# Path to your TSV file, the last subfolder
	fileOut = os.path.basename(dir2read)
	outFile = dirOut + "/" + fileOut + "_to_convert.tsv"
	# tsv_file_path = os.path.basename(dir2read)

	if(len(matched_files) > 0):
		# Open the TSV file in append mode
		with open(outFile, 'a', newline='') as file:
			# Create a csv writer object for a TSV file
			tsv_writer = csv.writer(file, delimiter='\t')
			for element in matched_files:
				full_path = dir2read + "/" + element
				tsv_writer.writerow([full_path])
		print(f"{fileOut} has been exported listing {len(matched_files)} images to convert")
	if(len(matched_files) == 0):
		print(f"None of the '{fileOut}' images have to be converted")

apaame_list_file2convert()
# %%
