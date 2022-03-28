from deep_translator import GoogleTranslator

to_translate = 'Hello World'

translated = GoogleTranslator(source='en', target='fr').translate(to_translate)

print(translated)