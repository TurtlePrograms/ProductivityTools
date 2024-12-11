import sys
import importlib
import argparse
from tools.core import Logger, LogLevel, ToolRegistry


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Run a tool or list available tools")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="List available tools")
    group.add_argument("tool", nargs="?", help="The tool to run")
    
    parser.add_argument("tool_options", nargs=argparse.REMAINDER, help="Options for the tool")
    
    parsed_args = parser.parse_args(args)

    if parsed_args.list:
        try:
            tools = ToolRegistry.getTools()

            # Display the tools
            Logger.log("Available tools:")
            Logger.log("----------------")

            for tool in tools:
                Logger.log(f"Tools: {tool}")
                Logger.log(f"  Description: {tools[tool]['description']}")
                if tools[tool]['aliases'] != []:
                    Logger.log(f"  Aliases: {str.join(', ', tools[tool]['aliases'])}")
                Logger.log()
        except Exception as e:
            Logger.log(f"Error: {e}", LogLevel.ERROR)
            return        
    elif parsed_args.tool:
        try:
            script = ToolRegistry.getScript(parsed_args.tool)
            if (script is None):
                Logger.log(f"Tool '{parsed_args.tool}' not found.", LogLevel.ERROR)
                return
            Logger.log(f"Running tool '{parsed_args.tool}'", LogLevel.INFO)
            module = importlib.import_module(f"tools.{script}")
            output = module.run(parsed_args.tool_options)
            if output is not None:
                Logger.log(output, LogLevel.NONE)
        except Exception as e:
            Logger.log(f"Error: {e}", LogLevel.ERROR)
            return
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
