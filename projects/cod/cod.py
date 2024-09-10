

# %%
# 

def merge2dbs(data_in_N, data_in_S, path_out):
	"""
	Merge the tables of the 2 databases, and remove duplicated rows

	:param data_in_N: A folder path to the folder root of the tables from the first DB
	:param data_in_S: A folder path to the folder root of the tables from the second DB
	:param path_out: A folder path

	"""
	import os
	import pandas as pd

	xlsx_files = os.listdir(data_in_N)
	for xlsx_file in xlsx_files:
		data_in_filename = os.path.splitext(xlsx_file)[0]
		df1 = pd.read_excel(data_in_N + xlsx_file)
		df2 = pd.read_excel(data_in_S + xlsx_file)
		combined_df = pd.concat([df1, df2])
		unique_df = combined_df.drop_duplicates()
		csv_output_path = path_out + data_in_filename + '.csv'
		unique_df.to_csv(csv_output_path, index=False)
		print(f"The file {data_in_filename + '.csv'} has been created in {path_out}")


data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/"
data_in_N = data_in + "N/"
data_in_S = data_in + "S/"
path_out = "C:/Rprojects/eamena-arches-dev/projects/cod/business_data/csv/"
# merge2dbs(data_in_N, data_in_S, path_out)

# %%
# convert all XLSX tables into CSV

def xlsx2csv(data_in, path_out):
	"""
	Read an XLSX, or a folder of XLSX, and convert it/them into a CSV. The filenames would be the same.

	:param data_in: A folder path or a file path
	:param path_out: A folder path

	"""
	import os

	if os.path.isdir(data_in):
		print(f"Read the directory {data_in}")
		all_files = os.listdir(data_in)
		xlsx_files = [file for file in all_files if file.endswith('.xlsx')]
		for xlsx_file in xlsx_files:
			data_in_filename = os.path.splitext(xlsx_file)[0]
			print(f"Read the XLSX file {data_in_filename}")
			df = pd.read_excel(f"{data_in}/{xlsx_file}")
			path_out_data = f"{path_out}/{data_in_filename}.csv"
			df.to_csv(path_out_data, index=False)
			print(f"The file {data_in_filename}.csv has been exported into {path_out}")
	elif os.path.isfile(data_in):
		if data_in.endswith('.xlsx'):
			data_in_filename = os.path.basename(data_in)
			data_in_filename = os.path.splitext(data_in_filename)[0]
			# data_in_filename = os.path.splitext(data_in)[0]
			print(f"Read the XLSX file {data_in_filename}")
			df = pd.read_excel(data_in)
			path_out_data = f"{path_out}/{data_in_filename}.csv"
			df.to_csv(path_out_data, index=False)
			print(f"The file {data_in_filename}.csv has been exported into {path_out}")


# data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/221224PhotosBCKP.xlsx"
data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/"
path_out = "C:/Rprojects/eamena-arches-dev/projects/cod/business_data/csv/"
# xlsx2csv(data_in, path_out)


#%%
# EXIF metdata

def convert_to_degrees(value):
	""" 
	Convert decimal degree to degrees, minutes, seconds tuple, formatted for EXIF. 
	"""
	degrees = int(value)
	minutes = int((value - degrees) * 60)
	seconds = (value - degrees - minutes / 60) * 3600
	degrees = (degrees, 1)
	minutes = (minutes, 1)
	seconds = (int(seconds * 100), 100)  # More accurate second representation as rational
	return degrees, minutes, seconds


def add_metadata_XY_to_photo(image_path, new_image_path, latitude, longitude):
	# TODO: adapt to the dataset structure: find the decimal coordinates in the `records` table
	"""
	Append coordinates to the EXIF metdata of the photograph
	
	"""
	from PIL import Image
	import piexif

	# image_path = 'path/to/your/image.jpg'
	img = Image.open(image_path)
	exif_dict = piexif.load(img.info['exif']) if 'exif' in img.info else {}
	gps_latitude = convert_to_degrees(latitude)
	gps_longitude = convert_to_degrees(abs(longitude))  # Longitude should be positive for EXIF
	# GPS data according to EXIF spec
	gps_ifd = {
		piexif.GPSIFD.GPSLatitudeRef: 'N' if latitude >= 0 else 'S',
		piexif.GPSIFD.GPSLatitude: gps_latitude,
		piexif.GPSIFD.GPSLongitudeRef: 'E' if longitude >= 0 else 'W',
		piexif.GPSIFD.GPSLongitude: gps_longitude,
	}
	exif_dict['GPS'] = gps_ifd
	exif_bytes = piexif.dump(exif_dict)
	# new_image_path = 'path/to/your/new_image.jpg'
	img.save(new_image_path, "jpeg", exif=exif_bytes)
	print("Image + coordinates saved")

