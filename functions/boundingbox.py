from geopy.distance import distance

def calcBoundingBox(place, radius:float):
    lat, lon = place[0], place[1]

    north = distance(kilometers=radius).destination((lat, lon), bearing=0)
    south = distance(kilometers=radius).destination((lat, lon), bearing=180)
    east = distance(kilometers=radius).destination((lat, lon), bearing=90)
    west = distance(kilometers=radius).destination((lat, lon), bearing=270)
    
    bbox = f"({south.latitude},{west.longitude}, {north.latitude}, {east.longitude})"

    return bbox
