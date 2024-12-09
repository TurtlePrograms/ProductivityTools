import argparse
from tools.core import Cache, Logger, LogLevel

def run(args):
    

    parser = argparse.ArgumentParser(
        description=Cache.getCache("tool_registry")['clone'].get('description')
    )
    # Add your arguments here

    parsed_args = parser.parse_args(args)

    Logger.log("Not implemented yet",LogLevel.CRITICAL)
    return

if __name__ == "__main__":
    run()
