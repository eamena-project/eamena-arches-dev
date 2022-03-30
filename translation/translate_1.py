# translate a PO file
# special character like '�' in place of 'é' only occurs with a PO output extension, 
# they do not appear in the output file if the extension is TXT

import os, re, csv
from deep_translator import GoogleTranslator

to_language = 'fr'
# number of maximum lines for a paragraph message
max_lines = 10
# one or the other depending on environment
path_fold = os.getcwd()+'/translation'
path_fold = os.getcwd()

# read PO
with open(path_fold+'/for_translation_arches-70_djangopo_fr_samp.po') as f_in:
    lines = [line.strip() for line in f_in if line.strip()]

# write PO/TXT
f_out = open(path_fold+'/translated_out.po', 'w')
writer = csv.writer(f_out, quoting=csv.QUOTE_NONE, delimiter=' ', escapechar=' ', lineterminator='\n')
# with indexes
num_lines = list(range(0,len(lines)))
for l in num_lines:
    line = lines[l]
    if(line.startswith('msgid')):
    # repeat and translate
        writer.writerow([line])
        if(line.startswith('msgid \"\"')):
        # the message has various lines
            ltext_eng = []
            for sl in list(range(1,max_lines)):
                sub_line = lines[l+sl]
                if(sub_line.startswith('msgstr')): 
                # the end of the message has been reached
                    break
                else:
                    text_eng = sub_line
                    text_translated = GoogleTranslator(source='en', target=to_language).translate(text_eng)
                    line_translated = text_translated
                    writer.writerow([line_translated])
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