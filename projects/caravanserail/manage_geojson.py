def filter_geojson_properties(input_file = None, output_file = None, keep_properties = ['EAMENA ID'], keep_geometries = ['Point']):
    """
    Remove unecessary fields in a GeoJSON file exported from EAMENA
    
    ex: filter_geojson_properties(input_file = 'data/cvn__test.geojson', output_file = 'data/cvn__test_OK2.geojson')
    """
    import json
    import pathlib
    
    dir = pathlib.Path(__file__).parent.resolve()
    input_file = str(dir) + "\\" + input_file
    output_file = str(dir) + "\\" + output_file
    # print(input_file)
    with open(input_file, 'r') as file:
        data = json.load(file)
    filtered_features = []
    for feature in data['features']:
        # Check if the feature's geometry type is in the allowed list
        if feature['geometry']['type'] in keep_geometries:
            # Filter the properties of the feature
            filtered_properties = {key: value for key, value in feature['properties'].items() if key in keep_properties}
            feature['properties'] = filtered_properties
            # Add the filtered feature to the list
            filtered_features.append(feature)
    data['features'] = filtered_features
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


def create_lines(input_file, output_file, max_distance_km=100, verbose=True):
    import geopandas as gpd
    from shapely.geometry import LineString
    import pathlib

    # Load data
    dir = pathlib.Path(__file__).parent.resolve()
    input_file = str(dir) + "\\" + input_file
    output_file = str(dir) + "\\" + output_file
    gdf = gpd.read_file(input_file)
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)  # Assume the input is in WGS 84 if not specified
    gdf = gdf.to_crs(epsg=3395)  # World Mercator for global applicability
    lines = gpd.GeoDataFrame(columns=['geometry', 'EAMENA_ID_from', 'EAMENA_ID_to'], crs=gdf.crs)
    for i, point1 in gdf.iterrows():
        closest_point = None
        min_distance = float('inf')  # Initialize with a very large number
        for j, point2 in gdf.iterrows():
            if i != j:  # Ensure not to calculate distance to itself
                distance = point1.geometry.distance(point2.geometry)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point2
        if min_distance < max_distance_km * 1000:
            print("- attent to create a line from ", point1['EAMENA ID'] + " to " + closest_point['EAMENA ID'])
            try:
                line = LineString([point1.geometry, closest_point.geometry])
                new_line = {
                    'geometry': line,
                    'EAMENA_ID_from': point1['EAMENA ID'],
                    'EAMENA_ID_to': closest_point['EAMENA ID']
                }
                lines = lines._append(new_line, ignore_index=True)
            except:
                print("     > Error")
    lines.set_crs(epsg=3395, inplace=True)
    lines = lines.to_crs(epsg=4326)
    lines.to_file(output_file, driver='GeoJSON')

create_lines(input_file = 'data/cvn__test_OK3.geojson', output_file = 'data/temp_subset_for_auto_lines_LINE4.geojson')
# filter_geojson_properties(input_file = 'cvn__test.geojson', output_file = 'cvn__test_OK3.geojson')