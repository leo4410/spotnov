import geopandas as gpd
import networkx as nx
import osmnx as ox

def example_analyse():
    df = gpd.read_file("data/100058.csv", sep=";", encoding="utf-8")
    return df

def calculate_shortest_distance(gdf, start_coords, search_radius, boundingbox):
    
    # south, west, north, east = boundingbox
    # G = ox.load_graphml("data/switzerland_walk.graphml")
    # G = ox.truncate_graph_bbox(G, north=north, south=south, west=west, east=east)
    
    G = ox.graph_from_point(start_coords, dist=search_radius*1000, network_type='walk')

    orig_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])

    meters_per_minute = 5 * 1000 / 60
    for u, v, data in G.edges(data=True):
        data['travel_time'] = data['length'] / meters_per_minute
    
    gdf["travel_time"]=0

    for idx, row in gdf.iterrows():
    
        try:
            route_length = nx.shortest_path_length(G, orig_node, ox.distance.nearest_nodes(G, X=row.lon, Y=row.lat), weight='travel_time')
            gdf.at[idx, "travel_time"] = route_length
        except nx.NetworkXNoPath:
            gdf.at[idx, "travel_time"] = None

    return(gdf)
