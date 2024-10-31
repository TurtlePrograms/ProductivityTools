import argparse
import os
def run(args):
    parser = argparse.ArgumentParser(
        description="Run Command, runs a set profile. a profile contains one or more programs to start"
    )
    parsed_args = parser.parse_args(args)
    cwd = os.path.dirname(os.path.abspath(__file__))
    cwd = os.path.dirname(cwd)
    os.popen(f"code {cwd}")