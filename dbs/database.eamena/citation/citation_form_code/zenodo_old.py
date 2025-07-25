
#%% test

def summed_values(data = None, fieldname = None):
    """
    Creates a dataframe summing the number of occurences for a given field
    
    ::param data: dictionary of Heritage Places (JSON)
    """
    import pandas as pd
    from collections import Counter

    l = list()
    for i in range(len(data['features'])):
        l.append(data['features'][i]['properties'][fieldname])
    split_names = [name.strip() for item in l if item is not None for name in item.split(',')]
    name_counts = Counter(split_names)
    df = pd.DataFrame.from_dict(name_counts, orient='index').reset_index()
    df = df.rename(columns={'index': 'name', 0: 'n_hp'})
    df = df.sort_values('n_hp', ascending=False)
    return df

def zenodo_contributors(data = None, fieldname = "Assessment Investigator - Actor", 
                        contributors_layout_HP = {"name": None, "type": "DataCollector"}, contributors_layout_GS = [{'name': "University of Oxford", "type": "DataManager"},{'name': "University of Southampton", "type": "DataManager"}]):
    """
    Creates dictionary of contributors, filling a dictionary layout (`contributors_layout_*`). Contributors are sorted according to the total number of their name occurences in the selected `fieldname`.
    
    :param data: dictionary of Heritage Places (JSON)
    """
    if fieldname in list(data['features'][0]['properties'].keys()):
    # HPs
        df = summed_values(data, fieldname)
        CONTRIBUTORS = list()
        for name in df['name']:
            contibut = contributors_layout_HP.copy()
            contibut['name'] = name
            # TODO: "affiliation" and "orcid"
            contibut = {key: value for key, value in contibut.items() if value is not None and value != 'null'}
            CONTRIBUTORS.append(contibut)
    else:
    # not HPs (GS, ...)
        CONTRIBUTORS = contributors_layout_GS
    return CONTRIBUTORS

def zenodo_keywords(data = None, constant = ['EAMENA', 'MaREA', 'Cultural Heritage'], additional = None, fields = ["Country Type", "Cultural Period Type"]):
    """
    Creates a list of keywords with a constant basis (`constant`) and parsed supplementary `fields` (for space-time keywords)
    
    :param data: dictionary of Heritage Places (JSON)
    :param additional: additional keyworks provided by the user
    """
    KEYWORDS = list()
    KEYWORDS = KEYWORDS + constant + additional
    if all(elem in list(data['features'][0]['properties'].keys()) for elem in fields):
    # HPs
        for fieldname in fields:
            df = summed_values(data, fieldname)
            KEYWORDS = KEYWORDS + df['name'].tolist()
        try:
            KEYWORDS.remove('Unknown')
        except ValueError:
            pass
    return KEYWORDS

def zenodo_dates(data = None, fields = ["Assessment Activity Date"]):
    """
    Get the min and the max of dates recorded in `fields`    

    :param data: dictionary of Heritage Places (JSON)
    """
    from datetime import datetime

    if all(elem in list(data['features'][0]['properties'].keys()) for elem in fields):
    # HPs
        ldates = list()
        for fieldname in fields:
            df = summed_values(data, fieldname)
            ldates = ldates + df['name'].tolist() 
        if 'None' in ldates:
            ldates.remove('None')
        # ldates.remove('None')
        # date_strings = [x for x in date_strings if x is not 'None']
        date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in ldates]
        min_date = min(date_objects)
        max_date = max(date_objects)
        min_date_str = min_date.strftime('%Y-%m-%d')
        max_date_str = max_date.strftime('%Y-%m-%d')
        DATES = [{'type': 'created', 'start': min_date_str, 'end': max_date_str}]
        return DATES
    else:
    # not HPs (GS, ...)
        DATES = [{'type': 'created', 'start': '2021-01-01', 'end': '2021-01-02'}]
        return DATES

