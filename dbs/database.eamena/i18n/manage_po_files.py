
def po_empty_messages(po_file_path = "https://raw.githubusercontent.com/eamena-project/arches/master/arches/locale/ckb/LC_MESSAGES/django.po", po_empty_messages = "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/ckb/django_empty_messages.po" ):
    
    import polib
    import requests

    po_file = requests.get(po_file_path).text
    po = polib.pofile(po_file)

    new_po = polib.POFile()
    new_po.metadata = po.metadata

    for entry in po:
        if not entry.msgstr:
            new_po.append(entry)

    print(f"the output PO file has {len(new_po)} empty messages")

    new_po.save(po_empty_messages)



def po_compare2files(po_basis_path = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/arches-70_djangopo_en.po" 
, po_translated_path = "https://raw.githubusercontent.com/eamena-project/arches/master/arches/locale/ckb/LC_MESSAGES/django.po", po_differences = "C:/Rprojects/eamena-arches-dev/dbs/database.eamena/i18n/data/ckb/django_differences.po" 
):
    ## Compare 2 PO file to find sentences in A that are missing in B. Used for the `ckb` translation 

    import polib
    import requests

    # Load PO files
    po_basis = requests.get(po_basis_path).text
    po_translated = requests.get(po_translated_path).text

    po_a = polib.pofile(po_basis)
    po_b = polib.pofile(po_translated)

    print(f"the PO base file has {len(po_a)} messages and the already translated PO file has {len(po_b)} messages")

    # Collect msgids from file_b for quick lookup
    msgids_b = {entry.msgid for entry in po_b}

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


po_empty_messages()