# from PIL import Image, ExifTags
imagename = "C:/Rprojects/eamena-arches-dev/data/photos/APAAME_20211026_RHB-0705.DNG"

# img = Image.open(imagename)
# exif = { ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS }

import exifread
# Open image file for reading (must be in binary mode)
f = open(imagename, 'rb')
tags = exifread.process_file(f)
exif_lens = tags['EXIF FocalLength'].values
exif_model = tags['Image Model'].values
exif_model = str(exif_lens)

from libxmp import XMPFiles, consts
xmpfile = XMPFiles( file_path=imagename, open_forupdate=True )