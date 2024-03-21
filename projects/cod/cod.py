
## Read City of the Dead (cod) database tables


#%% 
# read the photograph metadata
import os
import re
import pandas as pd
import piexif
from PIL import Image

# %%

## read the database exported tables
root_path = "C:/Rprojects/eamena-arches-dev/projects/cod/"
db_path = root_path + "db_data/tables/"
# records = units
record_db_path = db_path + "records.xlsx"
df_rec_metadata = pd.read_excel(record_db_path)
# photographs metadata
photo_db_path = db_path + "photos.xlsx"
df_im_metadata = pd.read_excel(photo_db_path)
# list the records = units from the metadata file
units = list(df_im_metadata['unitnumber'].unique())

## photographs
photo_im_path = root_path + "db_data/photos"
# create a pandas mapping file
df_im_map = pd.DataFrame({'unitnumber': [item.split("s_")[0] for item in os.listdir(photo_im_path)], 'directory': os.listdir(photo_im_path)})


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
