# Translation for Arches v7.0 internationalisation

Read a portable object (PO) file, use Python *regex* and 'deep_translator' libraries to convert `msgid` message from `eng` into `fr`, write a new PO file
  
<p align="center">  
<a href="https://github.com/eamena-oxford/eamena-arches-dev/blob/main/translation/for_translation_arches-70_djangopo_fr_samp.po">PO file input</a> :arrow_right: 
<a href="https://github.com/eamena-oxford/eamena-arches-dev/blob/main/translation/translate_1.py">Python file</a> :arrow_right: 
<a href="https://github.com/eamena-oxford/eamena-arches-dev/blob/main/translation/translated_out.po">PO file output</a>
</p>

## Current issues with the output

- [ ] special characters (only for a PO output extension, no issue if TXT)
- [ ] extra or missing spaces within the messages and between the messages
- [ ] translate already translated messages
- [ ] paragraph message/multiline messages
    - [ ] missing `msgstr` tag
    - [ ] reversed order between source language and target language



