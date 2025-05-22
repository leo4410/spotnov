import geopandas as gpd
import streamlit as st
import overpy
from shapely.geometry import Point

from loaders import overpass
from pages import statistics
from pages import search


st.write("Spotnov")

search.title()
statistics.title()
statistics.example_view()

gdf = overpass.getFireplaces("""["leisure"="firepit"]""", "(47.268048,7.186775,47.613107,8.115807)")

gdf["lat"] = gdf.geometry.y
gdf["lon"] = gdf.geometry.x

st.map(gdf, latitude="lat", longitude="lon")
