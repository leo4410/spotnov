import streamlit as st
from functions import analysis, boundingbox
from loaders import overpass
from pages import statistics
from pages import search
from streamlit_folium import st_folium
from functions.nearest_fireplace import create_fireplace_map

st.write("Spotnov")
Logo = "data/Logo.jpg"
st.image(Logo,width=400)
    
search.title()
search.search_map()
search.search_interface()

if "map_result" in st.session_state:
    gdf = st.session_state["map_result"]

    gdf["lat"] = gdf.geometry.y
    gdf["lon"] = gdf.geometry.x

    st.write()
    #st.dataframe(gdf)

    import pydeck as pdk

    # Farbe nach Typ definieren (falls nicht vorhanden: grau)
    color_map = {
        "firepit": [0, 255, 255],
        "bench": [255, 255, 0],
        "pitch": [180, 0, 0],
        None: [128, 128, 128]
    }
    gdf["color"] = gdf.get("typ", None).apply(lambda x: color_map.get(x, [128, 128, 128]))
    gdf["name"] = gdf.get("name", None)

    # Pydeck Layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=gdf,
        get_position='[lon, lat]',
        get_fill_color="color",
        get_radius=70,
        pickable=True
    )

    # View und Tooltip
    view_state = pdk.ViewState(
        latitude=gdf["lat"].mean(),
        longitude=gdf["lon"].mean(),
        zoom=13
    )

    tooltip = {
        "html": "<b>Typ:</b> {typ}<br><b>Name:</b> {name}<br><b>ID:</b> {id}",
        "style": {"backgroundColor": "white", "color": "black"}
    }   

    # Karte anzeigen mit Hover
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    ))

statistics.title()

### ---------------------------
### Anzahl Feuerstellen in Box
### ---------------------------
if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    
    gdf = st.session_state["map_result"]
    location_coords = st.session_state["location_coords"]
    search_radius = st.session_state["search_radius"]
    bounding_box = st.session_state["bounding_box"]
    anzahl = analysis.countMarkersInBoundingbox(gdf)
    st.write(f"Anzahl Feuerstellen: *{anzahl}*")

### ---------------------------
### Anzahl Feuerstellen in Box
### ---------------------------
if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    
    gdf = st.session_state["map_result"]
    bounding_box = st.session_state["bounding_box"]
    density = analysis.calculateFireplaceDensity(gdf, bounding_box)
    st.write(f"Anzahl Feuerstellen pro Kilometer: *{density:.2f}%*")


### ---------------------------------
### Distanz zur nächsten Feuerstellen
### ---------------------------------
if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    
    gdf = st.session_state["map_result"]
    bounding_box = st.session_state["bounding_box"]
    create_fireplace_map(gdf, bounding_box)


if "map_result" and "location_coords" and "search_radius" and "bounding_box" in st.session_state:
    
    gdf = st.session_state["map_result"]
    location_coords = st.session_state["location_coords"]
    search_radius = st.session_state["search_radius"]
    bounding_box = st.session_state["bounding_box"]
    gdf = statistics.nearest_place(gdf, location_coords, search_radius, bounding_box)
