# translate a PO file

import os, re, csv
from deep_translator import GoogleTranslator
# print (os.getcwd())

to_language = 'fr'

# read PO
with open(os.getcwd()+'/translation/for_translation_arches-70_djangopo_fr_samp.po') as f:
    lines = f.readlines()
print(os.getcwd()+'/translation/for_translation_arches-70_djangopo_fr_samp.po')

# write TXT
f = open(os.getcwd()+'/translation/translated_out.po', 'w')
writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=' ', escapechar=' ')
for line in lines:
    if(line.startswith('msgid')):
    # repeat and translate
        writer.writerow([line])
        # to be translated
        text_eng = re.sub('msgid', '', line)
        text_translated = GoogleTranslator(source='en', target=to_language).translate(text_eng)
        if (text_translated is not None):
        # do not read None type (ie, "")
            line_translated = 'msgstr \"' + text_translated + "\""
            writer.writerow([line_translated])
    else:
    # not to be translated
        writer.writerow([line])