# This file contains the plotting and mapping functions, updated with robust checks.
import matplotlib
matplotlib.use('Agg') # Use a non-interactive backend for Django
import matplotlib.pyplot as plt
from collections import Counter
import geopandas as gpd
import contextily as ctx
from shapely.geometry import shape
from .zenodo_calculate import duplicate_remove

def geometry_to_centroid(data):
    if 'features' not in data: return data
    for feature in data['features']:
        try:
            geom = shape(feature['geometry'])
            centroid = geom.centroid
            feature['geometry'] = {'type': 'Point', 'coordinates': (centroid.x, centroid.y)}
        except Exception: continue
    return data

def zenodo_statistics_hp(filename, data):
    print("Generating statistical plots...")
    data_copy = data.copy()
    data_copy['features'] = duplicate_remove(data_copy)
    if not data_copy.get('features'):
        print("No features to generate statistics for.")
        return

    field_condition = 'Overall Condition State Type'
    if any(field_condition in f.get('properties', {}) for f in data_copy['features']):
        try:
            conditions = [c for f in data_copy['features'] if (c := f['properties'].get(field_condition))]
            if conditions:
                counts = Counter(item.strip() for sublist in [c.split(',') for c in conditions] for item in sublist)
                plt.figure(figsize=(8, 8))
                plt.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%', startangle=90)
                plt.title(f"Distribution of Heritage Places' {field_condition}")
                plt.axis('equal')
                plot_filename = f"{filename}_stat_hp_conditions.png"
                plt.savefig(plot_filename, dpi=300)
                plt.close()
                print(f"Saved condition plot: {plot_filename}")
        except Exception as e: print(f"Error generating condition plot: {e}")
    else:
        print(f"Skipping statistics: '{field_condition}' not found in any features.")

    field_function = 'Heritage Place Function'
    if any(field_function in f.get('properties', {}) for f in data_copy['features']):
        try:
            functions = [func for feat in data_copy['features'] if (func := feat['properties'].get(field_function))]
            if functions:
                counts = Counter(item.strip() for sublist in [f.split(',') for f in functions] for item in sublist)
                labels, values = zip(*sorted(counts.items(), key=lambda x: x[1], reverse=True))
                plt.figure(figsize=(12, 8))
                plt.bar(labels, values, color='skyblue')
                plt.ylabel('Counts')
                plt.title(f"Distribution of Heritage Places' {field_function}")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plot_filename = f"{filename}_stat_hp_functions.png"
                plt.savefig(plot_filename, dpi=300)
                plt.close()
                print(f"Saved function plot: {plot_filename}")
        except Exception as e: print(f"Error generating function plot: {e}")
    else:
        print(f"Skipping statistics: '{field_function}' not found in any features.")

def zenodo_map(filename, data):
    print("Generating distribution maps...")
    if not data.get('features'):
        print("No features to map.")
        return
    try:
        gdf = gpd.GeoDataFrame.from_features(geometry_to_centroid(duplicate_remove(data.copy()))['features'], crs='epsg:4326').to_crs(epsg=3857)
    except Exception as e:
        print(f"Error preparing GeoDataFrame for maps: {e}")
        return

    for level in [1, 2, 3]:
        try:
            fig, ax = plt.subplots(figsize=(10, 10))
            gdf.plot(ax=ax, alpha=0.6, edgecolor='k', label='Heritage Places', markersize=20)
            title, plot_filename = "Distribution Map", f"{filename}_map_level_{level}.png"
            if level == 1:
                title, plot_filename = "Local Distribution", f"{filename}_map_local.png"
                xmin, ymin, xmax, ymax = gdf.total_bounds
                ax.set_xlim(xmin - (xmax-xmin)*0.1, xmax + (xmax-xmin)*0.1)
                ax.set_ylim(ymin - (ymax-ymin)*0.1, ymax + (ymax-ymin)*0.1)
            elif level == 2:
                if any('Country Type' in f.get('properties', {}) for f in data['features']):
                    title, plot_filename = "National Distribution", f"{filename}_map_national.png"
                    countries = {c.replace("Palestine, State of", "Palestine").replace("Iran (Islamic Republic of)", "Iran") for f in data['features'] if (c := f['properties'].get('Country Type','').split(',')[0].strip())}
                    for country in countries:
                        try:
                            gpd.read_file(f"https://raw.githubusercontent.com/eamena-project/eamena-data/main/reference_data/countries/{country}.geojson").to_crs(epsg=3857).plot(ax=ax, color='none', edgecolor='red', linewidth=1.5, label=country)
                        except Exception as e: print(f"Could not load boundary for {country}: {e}")
                else:
                    print("Skipping national map: 'Country Type' not found in any features.")
                    plt.close(fig)
                    continue
            elif level == 3:
                title, plot_filename = "EAMENA Scope Distribution", f"{filename}_map_eamena_scope.png"
                try:
                    gpd.read_file("https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/dbs/database.eamena/data/reference_data/grids/EAMENA_Grid_contour.geojson").to_crs(epsg=3857).plot(ax=ax, color='none', edgecolor='blue', linewidth=1.5, label='EAMENA Grid')
                except Exception as e: print(f"Could not load EAMENA grid contour: {e}")
            
            ctx.add_basemap(ax, source=ctx.providers.Esri.WorldTopoMap, zoom=10)
            ax.set_title(f"{title} of {len(gdf)} Heritage Places", fontsize=14)
            ax.legend()
            plt.tight_layout()
            plt.savefig(plot_filename, dpi=300)
            plt.close(fig)
            print(f"Saved map: {plot_filename}")
        except Exception as e: print(f"Error generating map for level {level}: {e}")
