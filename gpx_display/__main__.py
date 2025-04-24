import argparse
import gpxpy
from  .mapping import *
from .data_tools import *
from .input_tools import *
from pathlib import Path

def is_file(path: Path) -> bool:
    if not path.is_file():
        return False
    return path.name in (p.name for p in path.parent.iterdir())


def load_input_file(file_path):
    file_path = Path(file_path)
    if not is_file(file_path):
        raise RuntimeError(f"Cannot find file {file_path}! Check this!")
    file_name = file_path.parts[-1]
    if not file_name.endswith('.gpx'):
        raise RuntimeError(f"File provided is not a .gpx file, {file_path}")

    with open(file_path) as f:
        gpx = gpxpy.parse(f)

    return gpx    


def main():
    args = parse_args()

    if args.test is not None:
        print(args.test)

    gpx = load_input_file(args.input_file)
    points = parse_gpx_data(gpx)
    timezone = get_timezone(points[0])
    points = convert_times_to_local(points,timezone)
    points = calculate_pace_info(points)

    points = clip_route(points,args.start_time,args.start_distance,args.end_time,args.end_distance) 
    make_map(points)
    



def parse_args():
    parser = argparse.ArgumentParser(description="Command line tool to take some GPX data and produce a plot of the route with some additional data if requested")
    parser.add_argument('-f','--File',
                        dest="input_file",
                        required=True,
                        type=str,
                        default=None, 
                        help="Input file for the code to process")
    start = parser.add_mutually_exclusive_group(required=False)
    start.add_argument('-s','--start-time',
                        type=time_type,
                        dest="start_time",
                        required=False,
                        default=None,
                        help="Start time of main activity (e.g 09:00:00)")
    start.add_argument('--start-distance',
                        type=numeric_type,
                        dest="start_distance",
                        required=False,
                        default=None,
                        help="Start distance of main activity in km (e.g 1.34)")
    end = parser.add_mutually_exclusive_group(required=False)
    end.add_argument('-e','--end-time',
                        type=time_type,
                        dest="end_time",
                        required=False,
                        default=None,
                        help="End time of main activity (e.g 09:30:00)")
    end.add_argument('--end-distance',
                        type=numeric_type,
                        dest="end_distance",
                        required=False,
                        default=None,
                        help="End distance of main activity in km (e.g 5.90)")

    parser.add_argument('-t','--Test',
                        dest="test",
                        type=str,
                        default=None,
                        help="String to print to test argument parsing ability")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    main()
