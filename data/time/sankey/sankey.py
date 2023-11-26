

#%%
import os

os.getcwd()

#%%
import plotly.graph_objects as go
import pandas as pd

# Your dataframe
data = {'source': ['bare', 'bare', 'bare', 'bare', 'bare', 'mountain', 'mountain', 'mountain', 'mountain', 'mountain',
                   'quarry', 'quarry', 'quarry', 'quarry', 'quarry', 'urban', 'urban', 'urban', 'urban', 'urban',
                   'vegetation', 'vegetation', 'vegetation', 'vegetation', 'vegetation'],
        'target': ['bare', 'mountain', 'quarry', 'urban', 'vegetation', 'bare', 'mountain', 'quarry', 'urban', 'vegetation',
                   'bare', 'mountain', 'quarry', 'urban', 'vegetation', 'bare', 'mountain', 'quarry', 'urban', 'vegetation',
                   'bare', 'mountain', 'quarry', 'urban', 'vegetation'],
        'value': [21, 89, 76, 165, 121, 87, 100, 0, 98, 64, 124, 1, 81, 74, 8, 184, 128, 49, 154, 124, 133, 58, 0, 122, 127]}

df = pd.DataFrame(data)

# Create a Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=['bare', 'mountain', 'quarry', 'urban', 'vegetation']
    ),
    link=dict(
        source=df['source'].map({'bare': 0, 'mountain': 1, 'quarry': 2, 'urban': 3, 'vegetation': 4}),
        target=df['target'].map({'bare': 0, 'mountain': 1, 'quarry': 2, 'urban': 3, 'vegetation': 4}),
        value=df['value']
    )
)])

# Customize layout
fig.update_layout(title_text="Sankey Diagram", font_size=10)
fig.write_html("sankey_diagram.html")

# Show the plot
fig.show()
