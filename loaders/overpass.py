import geopandas as gpd
import overpy
from shapely.geometry import Point

def getMarkers(filters, boundingbox):
    
    filter_string = "("
    
    for filter in filters:
       filter_string = filter_string + "node" + filter + boundingbox + ";"
       
    filter_string = filter_string + ");out body;"
    
    api = overpy.Overpass()
    nodes = api.query(filter_string).nodes
    
    markers_list = []
    for node in nodes:
        point = Point(node.lon, node.lat)  

        entry = {
            "id": node.id,
            "geometry": point,
            # add further logic
        }
        
        markers_list.append(entry)
        
    markers_df = gpd.GeoDataFrame(markers_list, crs="EPSG:4326") 
    
    return markers_df
