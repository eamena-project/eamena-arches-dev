# Reference Data




## Temp
> To remove

```py
# Create pie chart (already in https://colab.research.google.com/drive/1AykNA2PfOvpitBdHiuQn3nJ04y_QOba)
# data['features'][0]['properties']
GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&term-filter=%5B%7B%22context%22%3A%22%22%2C%22context_label%22%3A%22Heritage%20Place%20-%20Resource%20Name%22%2C%22id%22%3A0%2C%22text%22%3A%22NQT0%22%2C%22type%22%3A%22term%22%2C%22value%22%3A%22NQT0%22%2C%22inverted%22%3Afalse%7D%5D&language=*&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D&total=12"
data = bdata.db_query(geojson_url = GEOJSON_URL)
lconditions = list()
for i in range(len(data['features'])):
  lconditions.append(data['features'][i]['properties']['Overall Condition State Type'])
lconditions = [item for sublist in [x.split(', ') for x in lconditions] for item in sublist]

import matplotlib.pyplot as plt
from collections import Counter

# Count the occurrences of each condition
condition_counts = Counter(lconditions)

# Prepare data for the pie chart
labels = list(condition_counts.keys())
sizes = list(condition_counts.values())
colors = plt.cm.Pastel1(range(len(labels)))  # Using a colormap for the pie chart colors

# Define a function to format the autopct to display counts
def absolute_value(val):
    total = sum(sizes)
    percent = int(round(val/100.*total))
    return f"{percent:d}"

# Create the pie chart
plt.figure(figsize=(8, 8))  # Set the figure size
plt.pie(sizes, labels=labels, autopct=absolute_value, startangle=90, colors=colors)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart
plt.title('Distribution of Conditions')
plt.show()
```

```py
# temp too
GEOJSON_URL = "https://database.eamena.org/api/search/export_results?paging-filter=1&tiles=true&format=geojson&reportlink=false&precision=6&term-filter=%5B%7B%22context%22%3A%22%22%2C%22context_label%22%3A%22Heritage%20Place%20-%20Resource%20Name%22%2C%22id%22%3A0%2C%22text%22%3A%22NQT0%22%2C%22type%22%3A%22term%22%2C%22value%22%3A%22NQT0%22%2C%22inverted%22%3Afalse%7D%5D&language=*&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D&total=12"
data = bdata.db_query(geojson_url = GEOJSON_URL)
field_is = 'Heritage Place Function'
lfunctions = list()
ct = 0
for i in range(len(data['features'])):
  ct = ct + 1
  lfunctions.append(data['features'][i]['properties'][field_is])
# split when there are several values for 1 HP
lfunctions = [item for sublist in [x.split(', ') for x in lfunctions] for item in sublist]
```



```py
# create an histogram
field_is = 'Heritage Place Function'
lfunctions = list()
ct = 0
for i in range(len(data['features'])):
  ct = ct + 1
  lfunctions.append(data['features'][i]['properties'][field_is])
# split when there are several values for 1 HP
lfunctions = [item for sublist in [x.split(', ') for x in lfunctions] for item in sublist]
function_counts = Counter(lfunctions)
sorted_functions = sorted(function_counts.items(), key=lambda x: x[1], reverse=True)
labels, values = zip(*sorted_functions)
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
plt.show()
```