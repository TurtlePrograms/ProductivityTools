import sys
import importlib
import argparse
from tools.core import Logger, LogLevel, ToolRegistry,Cache


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run a tool or list available tools"   
     )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="List available tools")
    group.add_argument("tool", nargs="?", help="The tool to run")
    
    parser.add_argument("tool_options", nargs=argparse.REMAINDER, help="Options for the tool")

    parsed_args = parser.parse_args(args)

    config = Cache.getCache("config")
    if parsed_args.list:
        try:
            tools = ToolRegistry.getTools()

            # Display the tools
            Logger.log("Available Tools")
            Logger.log("=" * 50)

            for tool, details in tools.items():
                Logger.log(f"Tool Name:         {tool}")
                Logger.log(f"Description:       {details['description']}")
                aliases = ", ".join(details['aliases']) if details['aliases'] else "None"
                Logger.log(f"Aliases:           {aliases}")
                is_exp_message = "Yes" if details['isExperimental'] else "No"
                Logger.log(f"Experimental:      {is_exp_message}")
                Logger.log(f"Documentation:     {details['documentation']}")
                Logger.log("-" * 50)

        except Exception as e:
            Logger.log(f"Error: {e}", LogLevel.ERROR)
            return        
    elif parsed_args.tool:
        try:
            script = ToolRegistry.getScript(parsed_args.tool)
            if (script is None):
                Logger.log(f"Tool '{parsed_args.tool}' not found.", LogLevel.ERROR)
                return
            
            if not config['showExperimentalWarning']:
                config['showExperimentalWarning'] = True
                Cache.setCache("config",config)

            if ToolRegistry.getToolInfo(parsed_args.tool)['isExperimental'] and config['showExperimentalWarning']:
                Logger.log("This tool is experimental and may not work as expected.", LogLevel.WARNING)

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

