# Ortsnamen in Koordinaten umwandeln (Geokodierung)
# Luftlinienentfernung zwischen Geo-Punkten berechnen
# Bounding-Box-Geometrien erstellen
# Hilfsfunktion für Bounding-Box-Erzeugung
# GeoDataFrames für räumliche Daten
# Datenanalyse und Tabellenverarbeitung
# OSM-Datenabruf über Overpass API

from geopy.geocoders import Nominatim                                       
from geopy.distance import distance
from shapely.geometry import box

from functions import boundingbox

import geopandas as gpd
import pandas as pd

from loaders.overpass import getMarkers

def count_fireplaces_in_bbox(markers) -> int:
    """
    Zählt alle OSM-Nodes, die dem Tag-Filter entsprechen
    (default: leisure=firepit) und innerhalb der Bounding-Box liegen.
    bbox muss im Format "(min_lat,min_lon,max_lat,max_lon)" vorliegen.
    """
    return len(markers)

# Ruft alle OSM-Einträge ab, die zum Filter passen und in der Bounding-Box liegen.
# Gibt die Anzahl der gefundenen Einträge (also die Anzahl der Feuerstellen) als ganzzahligen Wert zurück.
     