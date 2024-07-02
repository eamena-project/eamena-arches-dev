

# %%
# merge the tables of the 2 databases, and remve duplicated rows
import os
import pandas as pd

# Paths to the Excel files
data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/"
data_in_N = data_in + "N/"
data_in_S = data_in + "S/"
path_out = "C:/Rprojects/eamena-arches-dev/projects/cod/business_data/csv/"
xlsx_files = os.listdir(data_in_N)
for xlsx_file in xlsx_files:
	data_in_filename = os.path.splitext(xlsx_file)[0]
	df1 = pd.read_excel(data_in_N + xlsx_file)
	df2 = pd.read_excel(data_in_N + xlsx_file)
	combined_df = pd.concat([df1, df2])
	unique_df = combined_df.drop_duplicates()
	csv_output_path = path_out + data_in_filename + '.csv'
	unique_df.to_csv(csv_output_path, index=False)
	print(f"The file {data_in_filename + '.csv'} has been created in {path_out}")


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
	else:
		print("It is neither a file nor a directory.")


# data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/221224PhotosBCKP.xlsx"
data_in = "C:/Rprojects/eamena-arches-dev/projects/cod/db_data/tables/"
path_out = "C:/Rprojects/eamena-arches-dev/projects/cod/business_data/csv/"
xlsx2csv(data_in, path_out)


#%% 
# read the photograph metadata
import os
import re
import pandas as pd
import piexif
from PIL import Image

root_path = "C:/Rprojects/eamena-arches-dev/projects/cod/"

#%% 
## photographs
photo_im_path = root_path + "db_data/photos"
split_on = "s_" # all folder names are like: 88s_Ibrahim Mahmud/
unitnumbers = [item.split(split_on)[0] for item in os.listdir(photo_im_path)]
df_im_map = pd.DataFrame(
						 {'unitnumber': unitnumbers, 
						  'directory': os.listdir(photo_im_path)}
						  )

#%%
## listing

def list_files(root_dir):
    data = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            size = os.path.getsize(file_path)
            data.append({
                "folder": os.path.basename(dirpath),
                "filename": file,
                "size (MB)": round(size/1000000, 1)
            })
    return pd.DataFrame(data)

file_info_df = list_files(photo_im_path)
print(file_info_df)

file_info = file_info_df[(file_info_df["size (MB)"] > 0)]

# %%
## Read City of the Dead (cod) database tables

## read the database exported tables
db_path = root_path + "db_data/tables/"
# records = units
record_db_path = db_path + "records.xlsx"
df_rec_metadata = pd.read_excel(record_db_path)
# photographs metadata
photo_db_path = db_path + "photos.xlsx"
df_im_metadata = pd.read_excel(photo_db_path)
# list the records = units from the metadata file
units = list(df_im_metadata['unitnumber'].unique())

# ## photographs
# photo_im_path = root_path + "db_data/photos"
# # create a pandas mapping file
# df_im_map = pd.DataFrame(
# 	{'unitnumber': [item.split("s_")[0] for item in os.listdir(photo_im_path)], 'directory': os.listdir(photo_im_path)}
# 	)


# %%

# loop over the units, match units and folders with photographs
for unit in units:
	print(f"*** read unit/record '{unit}' ***")
	# add 0 if n < 10
	if unit < 10:
		unit_t = "0" + str(unit)
	else:
		unit_t = str(unit)
	selected_unit = df_im_map[df_im_map['unitnumber'] == unit_t]
	print(f"- directory: \n{selected_unit.to_markdown(index=False)}")
	unit_folder = selected_unit.iloc[0,1]
	photos = os.listdir(photo_im_path + '\\' + unit_folder)
	print(f"- photos: \n{photos}")
	print("\n")
	# loop over photo, add metadata, save
	for a_photo in range(len(photos)):
		a_photo_OK = re.sub(r'.*?(DSC|IMG)', r'\1', photos[a_photo])
		print(f"  + read photo: {photos[a_photo]} (ie {a_photo_OK})")
		a_photo_metadata = df_im_metadata[df_im_metadata['filename'].str.lower() == a_photo_OK.lower()]
		if len(a_photo_metadata) > 0:
			print(f"    = photo metadata:")
			print(a_photo_metadata.to_markdown(index=False))
			print("\n")
			cur_folder = selected_unit['directory'].iloc[0]
			photo_path = photo_im_path + "\\" + cur_folder + "\\" + photos[a_photo]
			print(f"    = write metadata")		
			# Load the image
			img = Image.open(photo_path)
			# extract metadata from the table
			im_descr = a_photo_metadata['description'].iloc[0]
			im_artis = a_photo_metadata['takenby'].iloc[0]
			im_title = df_rec_metadata[df_rec_metadata['ID'] == unit]["attribution"].iloc[0]
			im_caption = im_title + ". " + im_descr
			# Prepare EXIF data
			# Note: '0th', 'Exif', and other IFDs are parts of the EXIF standard. You can add more fields as needed.
			exif_dict = {
				"0th": {
					piexif.ImageIFD.ImageDescription: im_descr,
					piexif.ImageIFD.Artist: im_artis,
					# change XPTitle to Title?
					piexif.ImageIFD.XPTitle: im_title.encode('utf-16le'),
					# change XPComment to Comment?
					piexif.ImageIFD.XPComment: im_caption.encode('utf-16le'),
					# change XPAuthor to Author?
					piexif.ImageIFD.XPAuthor: im_artis.encode('utf-16le'),
					# Add Caption?
					# Add coordinates from 'df_rec_metadata'
				},
				"Exif": {
					# Add Exif tags if needed
				}
			}
			exif_bytes = piexif.dump(exif_dict)
			# overwrite
			# TODO: save with the highest resolution (if not, 1 MB -> 500 KB)
			img.save(photo_path, exif=exif_bytes)
			print(f"    => {photos[a_photo]} has been saved")
			img.close()
		else:
			print(f"    /!\ there are no metadata for {photos[a_photo]}")
		print("\n")

# %%
