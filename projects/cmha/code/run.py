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

