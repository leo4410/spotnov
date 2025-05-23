import streamlit as st

from functions import boundingbox
from functions.anzahl_fireplace import count_fireplaces_in_bbox
from functions.dichte_anzahl_fireplace import density_fireplaces_in_bbox
from loaders import overpass
from pages import statistics
from pages import search
from streamlit_folium import st_folium
from functions.nearest_fireplace import create_fireplace_map

st.write("Spotnov")

search.title()
search.search_interface()

if "map_result" in st.session_state:
    gdf = st.session_state["map_result"]

    gdf["lat"] = gdf.geometry.y
    gdf["lon"] = gdf.geometry.x

    st.map(gdf, latitude="lat", longitude="lon")

statistics.title()

bb = boundingbox.calcBoundingBox("Gelterkinden",4)

gdf = overpass.getMarkers(['["leisure"="firepit"]'], bb)

gdf["lat"] = gdf.geometry.y
gdf["lon"] = gdf.geometry.x

st.map(gdf, latitude="lat", longitude="lon")

#anzahl_fireplace

# alle Feuerstellen in dieser Box abfragen und zählen
anzahl = count_fireplaces_in_bbox(bb)

# Ergebnis anzeigen
st.write(f"Anzahl Feuerstellen in der Box: **{anzahl}**")

#dichte_anzahl_fireplace

# Dichte berechnen
density = density_fireplaces_in_bbox(bb)

# Ergebnis anzeigen
st.write(f"Dichte der Feuerstellen: **{density:.2f}%**")

#nearest Fireplace

# Karte und Distanz holen
#res = create_fireplace_map(bb)
#if res is None:
    #st.warning("Keine Feuerstellen in dieser Box gefunden.")
#else:
    #m, dist_km = res
    #t.write(f"Distanz zur nächsten Feuerstelle: **{dist_km:.2f} km**")
    #st_folium(m, width=700, height=500)

# Nächste Feuerstelle + Folium-Karte
res = create_fireplace_map(bb)
if res is None:
    st.warning("Keine Feuerstellen in dieser Bounding-Box gefunden.")
else:
    m, dist_km = res
    st.write(f"Distanz zur nächsten Feuerstelle: **{dist_km:.2f} km**")
    #st_folium(m, width=700, height=500)
    #import uuid
    #st_folium(m, width=700, height=500, key=str(uuid.uuid4()))
    st_folium(m, width=700, height=500, key="nearest_fireplace_map")


if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:

    gdf = st.session_state["map_result"]
    location_coords = st.session_state["location_coords"]
    search_radius = st.session_state["search_radius"]
    bounding_box = st.session_state["bounding_box"]
    gdf = statistics.nearest_place(gdf, location_coords, search_radius, bounding_box)
