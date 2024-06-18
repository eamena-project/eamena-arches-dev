def collect_untranslated_messages(url):
    import polib
    import pandas as pd
    import requests

    untranslated = []

    response = requests.get(url)
    if response.status_code == 200:
        po = polib.pofile(response.text)
        for entry in po.untranslated_entries():
            if not entry.msgstr:  # Checking for untranslated messages
                untranslated.append({'msgid': entry.msgid, 'file': url})
        df = pd.DataFrame(untranslated)
        return df
    else:
        return pd.DataFrame([], columns=['msgid', 'file'])

# Specify the path to your locale directory in your Django project
po_file = 'https://raw.githubusercontent.com/eamena-project/arches/master/arches/locale/ckb/LC_MESSAGES/django.po'
df_untranslated = collect_untranslated_messages(po_file)
df_untranslated.to_csv('C:/Rprojects/eamena-arches-dev/dbs/kahd/untranslated_messages.csv', index=False)
