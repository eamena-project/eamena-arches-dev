
#%%
# libraries
import os
from pyavm import AVM
import exifread
import pandas as pd
from PIL import Image #, ExifTags
# from PIL.ExifTags import TAGS

#%% 
# collect all metadata

valid_extensions = ['.jpg', '.jpeg', '.tiff', '.tif', '.dng', '.png']

pathIn = "C:/Rprojects/eamena-arches-dev/projects/apaame/sample/"
pathOut = "C:/Rprojects/eamena-arches-dev/projects/apaame/sample/metadata.csv"
dirIn = os.listdir(pathIn)
all_metada = pd.DataFrame(columns=['Filename', 'Tag Name', 'Value'])
for i in range(len(dirIn)):
    photo, extension = os.path.splitext(dirIn[i])
    extension = extension.lower()
    if extension in valid_extensions:
        photo_name = dirIn[i]
        print(str(i) + "- read " + photo_name)
        imagename = pathIn + photo_name
        # Open the image file
        with open(imagename, 'rb') as f:
            tags = exifread.process_file(f)

        # Create empty lists to store tag names and values
        tag_names = []
        tag_values = []

        # Iterate through the EXIF tags
        for tag, value in tags.items():
            tag_names.append(str(tag))
            tag_values.append(str(value))

        # Create a Pandas DataFrame from the lists
        metadata_df = pd.DataFrame({'Filename': photo, 'Tag Name': tag_names, 'Value': tag_values})
        all_metada = pd.concat([all_metada, metadata_df], ignore_index = True)
        # all_metada = all_metada.append(metadata_df)
# Display the DataFrame
print(all_metada.to_markdown(index=False))


#%%
# not run...
# selected field and expected extensions, export (or not), ...

df = pd.DataFrame(columns=["Name", "Creator", "Rights", "Title", "Description", "Credit", "Date", "Contact", "Subject", "Model", "Lens"])
export_df = False
mtd_exif = True
mtd_xml = False

# %%
# not run ..
for i in range(len(dirIn)):
    _, extension = os.path.splitext(dirIn[i])
    extension = extension.lower()
    if extension in valid_extensions:
        photo_name = dirIn[i]
        print(str(i) + "- read " + photo_name)
        imagename = pathIn + photo_name
        # imagename = path + "APAAME_20211026_RHB-0705.DNG"
        #img = Image.open(imagename) # for XMP
        # exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
        if mtd_xml:
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
        if mtd_exif:
        # EXIF
        # exif = image.getexif()
        # exif_model = exif[272] # 272 is the Model key
        # exif_lens = exif[42036] # 42036 is the LensModel key
        # exif_lens = exif[37386] # xxx is the LensModel key
        # exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
        f = open(imagename, 'rb')
        exifTags = exifread.process_file(f) # for EXIF
        exif_model = exifTags['Image Model'].values
        exif_lens = exifTags['FocalLength'].values
        exif_lens = str(exif_lens)
        df.loc[i] = [photo_name, xmp_creator, xmp_rights, xmp_title, xmp_description, xmp_credits, xmp_date, xmp_contact, xmp_subjects, exif_model, exif_lens]

print(df.to_markdown(index=False))

# export
if export_df:
    df.to_csv(pathOut, sep=',')
    print("Done")

# exif = image.getexif()

# for tag_id in exif:
#     # get the tag name, instead of human unreadable tag id
#     tag = TAGS.get(tag_id, tag_id)
#     data = exif.get(tag_id)
#     # decode bytes 
#     if isinstance(data, bytes):
#         data = data.decode()
#     print(f"{tag:25}: {data}")

# %%
