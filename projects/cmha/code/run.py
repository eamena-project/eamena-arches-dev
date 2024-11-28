from PIL import Image
from exif import Image as ExifImage
from fractions import Fraction

def convert_to_degrees(value):
	"""Convert decimal degrees to EXIF-compatible format."""
	degrees = int(value)
	minutes = int((value - degrees) * 60)
	seconds = (value - degrees - minutes / 60) * 3600
	return (Fraction(degrees, 1), Fraction(minutes, 1), Fraction(int(seconds * 100), 100))

def add_metadata_XY_to_photo_2(image_path, new_image_path, latitude, longitude):
	# Copy the original image to the new path
	with open(image_path, "rb") as src, open(new_image_path, "wb") as dst:
		dst.write(src.read())

	# Open the copied image to add EXIF data
	with open(new_image_path, "rb+") as img_file:
		img = ExifImage(img_file)
		if not img.has_exif:
			raise ValueError("Image does not have EXIF metadata")

		# Add GPS metadata
		lat_deg, lat_min, lat_sec = convert_to_degrees(latitude)
		lon_deg, lon_min, lon_sec = convert_to_degrees(abs(longitude))

		img.gps_latitude = [lat_deg, lat_min, lat_sec]
		img.gps_latitude_ref = "N" if latitude >= 0 else "S"
		img.gps_longitude = [lon_deg, lon_min, lon_sec]
		img.gps_longitude_ref = "E" if longitude >= 0 else "W"

		# Save changes
		img_file.seek(0)
		img_file.write(img.get_file())
		img_file.truncate()

	print("Image + coordinates saved with EXIF GPS metadata")




# # append the path to functions handling photograph metadata
# # os.chdir('c:/Rprojects/eamena-arches-dev/projects/cod/code')
# sys.path.append('c:/Rprojects/eamena-arches-dev/projects/cod/code')
# import cod
# # from cod import function_a # add_metadata_XY_to_photo
# # print(function_a())
# from cod import add_metadata_XY_to_photo_2

def add_metadata_XY_to_photo_exif(dirIn_photos = "c:/Rprojects/eamena-arches-dev/projects/cmha/db_data/Wadi Naqqat", hps = "c:/Rprojects/eamena-arches-dev/projects/cmha/data/wadi_naqqat_new_ok.geojson", exiftool_path = "c:/exiftool-13.03_64/exiftool.exe", dirOut_photos = None):
	"""
	Append coordinates to the EXIF metdata of the photograph using exiftools.exe

	:param dirIn_photos: path to the input folder. All subfolder will be parsed and their name matched against the names of hertiage places in the `hps` file. For example: folder WN01 in `dirIn_photos` will match the string WN01 in the 'Resource Name' field of hps
	:param hps: A GeoJSON file of HP to grab the coordinates from. 
	:param exiftool_path: path to the exiftool EXE

	>>> add_metadata_XY_to_photo_exif()

	"""
	import os
	from pathlib import Path
	import geopandas as gpd
	import subprocess

	gdf = gpd.read_file(hps)
	directories = [d for d in os.listdir(dirIn_photos) if os.path.isdir(os.path.join(dirIn_photos, d))]

	for a_dir in directories:
		mydir = dirIn_photos + "/" + a_dir
		print(f"read {a_dir}")
		# coordinates of this specific HP
		filtered_gdf = gdf[gdf['Resource Name'].str.contains(a_dir, na=False)]
		coords = [(point.x, point.y) for point in filtered_gdf.geometry]
		gps_latitude = coords[0][1]
		gps_longitude = coords[0][0]
		# create the output dir
		if dirOut_photos is not None:
			path = Path(dirIn_photos) 
			dirRoot = path.parent.absolute()
			print(f"will export the updated photo into: {dirRoot} ")
			# dirOut = dirRoot + "db_data/" + a_dir + "_out"
			dirOut = dirRoot + "db_data/" + a_dir + "_out"
			if not os.path.exists(dirOut):	
				os.makedirs(dirOut)
		# photos
		list_photos = os.listdir(mydir)
		for a_photo in list_photos:
			image_path = mydir + "/" + a_photo
			if dirOut_photos is not None:
				new_image_path = dirOut + "/" + a_photo
			print(f"    - image: {a_photo}")
			command = [
				exiftool_path,
				'-gpslatitude=' + str(gps_latitude),
				'-gpslongitude=' + str(gps_longitude),
				'-overwrite_original',
				image_path
			]
			# command = f"& {exiftool_path} -gpslatitude='{gps_latitude}' -gpslongitude='{gps_longitude}' -overwrite_original '{image_path}'"
			# print(command)
			result = subprocess.run(command, text=True, capture_output=True)
			# Print the output and any error
			print("Output:", result.stdout)
			print("Error:", result.stderr)

