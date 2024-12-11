import argparse
from tools.core import ToolRegistry, Logger, LogLevel

def run(args):
    

    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("scaffold")
    )
    # Add your arguments here

    parsed_args = parser.parse_args(args)

    Logger.log("Not implemented yet",LogLevel.CRITICAL)
    return

if __name__ == "__main__":
    run()
