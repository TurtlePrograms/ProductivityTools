import argparse
from tools.core import ToolRegistry, Logger, LogLevel
import subprocess
from time import sleep

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("watch")
    )
    settings_group = parser.add_argument_group("Settings")
    settings_group.add_argument("--time", type=int, nargs='?', default=1, help="The time in seconds to wait before running the command again, default: 1")
    settings_group.add_argument("--times", type=int, nargs='?', default=-1, help="The number of times to run the command (default: -1 for infinite)")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="The command to run")
    parsed_args = parser.parse_args(args)
    time = parsed_args.time
    args = parsed_args.args
    Logger.log(f"Waiting for {time} seconds...", LogLevel.INFO)
    Logger.log(f"Arguments: {args}", LogLevel.INFO)
    count = 0
    while True:
        output =  subprocess.run(args, shell=True, capture_output=True, text=True)
        subprocess.run(["cls"], shell=True)
        Logger.log(output.stdout,LogLevel.NONE)
        sleep(time)
        count += 1
        if count == parsed_args.times and parsed_args.times != -1:
            break
    return

if __name__ == "__main__":
    Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
