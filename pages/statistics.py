import streamlit as st
from functions import analysis
import pydeck as pdk
import streamlit as st

def title():
    st.write("Statistik")

def nearest_place(gdf, locaion_coords, search_radius, boundingbox):

    gdf = analysis.calculate_shortest_distance(gdf, locaion_coords, search_radius, boundingbox)

    st.write(gdf)
    st.write(locaion_coords)

    min_time = gdf['travel_time'].min()
    max_time = gdf['travel_time'].max()
    gdf['norm_time'] = (gdf['travel_time'] - min_time) / (max_time - min_time)

    # Funktion für RGB-Farben: grün → rot
    def get_color(norm_val):
        r = int(255 * norm_val)
        g = int(255 * (1 - norm_val))
        return [r, g, 0]  # RGB

    gdf['color'] = gdf['norm_time'].apply(get_color)

    # Pydeck-Layer definieren
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=gdf,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=100,  # Pixelradius
        pickable=True,
        auto_highlight=True,
    )

    # View definieren
    view_state = pdk.ViewState(
        latitude=gdf['lat'].mean(),
        longitude=gdf['lon'].mean(),
        zoom=11,
        pitch=0,
    )

    # Tooltip (optional)
    tooltip = {
        "html": "<b>{zielpunkt}</b><br/>Zeit: {travel_time_min} min",
        "style": {"backgroundColor": "white", "color": "black"}
    }

    # Karte rendern
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    ))
    