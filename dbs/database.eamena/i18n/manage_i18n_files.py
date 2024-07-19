
# Series of functions to manage the i18n/l10n of Django messages (po_*.py), thesauri, and RM (rm_*.py)

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
    """
    Compare 2 PO file to find sentences in A that are missing in B. Used for the `ckb` translation: running this script creates a new PO file that can be converted to an XLSX one with the po2excel.py script

    example: po_empty_messages()

    """
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


def rm_read(rm_file = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/Heritage Place.json"):
    """
    Read resource model

    """
    import json
    import requests

    # hp_concepts = "Heritage Place.json"
    # f = open(rm_file)
    response = requests.get(rm_file)
    data = response.json()
    # data = json.load(f)
    hp_conceptscollections = list(data.keys())
    nb = 0
    # sum all concepts (nodes?)
    for hp_conceptscollection in hp_conceptscollections:
        nb = nb + len(data[hp_conceptscollection])
    print(n)

def rm_remove_arabic_hard_written(rm_file = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/Information Resource.json", rm_file_out = 'Information Resource_without_arabic_hard_written.json', outdir = None):
    """
    Remove the Arabic hard written values that remain in the cards dictionnaries in the HP RM and export in a file

    """
    import os
    import json
    import re
    import requests

    response = requests.get(rm_file)
    data = response.json()

    for graph in data['graph']:
        for card in graph['cards']:
            if 'name' in card and card['name']:
                # rm text after the '/' in the dictionary
                if type(card['name']) == dict:
                    card['name']['en'] = re.sub(r'/.*', '', card['name']['en']).strip()
                else:
                    card['name'] = re.sub(r'/.*', '', card['name']).strip()

    outfile = outdir + "\\" + rm_file_out
    with open(outfile, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("Saved in " + outfile)


def rm_to_xlsx(rm_file = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/Heritage Place_without_hard_written_arabic.json", rm_file_out = 'Heritage Place_card_nodes.xlsx', outdir = None):
    """
    Read a RM file, extract the 'en' values from the cards, export in an XLSX column
    
    """
    import os
    import json
    import re
    import requests
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active

    response = requests.get(rm_file)
    data = response.json()

    l = []
    for graph in data['graph']:
        for card in graph['cards']:
            if 'name' in card and card['name']:
                if type(card['name']) == dict:
                    node = card['name']['en']
                else:
                    node = card['name']
                l.append(node)

    for index, value in enumerate(l, start=1):
        ws.cell(row=index, column=1, value=value)
    outfile = outdir + "\\" + rm_file_out
    wb.save(outfile)
    print("Saved in " + outfile)
    
# rm_read()
import os
# NB: le cwd ne marche pas pareil quand on run dans la fenetre interactive
outdir = os.path.dirname(os.path.realpath(__file__))
# remove Arabic -------------------------------------------------------------------
# rm_remove_arabic_hard_written(rm_file = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/Information Resource.json", rm_file_out = 'Information Resource_without_arabic_hard_written.json', outdir = outdir) # IR
rm_remove_arabic_hard_written(rm_file = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/Person_Organization.json", rm_file_out = 'Person_Organization_without_arabic_hard_written.json', outdir = outdir) # P/O
# to XLSX -------------------------------------------------------------------
def rm_to_xlsx(rm_file = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/Information Resource_without_arabic_hard_written.json", rm_file_out = 'Information Resource_card_nodes.xlsx', outdir = None)
# def rm_to_xlsx(rm_file = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/i18n/data/bases/Person_Organization_without_arabic_hard_written.json", rm_file_out = 'Person_Organization_card_nodes.xlsx', outdir = None)