def zenodo_related_identifiers(site = 'https://zenodo.org/oai2d', set = 'user-eamena', metadataPrefix = 'oai_dc', reference_data_list = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/lod/zenodo/reference_data_list.tsv"):
    """
    Parse the 'EAMENA database' community in Zenodo ('user-eamena') to check if there are already uploaded datasets. Handle differently the reference data (collections, RMs, ...) and the datasets (Sistan part 1, etc.), or business data. Reference data are 'isDescribedBy' related identifiers, whereas the datasets are 'isContinuedBy' related resources.

    :param reference_data_list: the list of reference data already existing in the 'eamena' Zenodo community. These objects will not be added as 'isContinuedBy' in the metadata key 'related_identifiers' but as 'isDescribedBy'
    """
    import pandas as pd
    from sickle import Sickle

    # reference_data_list = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/lod/zenodo/reference_data_list.tsv"
    reference_data = pd.read_csv (reference_data_list, sep = '\t')
    l_isDescribedBy = reference_data['url'].tolist()

    sickle = Sickle(site)
    records = sickle.ListRecords(metadataPrefix=metadataPrefix, set=set)
    # record = records.next()
    # return record.metadata['identifier'][0]# record = records.next()
    l = list()
    for record in records:
        l.append(record.metadata['identifier'][0])
    # rm the reference data
    l_isContinuedBy = [x for x in l if x not in l_isDescribedBy]
    ## create the record
    # business data
    l_isContinuedBy_out = list()
    for busdata in l_isContinuedBy:
        l_isContinuedBy_out.append({'relation': 'isContinuedBy',
                                    'identifier': busdata})
    # reference data
    l_isDescribedBy_out = list()   
    for refdata in l_isDescribedBy:
        l_isDescribedBy_out.append({'relation': 'isDescribedBy',
                                    'identifier': refdata})
    # merge lists
    l_related_identifiers = l_isContinuedBy + l_isDescribedBy_out
    return(l_related_identifiers)

def zenodo_statistics(data = None):
    """
    Calculate basic statistics on HPs.

    :param data: dictionary of Heritage Places (JSON)

    :return: A list with: the total number of Heritage Places; the number of Heritage Places layered by number of geometries (some have 1, 2, 3, ...); the total number of geometries; etc.

    """
    from collections import Counter

    l = list()
    LIST_HPS = list()
    for i in range(len(data['features'])):
        ea_id = data['features'][i]['properties']['EAMENA ID']
        l.append(ea_id)
    my_dict = {i:l.count(i) for i in l}
    value_counts = Counter(my_dict.values())
    HPS_GEOM_NB = dict(value_counts)
    HPS_NB = sum(HPS_GEOM_NB.values())   
    LIST_HPS.append(HPS_NB)
    LIST_HPS.append(HPS_GEOM_NB)
    HPS_GEOM_NB_TOTAL = {key: key * value for key, value in HPS_GEOM_NB.items()}
    HPS_GEOM_NB_TOTAL = sum(HPS_GEOM_NB_TOTAL.values())
    LIST_HPS.append(HPS_GEOM_NB_TOTAL)
    return(LIST_HPS)

def duplicate_remove(data = None, field_id = 'EAMENA ID'):
    """
    Remove duplicates on a specific field. Indeed, HP having more than one geometry (ex: Point and Polygon) will be duplicated.

    :param data: dictionary of Heritage Places (JSON)
    :param field_id: the field on which the duplicated will be counted, default 'EAMENA ID' (HP)

    :return: A dictionnary of features (only)

    :Example:
    >>> data_points['features'] = duplicate_remove(data_points)
    """
    seen_eamena_ids = set()
    filtered_features = []
    for feature in data['features']:
        eamena_id = feature['properties'].get(field_id)
        if eamena_id not in seen_eamena_ids:
            filtered_features.append(feature)
            seen_eamena_ids.add(eamena_id)
    return(filtered_features)

def geometry_types(data = None):
    """
    List all geometry types coming of an HP dataset.

    :param data: dictionary of Heritage Places (JSON)

    :return: Existing geometries (Points, LineStrings, etc.) in a list
    """
    unique_geometry_types = set()
    for feature in data['features']:
        geometry_type = feature['geometry']['type']
        unique_geometry_types.add(geometry_type)
    unique_geometry_types = sorted(unique_geometry_types)
    return(unique_geometry_types)

def geometry_to_centroid(data = None):
    """
    Converts Polygon, Line and Multi geometries to Point geometries.

    :param data: dictionary of Heritage Places (JSON)

    :return: A dictionary of Heritage Places (JSON) with only Point geometries.
    
    :Example:
    >>> data_points = geometry_to_centroid(data_points)
    """
    from shapely.geometry import shape

    for feature in data['features']:
        geometry = feature['geometry']
        geom = shape(geometry)
        if geom.geom_type in ['Polygon', 'LineString', 'MultiLineString', 'MultiPolygon', 'MultiPoint']:
            centroid = geom.centroid  # Get the centroid
            feature['geometry'] = {
                'type': 'Point',
                'coordinates': (centroid.x, centroid.y)
            }
    return data

def zenodo_statistics_hp(filename= "", data = None, stats = ['pie_on_conditions', 'hist_on_functions']):
    """
    Create a various plots and charts on HPs values.

    :param data: dictionary of Heritage Places (JSON)
    :param stats: the different charts that will be created: 'pie_on_conditions' stands for 'Overall Condition State Type', 'hist_on_functions' stands for .... For example stats = ['pie_on_conditions', 'hist_on_functions']

    :return: Charts
    """
    import matplotlib.pyplot as plt
    from collections import Counter
    import matplotlib
    matplotlib.use('Agg')

      # avoid duplicated geometries
    data['features'] = duplicate_remove(data)

    if('pie_on_conditions' in stats):
        field_is = 'Overall Condition State Type'
        lconditions = list()
        ct = 0
        for i in range(len(data['features'])):
            ct = ct + 1
            lconditions.append(data['features'][i]['properties'][field_is])
        # split when there are several values for 1 HP
        # Check if the value is not None before calling split
        # if lconditions is not None:
        if len(lconditions) > 0:
            try:
                lconditions = [item for sublist in [x.split(', ') for x in lconditions] for item in sublist]
                condition_counts = Counter(lconditions)
                labels = list(condition_counts.keys())
                sizes = list(condition_counts.values())
                colors = plt.cm.Pastel1(range(len(labels)))  # Using a colormap for the pie chart colors
                def absolute_value(val):
                    total = sum(sizes)
                    percent = int(round(val/100.*total))
                    return f"{percent:d}"
                plt.figure(figsize=(5, 5)) 
                plt.pie(sizes, labels=labels, autopct=absolute_value, startangle=90, colors=colors)
                plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                plt.title(f"Distribution of {ct} Heritage Places' {field_is}")
                plt.savefig(f"{filename}_stat_hp_conditions.png", dpi=300)
            except:
                pass

    if('hist_on_functions' in stats):
        field_is = 'Heritage Place Function'
        lfunctions = list()
        ct = 0
        for i in range(len(data['features'])):
            ct = ct + 1
            lfunctions.append(data['features'][i]['properties'][field_is])
        # split when there are several values for 1 HP
        if lfunctions is not None:
            lfunctions = [item for sublist in [x.split(', ') for x in lfunctions] for item in sublist]
            function_counts = Counter(lfunctions)
            sorted_functions = sorted(function_counts.items(), key=lambda x: x[1], reverse=True)
            labels, values = zip(*sorted_functions)
            # chart size depends on nb of values
            if len(labels) < 6:
                width,height = (5, 6)
            elif len(labels) > 6 and len(labels) < 12:
                width,height = (10, 6)
            else:
                width,height = (15, 6)
            plt.figure(figsize=(width,height))
            plt.bar(labels, values, color='skyblue')
            plt.xlabel(field_is)
            plt.ylabel('Counts')
            plt.title(f"Distribution of {ct} Heritage Places' {field_is}")
            plt.xticks(rotation=45)
            plt.savefig(f"{filename}_stat_hp_functions.png", dpi=300)

def zenodo_map(filename = "",data = None, levels = [1, 2, 3], country_base_url = "https://raw.githubusercontent.com/eamena-project/eamena-data/main/reference_data/countries/", grid_contour_url = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/data/reference_data/grids/EAMENA_Grid_contour.geojson", label='Heritage Places', edgecolor='black', linewidth=1, fig_size_width=10, fig_size_height=10):
  """
  Create a distribution maps of HPs at different levels: extent of the HPs (local), HPs within their national boundaries (national), HPs within the EAMENA geographical extent. Previously, remove duplicated geometries.

  :param data: dictionary of Heritage Places (JSON)
  :param levels: the different scale on which the maps will be created. 1: local, HP locations within their minimum bound rectangle; 2: national, HP locations within the countr-y-ies; 3: HP locations within the EAMENA project geographic scope
  :param country_base_url: the root path of the folder hosting EAMENA's countries GeoJSON files, for example: Egypt = "https://raw.githubusercontent.com/eamena-project/eamena-data/main/reference_data/countries/Egypt.geojson"
  :param grid_contour_url: The contour of the geographical scope of EAMENA

  :return: A simple distribution map
  """
  import matplotlib
  import geopandas as gpd
  import matplotlib.pyplot as plt
  import contextily as ctx
  import pyproj
  from matplotlib_scalebar.scalebar import ScaleBar
  matplotlib.use('Agg')

  # avoid duplicated geometries
  data_points = geometry_to_centroid(data)
  data_points['features'] = duplicate_remove(data_points)

  gdf = gpd.GeoDataFrame.from_features(data_points['features']) # to df
  gdf = gdf.set_crs('epsg:4326')
  gdf = gdf.to_crs(epsg=3857)

  for level in levels:
    if level == 1:
      fig, ax = plt.subplots(figsize=(fig_size_width, fig_size_height))	
      gdf.plot(ax=ax, alpha=0.5, edgecolor='k', label=label) # Plot the data points
      # Calculate the extent (bounding box) of the points
      xmin, ymin, xmax, ymax = gdf.total_bounds
      x_buffer = (xmax - xmin) * 0.10 # 10% buffer of the X and Y range
      y_buffer = (ymax - ymin) * 0.10
      xlim = (xmin - x_buffer, xmax + x_buffer)
      ylim = (ymin - y_buffer, ymax + y_buffer)
      ax.set_xlim(xlim)
      ax.set_ylim(ylim)
      ctx.add_basemap(ax, source=ctx.providers.Esri.WorldTopoMap)

      transformer = pyproj.Transformer.from_crs(3857, 4326, always_xy=True)
      ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{transformer.transform(x, 0)[0]:.2f}°'))  # For longitude
      ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'{transformer.transform(0, y)[1]:.2f}°'))  # For latitude
      ax.tick_params(axis='both', which='major', labelsize=10)
      scalebar = ScaleBar(dx=1, units="m", dimension="si-length", location="lower right", scale_loc="bottom")
      ax.add_artist(scalebar)
      ax.annotate('N', xy=(0.95, 0.95), xytext=(0.95, 0.9),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=10),
                ha='center', va='center', fontsize=20, xycoords='axes fraction')
      plt.title(f"Distribution map of {len(gdf)} Heritage Places", fontsize=14)
      plt.legend()
      plt.savefig(f"{filename}_map_local.png")

    if level == 2:
      fig, ax = plt.subplots(figsize=(fig_size_width, fig_size_height))	
      gdf.plot(ax=ax, alpha=0.5, edgecolor='k', label=label) # Plot the data points
      lcountries = set()
      # Possible error on the Country names, a try is needed until a better solution
      try:
        for i in range(len(data['features'])):
            lcountries.add(data['features'][i]['properties']['Country Type'])
        for country in lcountries:
            country_url = country_base_url + country + ".geojson"      
            gdf_country = gpd.read_file(country_url)  # Load the country GeoJSON
            gdf_country = gdf_country.set_crs('epsg:4326').to_crs(epsg=3857) 
            gdf_country.plot(ax=ax, color='none', edgecolor=edgecolor, linewidth=linewidth, label=country)
        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldTopoMap)

        transformer = pyproj.Transformer.from_crs(3857, 4326, always_xy=True)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{transformer.transform(x, 0)[0]:.2f}°'))  # For longitude
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'{transformer.transform(0, y)[1]:.2f}°'))  # For latitude
        ax.tick_params(axis='both', which='major', labelsize=10)
        scalebar = ScaleBar(dx=1, units="m", dimension="si-length", location="lower right", scale_loc="bottom")
        ax.add_artist(scalebar)
        ax.annotate('N', xy=(0.95, 0.95), xytext=(0.95, 0.9),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=10),
                    ha='center', va='center', fontsize=20, xycoords='axes fraction')
        plt.title(f"Distribution map of {len(gdf)} Heritage Places (national boundaries)", fontsize=14)
        plt.legend()
        plt.savefig(f"{filename}_map_national.png")
      except:
        pass

    if level == 3:
      fig, ax = plt.subplots(figsize=(fig_size_width, fig_size_height))
      gdf.plot(ax=ax, alpha=0.5, edgecolor='k', label=label) # Plot the data points
      # Load the EAMENA grid contour
      gdf_grid = gpd.read_file(grid_contour_url)  # Load the GeoJSON as a GeoDataFrame
      gdf_grid = gdf_grid.set_crs('epsg:4326').to_crs(epsg=3857)  # Ensure the same CRS
      gdf_grid.plot(ax=ax, color='none', edgecolor=edgecolor, linewidth=linewidth, label='Grid Contour')  # Adjust color and style as needed
          # Add a basemap
      ctx.add_basemap(ax, source=ctx.providers.Esri.WorldTopoMap)

      transformer = pyproj.Transformer.from_crs(3857, 4326, always_xy=True)
      ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{transformer.transform(x, 0)[0]:.2f}°'))  # For longitude
      ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'{transformer.transform(0, y)[1]:.2f}°'))  # For latitude
      ax.tick_params(axis='both', which='major', labelsize=10)
      scalebar = ScaleBar(dx=1, units="m", dimension="si-length", location="lower right", scale_loc="bottom")
      ax.add_artist(scalebar)
      ax.annotate('N', xy=(0.95, 0.95), xytext=(0.95, 0.9),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=10),
                ha='center', va='center', fontsize=20, xycoords='axes fraction')
      plt.title(f"Distribution map of {len(gdf)} Heritage Places (EAMENA geographic scope)", fontsize=14)
      plt.legend()
      plt.savefig(f"{filename}_map_eamena_scope.png", dpi=300)


