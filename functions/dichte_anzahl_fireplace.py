# imports

import re                                                           # Reguläre Ausdrücke zum Parsen und Extrahieren von Zahlen aus Strings
from geopy.distance import distance                                 # Luftlinienentfernung zwischen zwei Geo-Koordinaten in Kilometern berechnen  
from functions.anzahl_fireplace import count_fireplaces_in_bbox     # Anzahl der Feuerstellen in einer Bounding-Box ermitteln

def density_fireplaces_in_bbox(markers, bbox) -> float:
    """
    Berechnet die Dichte der Feuerstellen in Prozent basierend auf der Bounding-Box.
    Dichte = (Anzahl der Feuerstellen / Fläche der Bounding-Box in km²) * 100

    Parameter:
    - bbox: Bounding-Box im Format "(min_lat,min_lon,max_lat,max_lon)"
    - filters: OSM-Tag-Filter (default: leisure=firepit)
    """
    # Mit der Hilfsfunktion wird zuerst die Gesamtzahl der Feuerstellen in der Bounding-Box ermittelt.
    count = count_fireplaces_in_bbox(markers)

    # Bounding-Box-String in vier Koordinaten parsen. Aus dem BBox-String werden die vier Eckkoordinaten als Zahlen extrahiert.
    coords = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", bbox)))
    min_lat, min_lon, max_lat, max_lon = coords

    # Die horizontale Ausdehnung wird als Luftlinien-Distanz auf halber Höhe gemessen.
    center_lat = (min_lat + max_lat) / 2
    width_km = distance((center_lat, min_lon), (center_lat, max_lon)).km

    # Die vertikale Ausdehnung wird als Luftlinien-Distanz auf halber Breite gemessen.
    center_lon = (min_lon + max_lon) / 2
    height_km = distance((min_lat, center_lon), (max_lat, center_lon)).km

    # Aus Breite und Höhe ergibt sich die Gesamtfläche in Quadratkilometern.
    area_km2 = width_km * height_km

    # Die Dichte wird als (Anzahl Feuerstellen / Fläche) × 100 in Prozent ausgegeben.
    density_percent = (count / area_km2) * 100
    return density_percent
