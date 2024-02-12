
import requests
import json


ACCESS_TOKEN = 'P9bPdbaMsFgU9vZcotRxXaJsqrYSUcszQ7x6ilQO4OEwW2B7LpBtR3tZMDG3' #'ZdGvXQUsnL592Cwo1NQjV6QVGahechZElPWYRbWEReKpxGBTEw5qlNfaVpxS'
ZENODO_URL = 'https://sandbox.zenodo.org/api/deposit/depositions'

METADATA = {
     'metadata': {
         'title': '',
         'description': '',
         'upload_type': 'dataset',
         'license': 'cc-by',
         'subjects': [{"term": "Cultural property", "identifier": "https://id.loc.gov/authorities/subjects/sh97000183.html", "scheme": "url"}],
         'method': 'EAMENA data entry methodology',
         'creators': [{'name': "EAMENA database",
                       'affiliation': "University of Oxford, University of Southampton"}],
         'contributors': [],
         'keywords': [],
         'dates': {}
        #  'communities': "[{'identifier': 'eamena'}]",
        #  'related_identifiers': zn.zenodo_related_identifiers()
     }
 }

def create_zenodo_bucket(params): 
    r = requests.post(ZENODO_URL,
                    params=params,
                    json={})
        
    deposition_id = r.json()['id']
    bucket_url = r.json()["links"]["bucket"]
    return deposition_id, bucket_url

def add_zenodo_data(bucket_url, params, filename):
    zip_file_name = filename + ".zip"
    with open(zip_file_name, "rb") as fp:
        r = requests.put(
            "%s/%s" % (bucket_url, zip_file_name),
            data = fp,
            params = params,
        )

def add_zenodo_metadata(deposition_id, params, metadata):
    r = requests.put('%s/%s' % (ZENODO_URL, deposition_id),
                    params = params,
                    data = json.dumps(metadata))

def zenodo_publish(title, filename, description, zenodo_calculated_fields):
    params = {'access_token': ACCESS_TOKEN}
    deposition_id, bucket_url = create_zenodo_bucket(params)
    add_zenodo_data(bucket_url, params, filename)
    METADATA['metadata']['title'] = title
    METADATA['metadata']['description'] = description
    METADATA['metadata']['contributors'] = zenodo_calculated_fields[0]
    METADATA['metadata']['keywords'] = zenodo_calculated_fields[1]
    METADATA['metadata']['dates'] = zenodo_calculated_fields[2]
    add_zenodo_metadata(deposition_id, params, METADATA)
    r = requests.post('%s/%s/actions/publish' % (ZENODO_URL, deposition_id),
                        params={'access_token': ACCESS_TOKEN} )

    r = requests.get(ZENODO_URL,
                  params={'access_token': ACCESS_TOKEN})
    print(r.json()[0]['links']['html'])
    return r.json()[0]['links']['html']