image_path = "C:/Rprojects/eamena-arches-dev/projects/cod/www/4171_sl_JDs.jpg"
new_image_path = 'C:/Rprojects/eamena-arches-dev/projects/cod/www/4171_sl_JDs_with_coords.jpg'
# add_metadata_XY_to_photo(image_path, new_image_path, latitude = 48.848270462241814, longitude = 2.41120456097722) # loc: Paris


# %%
## Read City of the Dead (cod) database tables

## read the database exported tables
# db_path = root_path + "business_data/xlsx/"
# # records = units
# record_db_path = db_path + "records_NS.xlsx"
# df_rec_metadata = pd.read_excel(record_db_path)
# # photographs metadata
# photo_db_path = db_path + "photos_NS.xlsx"
# df_im_metadata = pd.read_excel(photo_db_path)
# # list the records = units from the metadata file
# units = list(df_im_metadata['unitnumber'].unique())

# ## photographs
# photo_im_path_in = root_path + "db_data/photos_in"
# # create a pandas mapping file
# df_im_map = pd.DataFrame(
# 	{'unitnumber': [item.split("s_")[0] for item in os.listdir(photo_im_path_in)], 'directory': os.listdir(photo_im_path_in)}
# 	)


# %%
def add_metadata_to_photo(root_path = "C:/Rprojects/eamena-arches-dev/projects/cod/", photos_in = "db_data/photos_in", photo_metadata = "business_data/xlsx/photos_NS.xlsx", records_in = "business_data/xlsx/records_NS.xlsx", photo_out = "db_data/photos_out", exif_metadata=False, xmp_metadata=False, iptc_metadata=False, gps_metadata=False, verbose = True):
	"""
	Append metadata into the photograph by reading other XLSX tables

	:param root_path: Root path of the project 
	:param photos_in: Path to the folder where the photographs are stored
	:param photo_metadata: Path to the file describing the photographs
	:param records_in: Path to the file of the records (aka HP), useful to collect data 
	:param photo_out: Path to the folder where the photographs with metdata will be stored
	:param xmp_metadata: Add XMP metadata if True
	
	"""
	import re
	from PIL import Image
	# from PIL import IptcImagePlugin
	from iptcinfo3 import IPTCInfo
	import piexif
	# from libxmp import XMPFiles, consts
	import subprocess
	import os
	import pandas as pd
	import logging

	# avoid the message 'Marker scan hit start of image data' to be printed
	logging.getLogger("iptcinfo").setLevel(logging.ERROR)

	photo_missed = []
	# db_path = root_path + "business_data/xlsx/records_NS.xlsx"
	record_db_path = root_path + records_in
	df_rec_metadata = pd.read_excel(record_db_path)
	# photographs metadata
	photo_db_path = root_path + photo_metadata
	df_im_metadata = pd.read_excel(photo_db_path)
	# repacement to match the photo/folder labels
	df_im_metadata['filename'] = df_im_metadata['filename'].apply(lambda x: re.sub(r'.*?(DSC|IMG)', r'\1', x))
	# list the records = units from the metadata file
	units = list(df_im_metadata['unitnumber'].unique())
	photo_im_path_in = root_path + photos_in
	photo_im_path_out = root_path + photo_out
	# create a mapping table
	split_on = "s_" # all folder names are like: 88s_Ibrahim Mahmud/
	unitnumbers = [item.split(split_on)[0] for item in os.listdir(photo_im_path_in)]
	df_im_map = pd.DataFrame(
							{'unitnumber': unitnumbers, 
							'directory': os.listdir(photo_im_path_in)}
							)
	# loop over the units, match units and folders with photographs
	stop_nb = 0
	# units.reverse()
	for unit in units[50:]:
		stop_nb += 1
		if stop_nb > 25:
			print("... Early stop - Done ...")
			return photo_missed
		print(f"*** read unit/record/heritage '{unit}' ***")
		# add 0 or 00 before to get the COD number
		if unit < 10:
			unit_t = "0" + str(unit)
		# elif unit > 9:
		# 	unit_t = "00" + str(unit)
		else:
			unit_t = str(unit)
		selected_unit = df_im_map[df_im_map['unitnumber'] == unit_t]
		if verbose:
			print(f"- directory: \n{selected_unit.to_markdown(index=False)}")
		unit_folder = selected_unit.iloc[0,1]
		photos = os.listdir(photo_im_path_in + '\\' + unit_folder)
		# print(photos)
		if verbose:
			print(f"- photos: \n{photos}")
			print("\n")
		# loop over photo, add metadata, save
		for a_photo in range(len(photos)):
			a_photo_OK = re.sub(r'.*?(DSC|IMG)', r'\1', photos[a_photo])
			# a_photo_OK = str(a_photo)
			if verbose:
				print(f"  + read photo: {photos[a_photo]} (ie {a_photo_OK})")
			# a_photo_metadata = df_im_metadata[df_im_metadata['picture'].str.lower() == a_photo_OK.lower()]
			a_photo_metadata = df_im_metadata[df_im_metadata['filename'].str.lower() == a_photo_OK.lower()]
			# a_photo_metadata = re.sub(r'.*?(DSC|IMG)', r'\1', df_im_metadata[df_im_metadata['picture'].str.lower() == a_photo_OK.lower()]
			if len(a_photo_metadata) > 0:
				if verbose:
					print(f"    = photo metadata:")
					print(a_photo_metadata.to_markdown(index=False))
					print("\n")
				cur_folder = selected_unit['directory'].iloc[0]
				photo_path_in = photo_im_path_in + "\\" + cur_folder + "\\" + photos[a_photo]
				photo_path_out = photo_im_path_out + "\\" + cur_folder + "\\" + photos[a_photo]
				# extract metadata from the table
				im_descr = a_photo_metadata['description'].iloc[0]
				im_artis = a_photo_metadata['takenby'].iloc[0]
				im_date = a_photo_metadata['datetaken'].iloc[0]
				# match the row/record/heritage place
				im_record_id = df_rec_metadata[df_rec_metadata['ID'] == unit]["ID"].iloc[0]
				im_record_attribution = df_rec_metadata[df_rec_metadata['ID'] == unit]["attribution"].iloc[0]
				# im_title = df_rec_metadata['ID'].iloc[0]
				if im_record_id < 10:
					im_record_id_t = "00" + str(im_record_id)
				if im_record_id < 100 and im_record_id > 9:
					im_record_id_t = "0" + str(im_record_id)
				im_title = im_record_attribution + " (COD-" + str(im_record_id_t) + ")"
				im_caption = im_title + ". " + im_descr
				im_coord_N = df_rec_metadata[df_rec_metadata['ID'] == unit]["coordinateN"].iloc[0]
				im_coord_E = df_rec_metadata[df_rec_metadata['ID'] == unit]["coordinateE"].iloc[0]
				im_copyright = "Copyright, Archinos architecture, 2024. All rights reserved."
				im_country = "Egypt"
				if verbose:
					print('       im_descr: ' + im_descr)
					print('       im_artis: ' + im_artis)
					print('       im_title: ' + im_title)
					print('       im_caption: ' + im_caption)
					print('       im_date: ' + im_date)
					print('       im_copyright: ' + im_copyright)
					print('       im_coord_N: ' + str(im_coord_N))
					print('       im_coord_E: ' + str(im_coord_E))
				if verbose:
					print(f"    = write metadata")
					# photo_path_in =  photo_path_out
				# prevent to rm former EXIF metadata
				# create dic
				# Load the image
				img = Image.open(photo_path_in)
				size_img_in = os.path.getsize(photo_path_in)
				size_img_in_MB = round(size_img_in/1000000, 1)
				try:
					exif_dict = piexif.load(img.info['exif'])
				except KeyError:
					exif_dict = {'0th': {}, 'Exif': {}, 'GPS': {}, '1st': {}, 'Interop': {}, 'thumbnail': None}
				if exif_metadata:
					if verbose:
						print(f"EXIF metadata (without GPS)---")
					exif_dict['0th'][piexif.ImageIFD.ImageDescription] = im_caption.encode('utf-8')
					exif_dict['0th'][piexif.ImageIFD.Artist] = im_artis.encode('utf-8')
					exif_dict['0th'][piexif.ImageIFD.XPTitle] = im_title.encode('utf-8')
					exif_dict['0th'][piexif.ImageIFD.XPComment] = im_caption.encode('utf-8')
					exif_dict['0th'][piexif.ImageIFD.XPAuthor] = im_artis.encode('utf-8')
					exif_dict['0th'][piexif.ImageIFD.DateTime] = im_date.encode('utf-8')
					exif_dict['0th'][piexif.ImageIFD.Copyright] = im_copyright.encode('utf-8')
					# exif_dict['Exif'][piexif.ImageIFD.Artist] = im_artis.encode('utf-8')
					# exif_dict['Exif'][piexif.ImageIFD.ImageDescription] = im_caption.encode('utf-8')
					# exif_dict['0th'][piexif.ImageIFD.GPSDestCountry] = im_country.encode('utf-8')
					# add_metadata_XY_to_photo(image_path, new_image_path, latitude = im_coord_N, longitude = im_coord_E) # loc: Paris
					# exif_dict['0th'][piexif.IptcIFD.Artist] = im_artis.encode('utf-8')
				if gps_metadata:
					if verbose:
						print(f"GPS metadata ---")
					gps_latitude = convert_to_degrees(im_coord_N)
					gps_longitude = convert_to_degrees(abs(im_coord_E))  # Longitude should be positive for EXIF
					# GPS data according to EXIF spec
					gps_ifd = {
						piexif.GPSIFD.GPSLatitudeRef: 'N' if im_coord_N >= 0 else 'S',
						piexif.GPSIFD.GPSLatitude: gps_latitude,
						piexif.GPSIFD.GPSLongitudeRef: 'E' if im_coord_E >= 0 else 'W',
						piexif.GPSIFD.GPSLongitude: gps_longitude,
					}
					exif_dict['GPS'] = gps_ifd

				# exif_dict = {
				# 	"0th": {
				# 		piexif.ImageIFD.ImageDescription: im_descr,
				# 		piexif.ImageIFD.Artist: im_artis,
				# 		# change XPTitle to Title?
				# 		piexif.ImageIFD.XPTitle: im_title.encode('utf-16le'),
				# 		# change XPComment to Comment?
				# 		piexif.ImageIFD.XPComment: im_caption.encode('utf-16le'),
				# 		# change XPAuthor to Author?
				# 		piexif.ImageIFD.XPAuthor: im_artis.encode('utf-16le'),
				# 		# Add Caption?
				# 		# Add coordinates from 'df_rec_metadata'
				# 	},
				# }
				exif_bytes = piexif.dump(exif_dict)
				# overwrite
				# TODO: save with the highest resolution (if not, 1 MB -> 500 KB)
				original_dpi = img.info.get('dpi')
				out_folder = photo_im_path_out + "\\" + cur_folder
				if not os.path.exists(out_folder):
					os.makedirs(out_folder)
				img.save(photo_path_out, exif=exif_bytes, quality=95, dpi=original_dpi, optimize=True, progressive=True)
				if verbose:
					print(f"    => {photos[a_photo]} has been saved with EXIF metadata")
				img.close()
				size_img_out = os.path.getsize(photo_path_out)
				size_img_out_MB = round(size_img_out/1000000, 1)
				if verbose:
					print(f"    image size (MB): {size_img_in_MB} => {size_img_out_MB}")
				if xmp_metadata:
					if verbose:
						print(f"XMP metadata ---")
					# XMP Handling with exiftool
					xmp_data = {
						"XMP-dc:Title": "Your Title Here",
						"XMP-dc:Description": "A brief description here."
					}
					# Convert XMP data to exiftool command arguments
					xmp_args = []
					for tag, value in xmp_data.items():
						xmp_args.extend(['-' + tag + '=' + value])
					print(photo_path_out)
					cmd_exiftool = ['exiftool'] + xmp_args + ['-overwrite_original', photo_path_out]
					cmd_exiftool = f'C:\exiftool\exiftool {xmp_args} -overwrite_original "{photo_path_out}"'
					print(cmd_exiftool)
					# print("HERE")
					# subprocess.run(r"cd C:/exiftool && dir", shell=True)
					# subprocess.run("cd pwd", shell=True)

					# subprocess.run(cmd_exiftool)

					if verbose:
						print(f"    => {photos[a_photo]} has been saved with XMP metadata")
				if iptc_metadata:
					if verbose:
						# print(photo_path_out)
						print(f"IPTC metadata ---")
					info = IPTCInfo(photo_path_out, force=True)
					info['caption/abstract'] = im_caption.encode('utf-8')
					info['object name'] = im_title.encode('utf-8')
					info['copyright notice'] = im_copyright.encode('utf-8')
					info['credit'] = f'{im_artis} - {im_copyright}'
					# my_artiste = im_artis.encode('utf-8')
					# my_copyright = im_copyright.encode('utf-8')
					# info['credit'] = f'{my_artiste} - {my_copyright}'
					info['country/primary location name'] = "Egypt"
					# exif_dict['0th'][piexif.ImageIFD.Artist] = im_artis.encode('utf-8')
					# exif_dict['0th'][piexif.ImageIFD.XPTitle] = im_title.encode('utf-8')
					# exif_dict['0th'][piexif.ImageIFD.XPComment] = im_caption.encode('utf-8')
					# exif_dict['0th'][piexif.ImageIFD.XPAuthor] = im_artis.encode('utf-8')
					# exif_dict['0th'][piexif.ImageIFD.DateTime] = im_date.encode('utf-8')
					# exif_dict['0th'][piexif.ImageIFD.Copyright] = im_copyright.encode('utf-8')
					info.save_as(photo_path_out)
			else:
				print(f"    /!\ No metadata available for {photos[a_photo]}")
				print(f"        {a_photo_OK} not found in the metadata table")
				photo_missed.append(a_photo_OK)
			if not xmp_metadata and not exif_metadata and not gps_metadata:
				if verbose:
						print(f"    CREATE HERE A DF WITH THE IMAGE NAME AS A KEY")
			if verbose:
				print("\n")
			# print(info.keys())
	if verbose:
		print("return the lis of unmatched photos and metdata")
	return photo_missed


