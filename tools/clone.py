import argparse
import tools.core as core

def run(args):
    

    parser = argparse.ArgumentParser(
        description=core.Cache.getCache("tool_registry")['clone'].get('description')
    )
    # Add your arguments here

    parsed_args = parser.parse_args(args)

    core.Logger.log("Not implemented yet",core.LogLevel.CRITICAL)
    return

if __name__ == "__main__":
    run()
