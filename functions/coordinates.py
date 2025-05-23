from geopy.geocoders import Nominatim

def calcCoordinates(place:str):
    geolocator = Nominatim(user_agent="coordinates_calc", timeout=5)
    location = geolocator.geocode(place)
    
    lat, lon = float(location.latitude), float(location.longitude)

    return (lat, lon)
