import streamlit as st
from functions import boundingbox

from loaders import overpass
from pages import statistics
from pages import search


st.write("Spotnov")

search.title()
search.search_interface()

statistics.title()
statistics.example_view()

bb = boundingbox.calcBoundingBox("Basel",30)

gdf = overpass.getFireplaces("""["leisure"="firepit"]""", bb)

gdf["lat"] = gdf.geometry.y
gdf["lon"] = gdf.geometry.x

st.map(gdf, latitude="lat", longitude="lon")
