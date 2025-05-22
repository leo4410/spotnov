import streamlit as st
from loaders import overpass
from functions import boundingbox
import pandas as pd


def title():
    st.write("Suche")


def search_interface():

    st.title("Objektsuche")

    label_dict = {
        1: "Bänke",
        2: "Feuerstellen",
        3: "Fussballplätze"
    }

    tag_dict = {
        1: """["amenity"="bench"]""",
        2: """["leisure"="firepit"]""",
        3: """["leisure"="pitch"]"""
    }

    with st.form("search_form"):

        location_input = st.text_input("Suchgebiet einstellen")
        radius_input = st.slider("Stelle den Radius ein", 0, 100, step=10)
        option_input = st.multiselect("Suchobjekt wählen", options=label_dict.keys(),default=label_dict.keys(),format_func=lambda x: label_dict[x]) #nimmt alle ausgewählten Keys (also das Objekt in Deutsch) und speichert diese in die Variabel
      
        submitted = st.form_submit_button("Suche starten!")

        if submitted:

            request = ""

            for e in option_input:
                st.write(e)
                request = request+f"{tag_dict[e]}"

            st.write(request)
            
            gdf=overpass.getFireplaces(request, boundingbox.calcBoundingBox(str(location_input), float(radius_input)) )

            st.session_state["map_result"] = gdf