# New form to publish data to Zenodo
- Added a new page at `/citations/`
- It allows a user to input a:
  -  GeoJSON URL export
  -  Title
  -  Description
<img width="733" alt="image" src="https://github.com/eamena-project/eamena-arches-dev/assets/41572010/8943e20f-9c22-4f94-87a3-c2df8c59d421">

The code uses a Django form to accept values from the user. It takes the GeoJSON url and writes the output to a json file on the server. The title and description are used to populate the `METADATA` object in `zenodo_publish.py`, which is used to the data publish to Zenodo. The code then deletes the json file from the server to save space. 

## TO DO 
We could further integrate the code with Arches by adding an option here to prepopulate the GeoJSON Url option based upon the search results.
<img width="1069" alt="image" src="https://github.com/eamena-project/eamena-arches-dev/assets/41572010/ccc2005f-8867-4638-8996-1f45d97fda9a">
