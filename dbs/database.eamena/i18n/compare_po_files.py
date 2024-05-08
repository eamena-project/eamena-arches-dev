## Compare 2 PO file to find sentences in A that are missing in B. Used for the `ckb` translation 


#%% 
import polib

# Load PO files
po_basis = "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/bases/arches-70_djangopo_en.po" 
# po_basis = "C:/Users/Thomas Huet/Downloads/django.po" 
po_translated = "C:/Rprojects/arches/arches/locale/ckb/LC_MESSAGES/django.po"
po_differences = "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/ckb/django_differences.po" 

po_a = polib.pofile(po_basis)
po_b = polib.pofile(po_translated)

print(f"the PO base file has {len(po_a)} and the already translated PO file has {len(po_b)}")

#%% 

# Collect msgids from file_b for quick lookup
msgids_b = {entry.msgid for entry in po_b}

#%%

# Initialize a new PO file to store differences
po_diff = polib.POFile()
po_diff.metadata = {
    'Project-Id-Version': '1.0',
    'Report-Msgid-Bugs-To': '',
    'POT-Creation-Date': '',
    'PO-Revision-Date': '',
    'Last-Translator': '',
    'Language-Team': '',
    'Language': '',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
}

# Find and add entries that are in file A but not in file B
for entry in po_a:
    if entry.msgid not in msgids_b:
        po_diff.append(entry)

# Save differences to the output PO file
po_diff.save(po_differences)
print(f"PO file with differences saved to {po_differences}")
