import streamlit as st


def title():
    st.write("Suche")


def search_interface():

    st.title("Objektsuche")

    search_area = st.text_input("Suchgebiet einstellen")

    search_radius = st.slider("Stelle den Radius ein", 0, 100, step=10)

    tag_mapping = {"Bänke" : "Bench",
                   "Feuerstellen" : "firepit",
                   "Fussballplätze" : "pitch"}

    st.markdown("Wähle das Suchobjekt")
    with st.container(border=True):
        search_option_de = st.multiselect("Objekt", tag_mapping.keys(), default=list(tag_mapping.keys())) #nimmt alle ausgewählten Keys (also das Objekt in Deutsch) und speichert diese in die Variabel

    if st.button("Suche starten!"):
        overpass_tag = [tag_mapping[de] for de in search_option_de] #Erstellt eine Liste mit den Values aus tag_mapping, wobei "de" die Keys darstellen, die aus der search_option_de stammen
        search(search_area, search_radius, tag_mapping(overpass_tag))

    #st.map()