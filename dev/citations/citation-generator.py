import psycopg2 as pg
import pandas as pd
import numpy as np
import re
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import plotly.express as px

# connection parameters
dbname = "eamena"
user = "post"
password = "eamenar"
host = "52.50.27.140"
port = "5432"