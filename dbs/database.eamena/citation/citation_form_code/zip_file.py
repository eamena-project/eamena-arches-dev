import os
import json
import zipfile
import numpy as np

class NpEncoder(json.JSONEncoder):
    """ Custom JSON encoder for NumPy data types. """
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super(NpEncoder, self).default(obj)

def save_zip(data, filename, plot_filenames):
    """Saves data to a GeoJSON file and then creates a ZIP archive."""
    json_file_name = f"{filename}.geojson"
    zip_file_name = f"{filename}.zip"

    try:
        with open(json_file_name, "w") as json_file:
            json.dump(data, json_file, indent=4, cls=NpEncoder)
        print(f"Successfully created GeoJSON file: {json_file_name}")
    except Exception as e:
        print(f"Error creating GeoJSON file: {e}")
        return

    try:
        with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(json_file_name)
            for file_path in plot_filenames:
                if os.path.exists(file_path):
                    zipf.write(file_path)
                else:
                    print(f"Warning: Plot file not found: {file_path}")
        print(f"Successfully created ZIP file: {zip_file_name}")
    except Exception as e:
        print(f"Error creating ZIP file: {e}")

def clean_up_files(filename, plot_filenames):
    """Removes the temporary files created during the process."""
    files_to_remove = [f"{filename}.geojson", f"{filename}.zip"] + plot_filenames
    for f in files_to_remove:
        try:
            if os.path.exists(f):
                os.remove(f)
                print(f"Cleaned up temporary file: {f}")
        except Exception as e:
            print(f"Error cleaning up file {f}: {e}")