# add_metadata_to_photo(gps_metadata=True)
# add_metadata_to_photo(gps_metadata=True, exif_metadata=True)
photo_missed = add_metadata_to_photo(gps_metadata=True, iptc_metadata=True, verbose=False)
print("\n- [ ] ".join(photo_missed))

# %%



# input_image_path = 'C:\Rprojects\eamena-arches-dev\projects\cod\db_data\photos_in\\02s_MuhTalaatHarb\\aDSC_1607s.JPG'

# import piexif
# from PIL import Image
# import subprocess
# import json

# # Load an image
# img = Image.open(input_image_path)

# # EXIF Handling with piexif
# exif_dict = piexif.load(img.info.get('exif', b''))
# exif_dict['0th'][piexif.ImageIFD.Make] = u'Canon'.encode('utf-8')
# exif_dict['0th'][piexif.ImageIFD.Model] = u'Canon EOS 80D'.encode('utf-8')
# exif_bytes = piexif.dump(exif_dict)

# # Save the image with new EXIF data
# temp_filename = 'C:\Rprojects\eamena-arches-dev\projects\cod\db_data\photos_out\\aDSC_1607s.JPG
# img.save(temp_filename, exif=exif_bytes)

# # XMP Handling with exiftool
# xmp_data = {
#     "XMP-dc:Title": "Your Title Here",
#     "XMP-dc:Description": "A brief description here."
# }

# # Convert XMP data to exiftool command arguments
# xmp_args = []
# for tag, value in xmp_data.items():
#     xmp_args.extend(['-' + tag + '=' + value])

# # Call exiftool to write XMP data
# subprocess.run(['exiftool'] + xmp_args + ['-overwrite_original', temp_filename])

# # Rename temp file if needed
# final_filename = 'final_output_image.jpg'
# subprocess.run(['mv', temp_filename, final_filename])

# print("EXIF and XMP metadata updated successfully.")
