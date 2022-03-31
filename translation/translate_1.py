# translate a PO file
# special character like '�' in place of 'é' only occurs with a PO output extension, 
# they do not appear in the output file if the extension is TXT

import os, re, csv
from deep_translator import GoogleTranslator

target_language = 'fr'
# number of maximum lines for a paragraph message
max_lines = 10
# one or the other depending on environment
path_fold = os.getcwd()+'/translation'
path_fold = os.getcwd()

# read PO
print("Read source file")
with open(path_fold+'/for_translation_arches-70_djangopo_fr_samp.po') as f_in:
    # don't catch the empty lines
    lines = [line.strip() for line in f_in if line.strip()]
print("     "+str(len(lines))+" lines to write")

# write PO/TXT
f_out = open(path_fold+'/translated_out.po', 'w')
#writer = csv.writer(f_out, quoting=csv.QUOTE_NONE, delimiter=' ', escapechar='\\', lineterminator='\n')
writer = f_out
# with indexes
num_lines = list(range(0,len(lines)))
print("Write output file")
for l in num_lines:
    if l % 100 == 0:
        print("     write "+"line "+str(l)+"/"+str(len(lines)))
    already_translated = 0
    line = lines[l]
    if(line.startswith('msgid')):
    # translate
        writer.write(line + '\n')
        if(line.startswith('msgid \"\"')):
        # the message has various lines
            ltext_eng = []
            for sl in list(range(1,max_lines)):
                sub_line = lines[l+sl]
                if(sub_line.startswith('msgstr')): 
                # the end of the message has been reached
                    # TODO
                    # if bool(re.match('msgstr \"[A-Z]+', sub_line)):
                    #     # test if the message has been already translated
                    #     already_translated = 1
                    break
                else:
                    text_eng = sub_line
                    text_translated = GoogleTranslator(source='en', target=target_language).translate(text_eng)
                    line_translated = text_translated
                    writer.write(line_translated + '\n')
        # to be translated
        text_eng = re.sub('msgid', '', line)
        text_translated = GoogleTranslator(source='en', target=target_language).translate(text_eng)
        if (text_translated is not None):
        # do not write None type (ie, "") and already translated messages
            # print(line_translated)
            line_translated = 'msgstr' + text_translated
            # line_translated = line_translated.rstrip()
            if already_translated == 0:
                # write if not already translated
                writer.write(line_translated + '\n')
    elif(not line.startswith('msgstr')):
    # not repeat the first msgtr
        writer.write(line + '\n')
    elif(bool(re.match('msgstr \"[A-Z]+', line))):
    # msgtr was translated by someone before running this script
        writer.write(line + '\n')
