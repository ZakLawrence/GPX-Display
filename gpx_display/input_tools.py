import argparse
from datetime import datetime, time

def parse_time_string(tstr):
    try: 
        return datetime.strptime(tstr,"%H:%M:%S").time()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Could not parse time: {tstr}! Time must be in HH:MM:SS format")