import geopandas as gpd
import overpy
from shapely.geometry import Point

def requestApi(filters, boundingbox):
    
    start_string="node "
    end_string=";out;"
    api = overpy.Overpass()
    
    result_nodes = api.query(start_string + filters + boundingbox + end_string).nodes
    
    return result_nodes
    

def getFireplaces(filters, boundingbox):
    fireplaceNodes = requestApi(filters, boundingbox)
    fireplace_list = []

    for node in fireplaceNodes:
        point = Point(node.lon, node.lat)  

        entry = {
            "id": node.id,
            "geometry": point,
            # add further logic
        }
        
        fireplace_list.append(entry)
        
    fireplace_df = gpd.GeoDataFrame(fireplace_list, crs="EPSG:4326") 
    
    return fireplace_df