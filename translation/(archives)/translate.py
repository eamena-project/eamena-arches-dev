# translate a PO file
# special character like '�' in place of 'é' only occurs with the PO extension 
# in the output file, they do not appear in the output file extension is TXT

import os, re, csv
from deep_translator import GoogleTranslator
# print (os.getcwd())

to_language = 'fr'
# one or the other
path_fold = os.getcwd()+'/translation'
path_fold = os.getcwd()

# read PO
with open(path_fold+'/for_translation_arches-70_djangopo_fr_samp.po') as f_in:
    # lines = (line.rstrip() for line in f_in) # All lines including the blank ones
    lines = [line.strip() for line in f_in if line.strip()]
    # lines = f_in.readlines()

# write PO/TXT
f_out = open(path_fold+'/translated_out.po', 'w')
writer = csv.writer(f_out, quoting=csv.QUOTE_NONE, delimiter=' ', escapechar=' ')
for line in lines:
    # line = l.rstrip()
    if(line.startswith('msgid')):
    # repeat and translate
        writer.writerow([line])
        if(line.startswith('msgid \"\"')):                                      # the message has various lines
            pass
        # to be translated
        text_eng = re.sub('msgid', '', line)
        text_translated = GoogleTranslator(source='en', target=to_language).translate(text_eng)
        if (text_translated is not None):
        # do not read None type (ie, "")
            line_translated = 'msgstr ' + text_translated
            # line_translated = line_translated.rstrip()
            writer.writerow([line_translated])
    elif(not line.startswith('msgstr')):
    # not repeat the first msgtr
        writer.writerow([line])