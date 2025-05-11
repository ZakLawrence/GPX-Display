import osmnx as ox
from osmnx._errors import InsufficientResponseError 
import matplotlib.pyplot as plt 
from .data_tools import *



def make_map(route,
             route_name = None,
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

    try:
        G = ox.graph_from_bbox(box, network_type="drive",retain_all=True,simplify=False)
    except:
        G = None
    try:
        W = ox.graph_from_bbox(box, network_type="walk",retain_all=True,simplify=False)
    except:
        W = None
    
    try:
        buildings = ox.features_from_bbox(box, tags={"building": True})
    except InsufficientResponseError:
        buildings = None
    
    # === 4. Get landcover features ===
    green_tags = {
        "leisure": ["park"],
        "landuse": ["grass", "recreation_ground"],
        "natural": ["wood"]
    }
    try:
        greenspace = ox.features_from_bbox(box, tags=green_tags)
    except InsufficientResponseError:
        greenspace = None 

    water_tags = {
        "natural": "water"
    }
    try:
        water = ox.features_from_bbox(box, tags=water_tags)
    except InsufficientResponseError:
        water = None 

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
    if greenspace is not None and not greenspace.empty:
        greenspace.plot(ax=ax, facecolor="lightgreen", edgecolor="none", alpha=0.4)
    
    # Water
    if water is not None and not water.empty:
        water.plot(ax=ax, facecolor="lightblue", edgecolor="none", alpha=0.5)
    
    # Buildings
    if buildings is not None and not buildings.empty:
        buildings.plot(ax=ax, facecolor="lightgray", edgecolor="gray", linewidth=0.5, alpha=0.8)
    
    if sportsspace is not None and not sportsspace.empty:
        sportsspace.plot(ax=ax, facecolor="pink", edgecolor="none", alpha=0.8)
    
    # Streets
    if G is not None:
        ox.plot_graph(G, ax=ax, node_size=0, edge_color="black", edge_linewidth=1.5, show=False, close=False)
    if W is not None:
        ox.plot_graph(W, ax=ax, node_size=0, edge_color="black", edge_linewidth=0.5, show=False, close=False)
    
    # GPX route
    lat, lon = zip(*coords)
    ax.plot(lon, lat, color="#fc4c02", linewidth=2, label="GPX Track")
    
    if route_name is not None:
        label_x = west + (east - west)/4
        label_y = north - padding/2
        ax.text(label_x, label_y, route_name,
            fontsize=30,
            color="#fc4c02",
            fontname="Verdana",
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    plt.tight_layout()
    plt.savefig(f"{route_name.replace(" ","_")}.png", dpi=300)
    #plt.show()
