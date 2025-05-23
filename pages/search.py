import pandas as pd
import streamlit as st
from functions import boundingbox
from loaders import overpass
import folium
from streamlit_folium import st_folium

def title():
    st.write("Suche")


def search_interface():

    st.title("Objektsuche")

    options_dict = {
        1: {"label": "Bänke", "tag": '["amenity"="bench"]'},
        2: {"label": "Feuerstellen", "tag": '["leisure"="firepit"]'},
        3: {"label": "Fussballplätze", "tag": '["leisure"="pitch"]'},
    } 






    if "last_click" not in st.session_state:
        st.session_state["last_click"] = None # Initalisiert st.session_state["last_click"] mit None, wenn noch nicht vorhanden


    center = st.session_state["last_click"] or {"lat": 68.0, "lng": 2.0} # Definiert ein center- Point, mit Werten aus "last_click" oder default- Werten


    m = folium.Map(location=[center["lat"], center["lng"]], zoom_start=13) # Generiert eine leere Karte mit dem zuvor definierten Zentrum


    if st.session_state["last_click"]: # Wenn "Klick" auf Karte erfolgt, werden lat/lon extrahiert und ein Marker zu Karte hinzugefügt
        lat = st.session_state["last_click"]["lat"]
        lon = st.session_state["last_click"]["lng"]
        folium.Marker(location=[lat, lon], popup="Letzter Klick").add_to(m)


    output = st_folium(m, height=500, width=700) # Karte wird in streamlit eingebunden und als Dict. (u.A. mit key "last_click") in output gespeichert
    clicked = output.get("last_clicked") 


    if clicked:
        st.session_state["last_click"] = clicked
        st.rerun()


        


    with st.form("search_form"):

        location_input = st.text_input("Suchgebiet einstellen")
        radius_input = st.slider("Stelle den Radius ein", 0, 20, step=1)
        option_input = st.multiselect("Suchobjekt wählen",options=options_dict.keys(),default=options_dict.keys(),format_func=lambda x: options_dict[x]["label"] ) #nimmt alle ausgewählten Keys (also das Objekt in Deutsch) und speichert diese in die Variabel
      
        submitted = st.form_submit_button("Suche starten!")

        if submitted:

            request = []

            for e in option_input:
                request.append(options_dict[e]["tag"]) 
            
            gdf=overpass.getMarkers(request, boundingbox.calcBoundingBox(str(location_input), float(radius_input)) )

            st.session_state["map_result"] = gdf





    if st.session_state["last_click"]:
        return (
            st.session_state["last_click"]["lat"],
            st.session_state["last_click"]["lng"]
        )
    else:
        return None, None
            