# # %%

# zenodo_statistics(data)

# # zenodo_contributors(data)
# # zenodo_keywords(data)
# # zenodo_dates(data)
# # # %%

# # %%

# %%

# zenodo_related_identifiers()
# %%

def zenodo_read(file_url = "https://zenodo.org/records/10375902/files/sistan_part1_hps.zip?download=1", file_extension='.geojson', output_directory='extracted_files', verbose=True):
    """
    Read Zenodo files (GeoJSON files, zipped or not), returns a geopandas dataframe.

    :param file_url: the Zenodo URL of the download
    :param file_extension: the file extension of the file to download (default: '.geojson')
    :param output_directory: the output directory 

    >>> geojson_data = zenodo_read(file_url = "https://zenodo.org/records/10375902/files/sistan_part1_hps.zip?download=1")
    >>> geojson_data = zenodo_read(file_url="https://zenodo.org/records/13329575/files/EAMENA_Grid_contour.geojson?download=1")
    """
    import os
    import wget
    import zipfile
    import geopandas as gpd

    output_file = wget.download(file_url)
    if verbose:
        print(f"Downloaded file: {output_file}")
    if zipfile.is_zipfile(output_file):
        if verbose:
            print(f"Try to read a ZIP file")
        # Path to the downloaded ZIP file
        zip_file_path = output_file # 'downloaded_file.zip'  # Replace with the actual path to your ZIP file

        # Directory to extract the GeoJSON file
        # output_directory = 'extracted_files'
        # TODO: replace this by a temp file
        os.makedirs(output_directory, exist_ok=True)

        # Open the ZIP file
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            # List the contents of the ZIP file
            zip_contents = zf.namelist()
            
            # Find the GeoJSON file
            geojson_file = next((f for f in zip_contents if f.lower().endswith(file_extension)), None)
            
            if geojson_file:
                # Extract only the GeoJSON file to the output directory
                zf.extract(geojson_file, output_directory)
                geojson_data = os.path.join(output_directory, geojson_file)
                if verbose:
                    print(f"Extracted GeoJSON file to: {geojson_data}")
            else:
                if verbose:
                    print("No GeoJSON file found in the ZIP archive.")
            # Load the GeoJSON file
    if not zipfile.is_zipfile(output_file):
        if verbose:
            print(f"Try to read a GeoJSON file")
        # TODO: test if GeoJSON
        geojson_data = output_file
    gdf = gpd.read_file(geojson_data)
    return gdf
    # Extract the first feature as a GeoDataFrame
    # first_feature_gdf = gdf.iloc[[0]]  # iloc[0] gets the first feature; using [[0]] preserves it as a GeoDataFrame

