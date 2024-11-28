import argparse
import subprocess
from time import sleep

def run(args):
    parser = argparse.ArgumentParser(
        description="Runs a command at a specified interval"
    )
    parser.add_argument("time", type=int, help="The time in seconds to wait before running the command again")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parsed_args = parser.parse_args(args)
    time = parsed_args.time
    args = parsed_args.args
    print(f"Waiting for {time} seconds...")
    print(f"Arguments: {args}")
    while True:
        output =  subprocess.run(args, shell=True, capture_output=True, text=True)
        subprocess.run(["cls"], shell=True)
        print(output.stdout)
        sleep(time)