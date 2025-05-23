from geopy.geocoders import Nominatim

def calcPlace(place):
    geolocator = Nominatim(user_agent="bbox_calc", timeout=5)
    location = geolocator.geocode(place)
    lat, lon = location.latitude, location.longitude
    return (lat, lon)