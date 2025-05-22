import pandas as pd
import streamlit as st
from functions import boundingbox
from loaders import overpass

def title():
    st.write("Suche")


def search_interface():

    st.title("Objektsuche")

    options_dict = {
        1: {"label": "Bänke", "tag": '["amenity"="bench"]'},
        2: {"label": "Feuerstellen", "tag": '["leisure"="firepit"]'},
        3: {"label": "Fussballplätze", "tag": '["leisure"="pitch"]'},
    } 

    with st.form("search_form"):

        location_input = st.text_input("Suchgebiet einstellen")
        radius_input = st.slider("Stelle den Radius ein", 0, 100, step=10)
        option_input = st.multiselect("Suchobjekt wählen",options=options_dict.keys(),default=options_dict.keys(),format_func=lambda x: options_dict[x]["label"] ) #nimmt alle ausgewählten Keys (also das Objekt in Deutsch) und speichert diese in die Variabel
      
        submitted = st.form_submit_button("Suche starten!")

        if submitted:

            request = []

            for e in option_input:
                request.append(options_dict[e]["tag"]) 
            
            gdf=overpass.getMarkers(request, boundingbox.calcBoundingBox(str(location_input), float(radius_input)) )

            st.session_state["map_result"] = gdf
            