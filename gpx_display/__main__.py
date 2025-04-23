import argparse
import gpxpy
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
    parser = argparse.ArgumentParser(description="Command line tool to take some GPX data and produce a plot of the route with some additional data if requested")
    parser.add_argument('-f','--File',
                        dest="input_file",
                        required=True,
                        type=str,
                        default=None, 
                        help="Input file for the code to process")
    parser.add_argument('-s','--start-time',
                        type=parse_time_string,
                        dest="start_time",
                        required=False,
                        default=None,
                        help="Start time of main activity (e.g 09:00:00)")
    parser.add_argument('-e','--end-time',
                        type=parse_time_string,
                        dest="end_time",
                        required=False,
                        default=None,
                        help="End time of main activity (e.g 09:30:00)")

    parser.add_argument('-t','--Test',
                        dest="test",
                        type=str,
                        default=None,
                        help="String to print to test argument parsing ability")

    args = parser.parse_args()

    if args.test is not None:
        print(args.test)

    gpx = load_input_file(args.input_file)
    points = parse_gpx_data(gpx)
    timezone = get_timezone(points[0])
    points = convert_times_to_local(points,timezone)
    points = calculate_pace_info(points)

    activity_date = points[0]['local_time'].date()
    print(f"Activity Date: {activity_date}")
    if args.start_time:
        combined = datetime.combine(activity_date, args.start_time)
        print(f"Inferred full datetime: {combined}")
    else:
        print("No start time provided")

    print(points[59]['local_time'].time())


if __name__ == "__main__":
    main()
