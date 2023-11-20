import pandas as pd
from pyproj import Proj, transform

# Sample dataframe
data = {
    'pt': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12'],
    'x': [303536.3, 303523.3, 303505.3, 303409.4, 303509.4, 303520.8, 303535.9, 303546.5, 303606.2, 303624.8, 303606.7, 303552],
    'y': [611956.1, 611934.3, 611932.1, 611904.7, 611904.7, 611902, 611905.4, 611912.1, 611915.1, 611933.1, 612003.4, 612013.1]
}

df = pd.DataFrame(data)

# Define the original coordinate reference system (UTM Zone 41R)
original_crs = Proj(init='epsg:32641')

# Define the target coordinate reference system (WGS84)
target_crs = Proj(init='epsg:4326')

# Convert coordinates to WGS84
df['lon'], df['lat'] = transform(original_crs, target_crs, df['x'].values, df['y'].values)

# Display the converted dataframe
print(df[['pt', 'lat', 'lon']])