def zenodo_read_metadata(zenodo_oai = 'https://zenodo.org/oai2d', metadataPrefix='oai_dc', zenodo_community='user-eamena', verbose=True):
    """
    Read Zenodo metadata from a community, returns a geopandas dataframe.

    :param zenodo_oai: the URL of the Zenodo OAI API
    :param metadataPrefix: the Zenodo metadata prefix
    :param zenodo_community: the Zenodo community

    >>> zenodo_read_metadata()
    """
    import sickle
    from sickle import Sickle
    import pandas as pd

    sickle = Sickle(zenodo_oai)
    records = sickle.ListRecords(metadataPrefix=metadataPrefix, set=zenodo_community)

    data = []
    for record in records:
        metadata = record.metadata
        title = metadata.get('title', ['No Title'])[0]
        # collectors = metadata.get('creator', ['Unknown'])
        collectors = metadata.get('contributor')
        # badges = metadata.get('badge', ['No Badges'])
        doi = metadata.get('identifier')

        data.append({
            'Title': title,
            'Data Collector': collectors,
            'Doi': doi[0]
        })
        # Safety break to avoid too long loops during testing
        # Remove or modify this based on actual needs
        if len(data) > 20:
            break
    df = pd.DataFrame(data)
    df.sort_values(by='Title', ascending=False)
    return df

