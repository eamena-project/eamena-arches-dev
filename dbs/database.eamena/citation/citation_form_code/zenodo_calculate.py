from collections import Counter
import pandas as pd
from datetime import datetime

def duplicate_remove(data, field_id='EAMENA ID'):
    """
    Removes duplicate features from a GeoJSON dataset based on a unique ID.
    This function is now correctly placed in this file.
    """
    if 'features' not in data:
        return []
    seen_ids = set()
    unique_features = []
    for feature in data['features']:
        feature_id = feature.get('properties', {}).get(field_id)
        if feature_id and feature_id not in seen_ids:
            unique_features.append(feature)
            seen_ids.add(feature_id)
    return unique_features

def add_alternative_name(data):
    """
    Iterates through each feature and adds an 'alternative-name' property,
    copying the value from the 'Name' property if it exists.
    """
    print("\n--- Modifying Data: Adding 'alternative-name' property ---")
    if 'features' in data and data.get('features'):
        modified_count = 0
        for feature in data['features']:
            # Check for 'Name' property and ensure it's not None
            if feature.get('properties') and 'Name' in feature['properties'] and feature['properties']['Name']:
                feature['properties']['alternative-name'] = feature['properties']['Name']
                modified_count += 1
        print(f"Appended 'alternative-name' to {modified_count} features.")
    else:
        print("No 'features' found to modify.")
    print("--- Finished Modifying Data ---")
    return data

def summed_values(data, fieldname):
    """
    Counts occurrences of values in a specified field within the GeoJSON data.
    """
    l = [f['properties'].get(fieldname) for f in data['features']]
    l = [x for x in l if x is not None]
    if not l: return pd.DataFrame(columns=['name', 'n_hp'])
    split_names = [name.strip() for item in l for name in item.split(',') if name.strip()]
    name_counts = Counter(split_names)
    if not name_counts: return pd.DataFrame(columns=['name', 'n_hp'])
    df = pd.DataFrame.from_dict(name_counts, orient='index').reset_index()
    df = df.rename(columns={'index': 'name', 0: 'n_hp'})
    return df.sort_values('n_hp', ascending=False)

def zenodo_contributors(data):
    """
    Generates a list of contributors from the data.
    This function is guaranteed to ONLY use the "Assessment Investigator - Actor" field.
    """
    print("\n--- Calculating Contributors ---")
    fieldname = "Assessment Investigator - Actor"
    print(f"Searching for field: '{fieldname}'")

    if not data.get('features'):
        print("No 'features' found in the dataset. Cannot calculate contributors.")
        return []

    # Extract all non-empty values from the specified field across all features.
    all_values = [
        f['properties'].get(fieldname)
        for f in data['features']
        if f.get('properties') and f['properties'].get(fieldname)
    ]

    if not all_values:
        print(f"Field '{fieldname}' not found or is empty in all features. Using default EAMENA contributors.")
        return [{'name': "University of Oxford", "type": "DataManager"}, {'name': "University of Southampton", "type": "DataManager"}]

    print(f"Found {len(all_values)} records with a value for the '{fieldname}' field.")

    # Process the names: split comma-separated strings and get a unique, sorted list.
    unique_names = sorted(list(set(
        name.strip()
        for item in all_values
        for name in item.split(',')
        if name.strip()
    )))

    print(f"Extracted the following unique contributors: {unique_names}")

    # Format the names for the Zenodo API.
    contributors = [{"name": name, "type": "DataCollector"} for name in unique_names]

    print(f"Formatted {len(contributors)} contributors for Zenodo.")
    print("--- Finished Calculating Contributors ---\n")
    return contributors

def zenodo_keywords(data):
    """
    Generates a list of keywords from the data.
    """
    print("Calculating keywords...")
    constant = ['EAMENA', 'MaREA', 'Cultural Heritage']
    fields = ["Country Type", "Cultural Period Type"]
    keywords = constant[:]
    if data.get('features'):
        for fieldname in fields:
            if any(fieldname in f.get('properties', {}) for f in data['features']):
                df = summed_values(data, fieldname)
                if not df.empty and 'name' in df.columns:
                    keywords.extend(df['name'].tolist())
    keywords = list(set(kw for kw in keywords if kw and kw != 'Unknown'))
    print(f"Generated {len(keywords)} keywords.")
    return keywords

def zenodo_dates(data):
    """
    Determines the date range of the dataset.
    """
    print("Calculating dates...")
    fieldname = "Assessment Activity Date"
    if data.get('features') and any(fieldname in f.get('properties', {}) for f in data['features']):
        ldates = [d for d in summed_values(data, fieldname)['name'].tolist() if d and d != 'None']
        if not ldates:
            print("Date field was found but contained no valid date values. Using default.")
            return [{'type': 'created', 'start': '2021-01-01', 'end': '2021-01-02'}]
        try:
            date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in ldates]
            min_date, max_date = min(date_objects), max(date_objects)
            print(f"Date range found: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
            return [{'type': 'created', 'start': min_date.strftime('%Y-%m-%d'), 'end': max_date.strftime('%Y-%m-%d')}]
        except ValueError:
            print("Warning: Could not parse some dates. Using default.")
    
    print("No 'Assessment Activity Date' field found. Using default dates.")
    return [{'type': 'created', 'start': '2021-01-01', 'end': '2021-01-02'}]
