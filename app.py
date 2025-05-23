import streamlit as st
from pages import statistics
from pages import search

st.write("Spotnov")
Logo = "data/Logo.jpg"
st.image(Logo,width=400)
    
### -------------------------
### Start des Abschnitt Suche
### -------------------------
search.title()
search.search_map()
search.search_interface()

if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    gdf = st.session_state["map_result"]
    search.search_result(gdf)

### -----------------------------
### Start des Abschnitt Statistik
### -----------------------------
statistics.title()

### ---------------------------
### Anzahl Feuerstellen in Box
### ---------------------------
if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    gdf = st.session_state["map_result"]
    statistics.markerCountWidget(gdf)

### ---------------------------
### Anzahl Feuerstellen in Box
### ---------------------------
if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    gdf = st.session_state["map_result"]
    bounding_box = st.session_state["bounding_box"]
    statistics.markerDensityWidget(gdf, bounding_box)

### ---------------------------------
### Distanz zur nächsten Feuerstellen
### ---------------------------------
if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    gdf = st.session_state["map_result"]
    bounding_box = st.session_state["bounding_box"]
    statistics.markerDistanceWidget(gdf, bounding_box)


if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    
    gdf = st.session_state["map_result"]
    location_coords = st.session_state["location_coords"]
    search_radius = st.session_state["search_radius"]
    bounding_box = st.session_state["bounding_box"]
    gdf = statistics.markerShortestDistanceWidget(gdf, location_coords, search_radius, bounding_box)
