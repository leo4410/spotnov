# functions/density_fireplaces.py

import re
from geopy.distance import distance
from functions.anzahl_fireplace import count_fireplaces_in_bbox

def density_fireplaces_in_bbox(
    bbox: str,
    filters: str = '["leisure"="firepit"]'
) -> float:
    """
    Berechnet die Dichte der Feuerstellen in Prozent basierend auf der Bounding-Box.
    Dichte = (Anzahl der Feuerstellen / Fläche der Bounding-Box in km²) * 100

    Parameter:
    - bbox: Bounding-Box im Format "(min_lat,min_lon,max_lat,max_lon)"
    - filters: OSM-Tag-Filter (default: leisure=firepit)
    """
    # 1) Anzahl der Feuerstellen in der Box ermitteln
    count = count_fireplaces_in_bbox(bbox, filters)

    # 2) Bounding-Box-String in vier Koordinaten parsen
    coords = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", bbox)))
    min_lat, min_lon, max_lat, max_lon = coords

    # 3) Breite der Box (in km) auf halber Höhe berechnen
    center_lat = (min_lat + max_lat) / 2
    width_km = distance((center_lat, min_lon), (center_lat, max_lon)).km

    # 4) Höhe der Box (in km) auf halber Breite berechnen
    center_lon = (min_lon + max_lon) / 2
    height_km = distance((min_lat, center_lon), (max_lat, center_lon)).km

    # 5) Fläche der Box in km²
    area_km2 = width_km * height_km

    # 6) Dichte in Prozent berechnen
    density_percent = (count / area_km2) * 100
    return density_percent
