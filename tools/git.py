import argparse
import importlib
from tools.core import ToolRegistry, Logger, LogLevel
from tools.git_tools.open import run

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("git")
    )
    parser.add_argument("tool", help="The tool to run")
    parser.add_argument("tool_options", nargs=argparse.REMAINDER, help="Options for the tool")

    parsed_args = parser.parse_args(args)
    tool = ToolRegistry.getToolInfo(parsed_args.tool, "git")[0]
    if tool is None:
        Logger.log(f"Tool '{parsed_args.tool}' not found.", LogLevel.ERROR)
        return
    try:
        Logger.log(f"Running Git tool '{parsed_args.tool}'", LogLevel.INFO)
        module = importlib.import_module(f"tools.git_tools.{tool["script"]}")
        module.run(parsed_args.tool_options)

    except Exception as e:
        Logger.log(f"Error: {e}", LogLevel.ERROR)


    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
