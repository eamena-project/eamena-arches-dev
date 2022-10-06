import os
from pyavm import AVM
import exifread
import pandas as pd
from PIL import Image #, ExifTags
# from PIL.ExifTags import TAGS

df = pd.DataFrame(columns=["Creator","Rights","Title","Description","Credit","Date","Contact","Subject","Model","Lens"])

pathIn = "C:/Rprojects/eamena-arches-dev/data/photos/"
pathOut = "C:/Rprojects/eamena-arches-dev/projects/apaame-photos/metadata.csv"
dirIn = os.listdir(pathIn)
for i in range(len(dirIn)):
    print(str(i) + "- read " + dirIn[i])
    imagename = pathIn + dirIn[i]
    # imagename = path + "APAAME_20211026_RHB-0705.DNG"
    #img = Image.open(imagename) # for XMP
    # exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    # XMP
    xmp = AVM.from_image(imagename)
    xmp_creator = xmp.Creator
    xmp_rights = xmp.Rights
    xmp_title = xmp.Title
    xmp_description = xmp.Description # coordinates
    xmp_credits = xmp.Credit
    xmp_date = xmp.Date
    xmp_contact = xmp.Contact
    xmp_subjects = xmp.Subject # key words
    # EXIF
    # exif = image.getexif()
    # exif_model = exif[272] # 272 is the Model key
    # exif_lens = exif[42036] # 42036 is the LensModel key
    # exif_lens = exif[37386] # xxx is the LensModel key
    # exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    f = open(imagename, 'rb')
    exifTags = exifread.process_file(f) # for EXIF
    exif_model = exifTags['Image Model'].values
    exif_lens = exifTags['EXIF FocalLength'].values
    exif_lens = str(exif_lens)
    df.loc[i] = [xmp_creator, xmp_rights, xmp_title, xmp_description, xmp_credits, xmp_date, xmp_contact, xmp_subjects, exif_model, exif_lens]
# export
df.to_csv(pathOut, sep=',')
# print(avm)

# exif = image.getexif()

# for tag_id in exif:
#     # get the tag name, instead of human unreadable tag id
#     tag = TAGS.get(tag_id, tag_id)
#     data = exif.get(tag_id)
#     # decode bytes 
#     if isinstance(data, bytes):
#         data = data.decode()
#     print(f"{tag:25}: {data}")
