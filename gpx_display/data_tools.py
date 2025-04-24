import gpxpy
from datetime import datetime
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
from geopy.distance import geodesic

def get_timezone(point):
    tf = TimezoneFinder()
    return tf.timezone_at(lat=point["lat"],lng=point["long"])

def parse_gpx_data(gpx):
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    "lat":point.latitude,
                    "long":point.longitude,
                    "elevation":point.elevation,
                    "time":point.time
                })
    return points

def get_lat_long(points):
    return [(p['lat'],p['long']) for p in points]

def convert_times_to_local(points,timezone_str):
    tz = ZoneInfo(timezone_str)
    for p in points:
        p["local_time"] = p["time"].astimezone(tz)
    return points

def format_pace(pace_min_per_km):
    if pace_min_per_km is None:
        return None
    minutes = int(pace_min_per_km)
    if minutes > 20:
        return "Stopped"
    seconds = int(round((pace_min_per_km - minutes) * 60))
    return f"{minutes}:{seconds:02d} min/km"

def calculate_pace_info(points,window_size=4):
    for i in range(len(points)):
        start_idx = max(0,i-window_size)
        end_idx = min(len(points)-1,i+window_size)

        start = points[start_idx]
        end = points[end_idx]

        distance_km = geodesic((start["lat"],start["long"]),(end["lat"],end["long"])).km
        duration_min = (end["time"]-start["time"]).total_seconds()/60.0

        if distance_km > 0 and duration_min > 0: 
            pace = duration_min/distance_km
        else:
            pace = None
        
        points[i]["pace"] = pace
        points[i]["pace_formatted"] = format_pace(pace)
    return points

def clip_route_time(points,start=None,end=None):
    if start is None and end is None:
        return points
    
    clipped = []
    for pt in points:
        pt_time = pt['local_time'].time()
        if start and pt_time < start:
            continue
        if end and pt_time > end:
            continue
        clipped.append(pt)
    return clipped

def clip_route_distance(points,start=None,end=None):
    if start is None and end is None:
        return points
    
    total_distance = 0 
    clipped = []
    for i in range(len(points)):    
        if i == 0 and start and start > 0:
            continue
        if i > 0:
            p1 = (points[i-1]['lat'],points[i-1]['long'])
            p2 = (points[i]['lat'],points[i]['long'])
            dist = geodesic(p1,p2).km
            total_distance += dist
            if start and total_distance < start:
                continue
            if end and total_distance > end:
                continue
        clipped.append(points[i])
    return clipped

def clip_route(points,start_time=None,start_distance=None, end_time=None, end_distance=None):
    points = clip_route_time(points,start_time,end_time)
    points = clip_route_distance(points,start_distance,end_distance)
    return points
