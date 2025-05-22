import geopandas as gpd
import streamlit as st

from pages import statistics
from pages import search

st.write("Hello World")
search.title()
statistics.title()

source = gpd.read_file("data/100058.csv")
