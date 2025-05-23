# imports
# # Parsen, Geometrie, Geodatenverarbeitung, Distanzberechnung, OSM-Datenabruf, Kartendarstellung, Webinterface

from streamlit_folium import st_folium
import re
import geopandas as gpd
from geopy.distance import distance
import folium

def create_fireplace_map(nodes, bbox):
    """
    Baut eine Folium-Karte mit Zentrum, nächster Feuerstelle und Luftlinien-Linie.
    Gibt None zurück, wenn keine Feuerstellen in der Box gefunden werden.
    """

    #hier werden die Feuerstellen geladen -->liefert ein GeodataFrame mit allen OSM-Nodes im Rechteck

    
    nums = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", bbox)))
    min_lat, min_lon, max_lat, max_lon = nums
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    #re.findall(r"[-+]?\d*\.\d+|\d+", bbox) sucht in dem String bbox nach allen Zahlen (mit oder ohne Vorzeichen, mit Dezimalpunkt oder als Ganzzahl).
    #map(float, …) wandelt jede gefundene Zahl in einen float um.
    #list(…) speichert diese vier Werte in der Liste nums.
    #Anschliessend werden die vier Werte der Reihe nach den Variablen min_lat (minimale Breite), min_lon (minimale Länge), max_lat (maximale Breite) und max_lon (maximale Länge) zugewiesen.
    #hier wird der geografische Mittelpunkt der Bounding Box berechnet

    nodes["lat"] = nodes.geometry.y
    nodes["lon"] = nodes.geometry.x
    nodes["dist"] = 0

    #Der geografische Mittelpunkt der Bounding-Box wird in den Variablen center_lat und center_lon gespeichert, 
    #waehrend im GeoDataFrame nur fuer jede Feuerstelle die Spalten lat, lon und eine anfaenglich auf 0 gesetzte Spalte dist angelegt werden, 
    #in der spaeter die berechneten Entfernungen zum Mittelpunkt abgespeichert werden.

    
    for idx, row in nodes.iterrows():
        nodes.loc[idx, "dist"] = distance((center_lat, center_lon), (row.lat, row.lon)).km

    best_id = nodes["dist"].idxmin()
    best = nodes.loc[best_id]

    dist_km = nodes.loc[best_id, "dist"]

    #Der Code geht jede Feuerstelle in der Tabelle durch und misst die direkte Luftlinie vom zuvor ermittelten Kartenmittelpunkt bis zur jeweiligen Feuerstelle; das Ergebnis wird sofort in der Tabelle als Distanzwert gespeichert.
    #Sobald alle Distanzen eingetragen sind, durchsucht der Code diese Werte und findet die geringste Entfernung, um so die am nächsten gelegene Feuerstelle auszuwählen.
    #Mit dieser Information kann die Funktion dann gezielt genau diesen Punkt auf der Karte markieren und die Distanz anzeigen.

    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

   
    folium.CircleMarker(
        location=[center_lat, center_lon],
        radius=5, color="green", fill=True, fill_color="green",
        popup="Box-Zentrum"
    ).add_to(m)

    
    folium.CircleMarker(
        location=[best.lat, best.lon],
        radius=5, color="red", fill=True, fill_color="red",
        popup=f"Feuerstelle ({dist_km:.2f} km)"
    ).add_to(m)

    
    folium.PolyLine(
        [[center_lat, center_lon], [best.lat, best.lon]],
        color="blue", weight=2, dash_array="5,5"
    ).add_to(m)

    st_folium(m, width=700, height=500, key="nearest_fireplace_map")

# Die Funktion erstellt eine Folium-Karte, zentriert auf den geografischen Mittelpunkt der übergebenen Bounding-Box, lädt alle OSM-Feuerstellen nach dem Filter (standardmäßig leisure=firepit),
# berechnet die Luftlinien-Distanz zum nächsten Fundort, markiert Zentrum und nächstgelegene Feuerstelle mit Kreismarkern, 
# verbindet sie per Linie und gibt die Karte sowie die Distanz in Kilometern zurück (oder None, falls keine Treffer vorliegen).