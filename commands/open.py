import argparse
import os
def run(args):
    parser = argparse.ArgumentParser(
        description="Opens visual studio code on the productivity tools folder"
    )
    parsed_args = parser.parse_args(args)
    cwd = os.path.dirname(os.path.abspath(__file__))
    cwd = os.path.dirname(cwd)
    os.popen(f"code {cwd}")