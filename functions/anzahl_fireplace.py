from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import box

from functions import boundingbox

import geopandas as gpd
import pandas as pd

from loaders.overpass import getMarkers

def count_fireplaces_in_bbox(
    bbox: str,
    filters: str = '["leisure"="firepit"]'
) -> int:
    """
    Zählt alle OSM-Nodes, die dem Tag-Filter entsprechen
    (default: leisure=firepit) und innerhalb der Bounding-Box liegen.
    bbox muss im Format "(min_lat,min_lon,max_lat,max_lon)" vorliegen.
    """
    nodes = getMarkers([filters], bbox)
    return len(nodes)