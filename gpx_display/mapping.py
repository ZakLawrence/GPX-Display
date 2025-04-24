import osmnx as ox
from osmnx._errors import InsufficientResponseError 
import matplotlib.pyplot as plt 
from .data_tools import *


def make_map(route,
             padding = 0.001
             ):
    coords = get_lat_long(route)

    lats, lons = zip(*coords)
    
    north,south = max(lats),min(lats)
    east,west = max(lons),min(lons)

    north += padding
    south -= padding
    east += padding
    west -= padding
    box = (west,south,east,north)

    G = ox.graph_from_bbox(box, network_type="drive",retain_all=True,simplify=False)
    W = ox.graph_from_bbox(box, network_type="walk",retain_all=True,simplify=False)
    buildings = ox.features_from_bbox(box, tags={"building": True})
    
    
    # === 4. Get landcover features ===
    green_tags = {
        "leisure": ["park"],
        "landuse": ["grass", "recreation_ground"],
        "natural": ["wood"]
    }
    greenspace = ox.features_from_bbox(box, tags=green_tags)
    
    water_tags = {
        "natural": "water"
    }
    water = ox.features_from_bbox(box, tags=water_tags)
    
    sports_tags = {
        "leisure": ["track"]
    }
    try:
        sportsspace = ox.features_from_bbox(box, tags=sports_tags)
    except InsufficientResponseError: 
        sportsspace = None

    # === 5. Plot ===
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Greenspace (parks, grass, etc.)
    if not greenspace.empty:
        greenspace.plot(ax=ax, facecolor="lightgreen", edgecolor="none", alpha=0.4)
    
    # Water
    if not water.empty:
        water.plot(ax=ax, facecolor="lightblue", edgecolor="none", alpha=0.5)
    
    # Buildings
    if not buildings.empty:
        buildings.plot(ax=ax, facecolor="lightgray", edgecolor="gray", linewidth=0.5, alpha=0.8)
    
    if sportsspace is not None and not sportsspace.empty:
        sportsspace.plot(ax=ax, facecolor="pink", edgecolor="none", alpha=0.8)
    
    # Streets
    ox.plot_graph(G, ax=ax, node_size=0, edge_color="black", edge_linewidth=1.5, show=False, close=False)
    ox.plot_graph(W, ax=ax, node_size=0, edge_color="black", edge_linewidth=0.5, show=False, close=False)
    
    # GPX route
    lat, lon = zip(*coords)
    ax.plot(lon, lat, color="#fc4c02", linewidth=2, label="GPX Track")
    
    plt.tight_layout()
    plt.savefig("route_landcover.png", dpi=300)
    plt.show()