def zenodo_folium(gdf = None, zoom_start=12):
    """
    Plot a geopandas on a folium map.

    :param gdf: a geopandas dataframe, maybe heritated form the zenodo_read() function
    :param zoom_start: starting zoom. Default 12. 
    """
    import folium

    # Get the centroid and center the map
    centroid = gdf.geometry.centroid.iloc[0]
    map_center = [centroid.y, centroid.x]
    my_map = folium.Map(location=map_center, zoom_start=zoom_start)

    folium.GeoJson(gdf.__geo_interface__).add_to(my_map)
    return my_map

def zenodo_folium_by_HP(gdf = None, id_field = 'EAMENA ID', zoom_start=12):
    """
    Create an interactive folium map for a Jupyter NB, allowing a user to select an HP and having a zoom in (NOT WORKING)

    :param gdf: a geopandas dataframe, maybe heritated form the zenodo_read() function
    :param id_field: the selection will be on this field.
    :param zoom_start: starting zoom. Default 12. 
    """
    import ipywidgets as widgets
    from IPython.display import display
    import folium

    # Create a list of unique EAMENA IDs
    eamena_ids = gdf[id_field].unique()

    # Create a dropdown widget
    dropdown = widgets.Dropdown(
        options=eamena_ids,
        description=f'{id_field}:',
        value=eamena_ids[0],  # Default selection is the first option
        style={'description_width': 'initial'}
    )

    # Function to update the map based on the selected ID
    def update_map(eamena_id):
        # Filter GeoDataFrame for the selected EAMENA ID
        selected_feature_gdf = gdf[gdf[id_field] == eamena_id]

        # Get the centroid of the selected feature
        centroid = selected_feature_gdf.geometry.centroid.iloc[0]
        map_center = [centroid.y, centroid.x]

        # Create a folium map centered at the centroid of the selected feature
        my_map = folium.Map(location=map_center, zoom_start=zoom_start)

        # Add the selected feature to the map using GeoJSON
        folium.GeoJson(selected_feature_gdf.__geo_interface__).add_to(my_map)

        display(my_map)

    # Observe changes in the dropdown selection and update the map
    def on_dropdown_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            update_map(change['new'])

    dropdown.observe(on_dropdown_change)

    # Display the dropdown and an initial map
    display(dropdown)
    update_map(eamena_ids[100])  # Initial map with the first ID
