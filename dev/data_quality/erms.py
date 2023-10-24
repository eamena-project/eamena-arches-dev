import psycopg2 as pg
import pandas as pd
import numpy as np
import re
import requests
import json
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import plotly.express as px

def erms(GEOJSON_URL):
	print(GEOJSON_URL)
