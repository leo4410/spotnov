import geopandas as gpd

def example_analyse():
    df = gpd.read_file("data/100058.csv", sep=";", encoding="utf-8")
    return df
