import folium
import pydeck as pdk
import streamlit as st

from functions import boundingbox, places
from loaders import overpass
from streamlit_folium import st_folium

def title():
    st.write("Suche")

def search_map():
    location_coordinates = ()

    if "last_click" not in st.session_state:
        st.session_state["last_click"] = None

    center = st.session_state["last_click"] or {"lat":47.0502 , "lng": 8.3093}
    m = folium.Map(location=[center["lat"], center["lng"]], zoom_start=13, attr='Mapbox',name='Mapbox Dark',tiles="CartoDB dark_matter")

    if st.session_state["last_click"]:
        lat = st.session_state["last_click"]["lat"]
        lon = st.session_state["last_click"]["lng"]
        folium.Marker(location=[lat, lon], popup="Letzter Klick").add_to(m)

    output = st_folium(m, height=500, width=700)
    clicked = output.get("last_clicked")

    if clicked:
        st.session_state["last_click"] = clicked
        st.rerun()

    # 7. Koordinaten ausgeben
    if st.session_state["last_click"]:
        lat = st.session_state["last_click"]["lat"]
        lon = st.session_state["last_click"]["lng"]
        location_coordinates = (lat,lon)
    else:
        st.info("Klicke auf die Karte, um Koordinaten zu wählen.")

    options_dict = {
        1: {"label": "Bänke", "tag": '["amenity"="bench"]'},
        2: {"label": "Feuerstellen", "tag": '["leisure"="firepit"]'},
        3: {"label": "Fussballplätze", "tag": '["leisure"="pitch"]'},
    } 

    with st.form("set_form"):

        radius_input = st.slider("Stelle den Radius ein", 0, 20, step=1)
        option_input = st.multiselect("Suchobjekt wählen",options=options_dict.keys(),default=options_dict.keys(),format_func=lambda x: options_dict[x]["label"] ) #nimmt alle ausgewählten Keys (also das Objekt in Deutsch) und speichert diese in die Variabel
      
        submitted = st.form_submit_button("Suche starten!")

        if submitted:

            request = []

            for e in option_input:
                request.append(options_dict[e]["tag"]) 
            
            bounding_box = boundingbox.calcBoundingBox(location_coordinates, float(radius_input))
            
            gdf=overpass.getMarkers(request, bounding_box )
            
            st.session_state["map_result"] = gdf
            st.session_state["location_coords"] = location_coordinates
            st.session_state["bounding_box"] = bounding_box
            st.session_state["search_radius"] = radius_input


def search_interface():

    st.title("Objektsuche")

    options_dict = {
        1: {"label": "Bänke", "tag": '["amenity"="bench"]'},
        2: {"label": "Feuerstellen", "tag": '["leisure"="firepit"]'},
        3: {"label": "Fussballplätze", "tag": '["leisure"="pitch"]'},
    } 

    with st.form("search_form"):

        location_input = st.text_input("Suchgebiet einstellen")
        radius_input = st.slider("Stelle den Radius ein", 0, 20, step=1)
        option_input = st.multiselect("Suchobjekt wählen",options=options_dict.keys(),default=options_dict.keys(),format_func=lambda x: options_dict[x]["label"] ) #nimmt alle ausgewählten Keys (also das Objekt in Deutsch) und speichert diese in die Variabel
      
        submitted = st.form_submit_button("Suche starten!")

        if submitted:

            request = []

            for e in option_input:
                request.append(options_dict[e]["tag"]) 
            
            location_coords = places.calcPlace(str(location_input))
            bounding_box = boundingbox.calcBoundingBox(location_coords, float(radius_input))
            
            gdf=overpass.getMarkers(request, bounding_box )
            st.session_state["map_result"] = gdf
            st.session_state["location_coords"] = location_coords
            st.session_state["bounding_box"] = bounding_box
            st.session_state["search_radius"] = radius_input


def search_result(gdf):
    gdf["lat"] = gdf.geometry.y
    gdf["lon"] = gdf.geometry.x

    color_map = {
        "firepit": [0, 255, 255],
        "bench": [255, 255, 0],
        "pitch": [180, 0, 0],
        None: [128, 128, 128]
    }

    gdf["color"] = gdf.get("typ", None).apply(lambda x: color_map.get(x, [128, 128, 128]))
    gdf["name"] = gdf.get("name", None)

    # Layer definieren
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=gdf,
        get_position='[lon, lat]',
        get_fill_color="color",
        get_radius=70,
        pickable=True
    )

    # View definieren
    view_state = pdk.ViewState(
        latitude=gdf["lat"].mean(),
        longitude=gdf["lon"].mean(),
        zoom=13
    )

    # Tooltip definieren
    tooltip = {
        "html": "<b>{id}</b><br>Typ: {typ}",
        "style": {"backgroundColor": "white", "color": "black"}
    }   

    # Karte anzeigen mit Hover
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    ))
