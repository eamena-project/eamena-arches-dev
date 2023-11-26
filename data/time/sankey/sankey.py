#%%
import os
import plotly.graph_objects as go
import pandas as pd

url = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/time/sankey/acd_ex1.tsv"
df = pd.read_csv(url, sep='\t')
df['target'] = df['target'] + "_" # to distinguish 'source' and 'target'


#%%
# Create a Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=['bare', 'mountain', 'quarry', 'urban', 'vegetation', 'bare_', 'mountain_', 'quarry_', 'urban_', 'vegetation_']
    ),
    link=dict(
        source=df['source'].map({'bare': 0, 'mountain': 1, 'quarry': 2, 'urban': 3, 'vegetation': 4}),
        target=df['target'].map({'bare_': 5, 'mountain_': 6, 'quarry_': 7, 'urban_': 8, 'vegetation_': 9}),
        value=df['value']
    )
)])

# Customize layout
fig.update_layout(title_text="Sankey Diagram", font_size=10)

dirIn = os.path.dirname(os.path.realpath(__file__))
fileout = "sankey_diagram.html"
fig.write_html(dirIn + "/" + fileout)

# Show the plot
# fig.show()