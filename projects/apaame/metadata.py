import exifread

file_path = 'D:/APAAME Master Catalog/1998/1998-05-12/APAAME_19980512_RHB-0172.tif'
file_path = 'D:/APAAME Master Catalog/1998/1998-05-12/APAAME_19980512_RHB-0142D.tif'

# Open the image file
with open(file_path, 'rb') as f:
    # Read EXIF data
    tags = exifread.process_file(f)
    
    # Print all EXIF data found
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print(f"{tag}: {tags[tag]}")
