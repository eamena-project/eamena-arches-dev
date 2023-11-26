#%%
import os
import plotly.graph_objects as go
import pandas as pd

dirIn = os.path.dirname(os.path.abspath(__file__))


url = "https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/data/time/sankey/acd_ex1.tsv"

df = pd.read_csv(url, sep='\t')
df['target'] = df['target'] + "_" # to distinguish 'source' and 'target'
# Concatenate 'source' and 'target' columns, get unique values, and convert to a list
labels = pd.concat([df['source'], df['target']]).unique().tolist()

# Create a Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=labels
    ),
    link=dict(
        source=df['source'].map(lambda x: labels.index(x)),
        target=df['target'].map(lambda x: labels.index(x)),
        value=df['value']
    )
)])

# Customize layout
fig.update_layout(title_text="Sankey Diagram", font_size=10)

# Export as HTML
fileOut = dirIn + "/sankey.html" 
fig.write_html(fileOut)

# Show the plot
fig.show()
