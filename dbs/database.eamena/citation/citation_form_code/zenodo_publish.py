import requests
import json

# CORRECTED: The 'communities' key has been added to ensure the dataset
# is published to the 'eamena' community on Zenodo.
METADATA_TEMPLATE = {
    'metadata': {
        'title': '',
        'description': '',
        'upload_type': 'dataset',
        'license': 'cc-by',
        'communities': [{'identifier': 'eamena'}],
        'subjects': [{"term": "Cultural property", "identifier": "https://id.loc.gov/authorities/subjects/sh97000183.html", "scheme": "url"}],
        'method': 'EAMENA data entry methodology',
        'creators': [{'name': "EAMENA database", 'affiliation': "University of Oxford, University of Southampton"}],
        'contributors': [],
        'keywords': [],
        'dates': {}
    }
}

def zenodo_publish(title, filename, description, zenodo_calculated_fields, zenodo_url, token):
    """
    Handles the entire publication process to Zenodo.
    """
    params, headers = {'access_token': token}, {"Content-Type": "application/json"}
    
    print(f"Attempting to create new deposition at: {zenodo_url}")
    try:
        r = requests.post(zenodo_url, params=params, json={}, headers=headers)
        r.raise_for_status()
        deposition_data = r.json()
        deposition_id, bucket_url = deposition_data['id'], deposition_data["links"]["bucket"]
        print(f"Successfully created deposition with ID: {deposition_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating Zenodo deposition: {e}\nResponse: {e.response.text if e.response else 'N/A'}")
        return None

    print("Uploading data file to Zenodo...")
    try:
        with open(f"{filename}.zip", "rb") as fp:
            r = requests.put(f"{bucket_url}/{filename}.zip", data=fp, params=params)
            r.raise_for_status()
        print("File upload successful.")
    except Exception as e:
        print(f"Error uploading file to Zenodo: {e}")
        return None

    print("Uploading metadata...")
    # Use the corrected template
    metadata = METADATA_TEMPLATE.copy()
    metadata['metadata'].update({
        'title': title,
        'description': description,
        'contributors': zenodo_calculated_fields[0],
        'keywords': zenodo_calculated_fields[1],
        'dates': zenodo_calculated_fields[2]
    })
    
    try:
        r = requests.put(f'{zenodo_url}/{deposition_id}', params=params, data=json.dumps(metadata), headers=headers)
        r.raise_for_status()
        print("Metadata upload successful.")
    except requests.exceptions.RequestException as e:
        print(f"Error uploading metadata: {e}\nResponse: {e.response.text if e.response else 'N/A'}")
        return None

    print("Publishing deposition...")
    try:
        r = requests.post(f'{zenodo_url}/{deposition_id}/actions/publish', params=params)
        r.raise_for_status()
        print("Publication successful!")
        return r.json()['links']['html']
    except requests.exceptions.RequestException as e:
        print(f"Error publishing deposition: {e}\nResponse: {e.response.text if e.response else 'N/A'}")
        return None
