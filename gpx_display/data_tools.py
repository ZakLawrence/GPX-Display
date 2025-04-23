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

def convert_times_to_local(points,timezone_str):
    tz = ZoneInfo(timezone_str)
    for p in points:
        p["local_time"] = p["time"].astimezone(tz)
    return points

def format_pace(pace_min_per_km):
    if pace_min_per_km is None:
        return None
    minutes = int(pace_min_per_km)
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