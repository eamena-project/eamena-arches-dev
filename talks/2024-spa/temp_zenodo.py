from sickle import Sickle

sickle = Sickle('https://zenodo.org/oai2d')
records = sickle.ListRecords(metadataPrefix='oai_dc', set='user-eamena')
for record in records:
    print(record.metadata['identifier'][0])
