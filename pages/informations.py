from helpers import colorScaleHelper
from loaders import overpass
import streamlit as st
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import st_folium

def title():
    st.header("Informationen")
    
def cantons():
    
    st.subheader("Anzahl Feuerstellen pro Kanton")
    # Shapefile-Pfad auf dem Server
    shapefile_path = "data/swissboundaries3d_2025-04_2056_5728.shp/swissBOUNDARIES3D_1_5_TLM_KANTONSGEBIET.shp"

    # Shapefile laden
    gdf = gpd.read_file(shapefile_path)

    # CRS prüfen und transformieren, falls nötig
    gdf_i=overpass.getAllFirepits()
    
    gdf_i=gdf_i.to_crs(epsg=2056)
    
    joined = gpd.sjoin(gdf_i, gdf, how="inner", predicate="within")
    point_counts = joined.groupby("UUID").size().reset_index(name="num_points")
    gdf = gdf.merge(point_counts, on="UUID", how="left")
    gdf["num_points"] = gdf["num_points"].fillna(0).astype(int)
    
    # GeoJSON-Interface extrahieren
    
    min_time = gdf['num_points'].min()
    max_time = gdf['num_points'].max()
    gdf['norm_points'] = (gdf['num_points'] - min_time) / (max_time - min_time)
    
    # Farbskala berechnen und hinzufügen
    gdf = gdf.to_crs(epsg=4326)
    gdf['color'] = gdf['norm_points'].apply(lambda x: colorScaleHelper.calculateColorScale(x, False))
    
    geojson = gdf.__geo_interface__

    for feature, color in zip(geojson["features"], gdf["color"]):
        feature["properties"]["color"] = color

    # Karte erstellen
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)

    # Polygone hinzufügen
    for idx, row in gdf.iterrows():
        color = f"rgb({row['color'][0]}, {row['color'][1]}, {row['color'][2]})"
        
        folium.GeoJson(
            row['geometry'].__geo_interface__,
            style_function=lambda feature, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 1
            }
        ).add_to(m)
        
    m.fit_bounds(m.get_bounds())

    # In Streamlit anzeigen
    st_folium(m, width=700, height=500)
