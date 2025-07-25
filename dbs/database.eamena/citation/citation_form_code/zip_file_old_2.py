import os
import json
import zipfile
import numpy as np

# needed to export as JSON
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def save_zip(data, filename, plot_filenames):

    # JSON file name and ZIP file
    json_file_name = filename + ".geojson"
    zip_file_name = filename + ".zip"

    # Create the JSON file and write the data to it
    json_string = json.dumps(data, cls=NpEncoder)
    json_string = json.loads(json_string)
    with open(json_file_name, "w") as json_file:
        json.dump(json_string, json_file, indent=4)
        print(json_file_name + " has been exported in " + os.getcwd())

    # Create a ZIP file and add the JSON file to it
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(json_file_name)
        for file_path in plot_filenames:
            zipf.write(file_path)
            print(f"Added {file_path} to {plot_filenames}")
        print(zip_file_name + " has been exported in " + os.getcwd())

def save_zip2(data, filename):
    # Temporary function to avoid the errors created by missing values maiking the map cracshes (ex: Country Type)

    # JSON file name and ZIP file
    json_file_name = filename + ".geojson"
    zip_file_name = filename + ".zip"

    # Create the JSON file and write the data to it
    json_string = json.dumps(data, cls=NpEncoder)
    json_string = json.loads(json_string)
    with open(json_file_name, "w") as json_file:
        json.dump(json_string, json_file, indent=4)
        print(json_file_name + " has been exported in " + os.getcwd())
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(json_file_name)
    print(zip_file_name + " has been exported in " + os.getcwd())
    # # Create a ZIP file and add the JSON file to it
    # with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    #     zipf.write(json_file_name)
    #     for file_path in plot_filenames:
    #         zipf.write(file_path)
    #         print(f"Added {file_path} to {plot_filenames}")
    #     print(zip_file_name + " has been exported in " + os.getcwd())

def clean_up_zip(title):
    json_file_name = title + ".geojson"
    zip_file_name = title + ".zip"
    os.remove(zip_file_name)
    print(zip_file_name + " has been cleaned up in " + os.getcwd())
    os.remove(json_file_name)
    print(json_file_name + " has been cleaned up in " + os.getcwd())
