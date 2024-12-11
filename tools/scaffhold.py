import argparse
from tools.core import Logger, LogLevel, ToolRegistry


def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("scaffold")
    )
    parser.add_argument("name", help="Name of the new tool")
    parser.add_argument("-d", "--description", help="Description of the new tool")
    parser.add_argument("-a", "--alias", action="append", help="Alias for the new tool")

    parsed_args = parser.parse_args(args)

    scaffold_path = f"tools/{parsed_args.name}.py"
    scaffold_content = f"""import argparse
from tools.core import ToolRegistry, Logger, LogLevel

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("{parsed_args.name}")
    )
    # Add your arguments here

    parsed_args = parser.parse_args(args)

    Logger.log("Not implemented yet",LogLevel.CRITICAL)
    return

if __name__ == "__main__":
    run()
"""
    
    if ToolRegistry.doesToolExist(parsed_args.name):
        Logger.log(f"Tool or alias with name '{parsed_args.name}' already exists", LogLevel.ERROR)
        return

    ToolRegistry.registerTool(parsed_args.name, parsed_args.description, parsed_args.alias)

    with open(scaffold_path, "w") as f:
        f.write(scaffold_content)
    
    Logger.log(f"Created new tool scaffold at {scaffold_path}", LogLevel.INFO)