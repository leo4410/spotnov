import geopandas as gpd
import networkx as nx
import osmnx as ox
import re                                                          
from geopy.distance import distance                                

def example_analyse():
    df = gpd.read_file("data/100058.csv", sep=";", encoding="utf-8")
    return df

def calculate_shortest_distance(gdf, start_coords, search_radius, boundingbox):
    
    # south, west, north, east = boundingbox
    # G = ox.load_graphml("data/switzerland_walk.graphml")
    # G = ox.truncate_graph_bbox(G, north=north, south=south, west=west, east=east)
    
    G = ox.graph_from_point(start_coords, dist=search_radius*1000, network_type='walk')

    orig_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
    dest_nodes = ox.distance.nearest_nodes(G, X=gdf["lon"].values, Y=gdf["lat"].values)

    meters_per_minute = 5 * 1000 / 60
    for u, v, data in G.edges(data=True):
        data['travel_time'] = data['length'] / meters_per_minute
    
    gdf["travel_time"]=0

    lengths = nx.single_source_dijkstra_path_length(G, orig_node, weight="travel_time")
    gdf["travel_time"] = [lengths.get(node, None) for node in dest_nodes]

    return(gdf)

def countMarkersInBoundingbox(markers):
    return len(markers)

def calculateFireplaceDensity(markers, bbox):
    """
    Berechnet die Dichte der Feuerstellen in Prozent basierend auf der Bounding-Box.
    Dichte = (Anzahl der Feuerstellen / Fläche der Bounding-Box in km²) * 100

    Parameter:
    - bbox: Bounding-Box im Format "(min_lat,min_lon,max_lat,max_lon)"
    - filters: OSM-Tag-Filter (default: leisure=firepit)
    """
    # Anzahl Feuerstellen berechnen
    count = countMarkersInBoundingbox(markers)

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
    density = (count / area_km2)
    return density

