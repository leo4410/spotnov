from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import box

def calcBoundingBox(place:str, radius:float):
    geolocator = Nominatim(user_agent="bbox_calc", timeout=5)
    location = geolocator.geocode(place)
    
    lat, lon = location.latitude, location.longitude

    # Berechne die 4 Richtungen (47.268048,7.186775,47.613107,8.115807)
    north = distance(kilometers=radius).destination((lat, lon), bearing=0)
    south = distance(kilometers=radius).destination((lat, lon), bearing=180)
    east = distance(kilometers=radius).destination((lat, lon), bearing=90)
    west = distance(kilometers=radius).destination((lat, lon), bearing=270)
    
    bbox = f"({south.latitude},{west.longitude}, {north.latitude}, {east.longitude})"

    return bbox

