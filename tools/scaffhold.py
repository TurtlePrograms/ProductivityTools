import argparse
import tools.core as core


def run(args):
    parser = argparse.ArgumentParser(
        description="Tool to create a new tool scaffold"
    )
    parser.add_argument("name", help="Name of the new tool")
    parser.add_argument("-d", "--description", help="Description of the new tool")
    parser.add_argument("-a", "--alias", action="append", help="Alias for the new tool")

    parsed_args = parser.parse_args(args)

    scaffold_path = f"tools/{parsed_args.name}.py"
    scaffold_content = f"""import argparse
from tools.core import Cache, Logger, LogLevel

def run(args):
    parser = argparse.ArgumentParser(
        description=Cache.getCache("tool_registry")['{parsed_args.name}'].get('description')
    )
    # Add your arguments here

    parsed_args = parser.parse_args(args)

    Logger.log("Not implemented yet",LogLevel.CRITICAL)
    return

if __name__ == "__main__":
    run()
"""

    
    registry = core.Cache.getCache("tool_registry")

    if parsed_args.name in registry:
        core.Logger.log(f"Tool '{parsed_args.name}' already exists", core.LogLevel.ERROR)
        return

    registry[parsed_args.name] = {
        "description": parsed_args.description,
        "script": parsed_args.name.lower().replace(" ", "_"),
    }
    if not parsed_args.alias:
        parsed_args.alias = []
    for alias in parsed_args.alias:
        if alias in registry:
            core.Logger.log(f"Alias '{alias}' already exists", core.LogLevel.ERROR)
            continue
        registry[alias] = {
            "description": parsed_args.description,
            "script": parsed_args.name.lower().replace(" ", "_"),
        }
    core.Cache.saveCache("tool_registry", registry)
    with open(scaffold_path, "w") as f:
        f.write(scaffold_content)
    core.Logger.log(f"Created new tool scaffold at {scaffold_path}", core.LogLevel.INFO)