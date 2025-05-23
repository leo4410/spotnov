# functions/nearest_fireplace.py

import re
from shapely.geometry import Point, LineString
import geopandas as gpd
from geopy.distance import distance
from loaders.overpass import getMarkers
import folium
import streamlit as st

def create_fireplace_map(
    bbox: str,
    filters: str = '["leisure"="firepit"]',
    zoom_start: int = 13
) -> tuple[folium.Map, float] | None:
    """
    Baut eine Folium-Karte mit Zentrum, nächster Feuerstelle und Luftlinien-Linie.
    Gibt None zurück, wenn keine Feuerstellen in der Box gefunden werden.
    """

    # 1) Alle Nodes innerhalb der Box abfragen
    nodes = getMarkers([filters], bbox)

    # 2) Bounding-Box parsen
    nums = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", bbox)))
    min_lat, min_lon, max_lat, max_lon = nums
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2


    nodes["lat"] = nodes.geometry.y
    nodes["lon"] = nodes.geometry.x
    nodes["dist"] = 0

    # 3) Nächste Feuerstelle finden
    for node in nodes.itertuples():
        distance((center_lat, center_lon), (node.lat, node.lon)).km

    best_id = nodes['dist'].idxmin()
    best = nodes.loc[best_id]

    dist_km = distance((center_lat, center_lon), (best.lat, best.lon)).km




    # 4) Karte aufbauen
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)

    # Zentrum als grüner Punkt
    folium.CircleMarker(
        location=[center_lat, center_lon],
        radius=5, color="green", fill=True, fill_color="green",
        popup="Box-Zentrum"
    ).add_to(m)

    # Feuerstelle als roter Punkt
    folium.CircleMarker(
        location=[best.lat, best.lon],
        radius=5, color="red", fill=True, fill_color="red",
        popup=f"Feuerstelle ({dist_km:.2f} km)"
    ).add_to(m)

    # Linie dazwischen
    folium.PolyLine(
        [[center_lat, center_lon], [best.lat, best.lon]],
        color="blue", weight=2, dash_array="5,5"
    ).add_to(m)

    return m, dist_km