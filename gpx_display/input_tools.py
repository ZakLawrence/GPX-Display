import argparse
from datetime import datetime, time

def time_type(tstr):
    try: 
        return datetime.strptime(tstr,"%H:%M:%S").time()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Could not parse time: {tstr}! Time must be in HH:MM:SS format")
    
def numeric_type(nstr):
    try:
        return int(nstr)
    except ValueError:
        try: 
            return float(nstr)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Value {nstr} is not a valid number!")