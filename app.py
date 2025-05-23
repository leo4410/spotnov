import streamlit as st
from functions import boundingbox
from loaders import overpass
from pages import statistics
from pages import search

st.write("Spotnov")

search.title()
search.search_interface()

if "map_result" in st.session_state:
    gdf = st.session_state["map_result"]

    gdf["lat"] = gdf.geometry.y
    gdf["lon"] = gdf.geometry.x

    st.map(gdf, latitude="lat", longitude="lon")
    
statistics.title()
statistics.example_view()
