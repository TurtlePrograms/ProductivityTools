import sys
import importlib
import argparse
from tools.core import Logger, LogLevel, ToolRegistry,Cache


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run a tool or list available tools"   
     )
    parser.add_argument("tool", help="The tool to run")
    parser.add_argument("tool_options", nargs=argparse.REMAINDER, help="Options for the tool")

    parsed_args = parser.parse_args(args)

    config = Cache.getCache("config")
    try:
        tool,section = ToolRegistry.getToolInfo(parsed_args.tool,"base")
        script = tool['script']
        if (section != "base"):
            script = section
            parsed_args.tool_options.insert(0,tool['script'])

        if (script is None):
            Logger.log(f"Tool '{parsed_args.tool}' not found.", LogLevel.ERROR)
            return
        
        if not config['showExperimentalWarning']:
            config['showExperimentalWarning'] = True
            Cache.setCache("config",config)

        if ToolRegistry.getToolInfo(parsed_args.tool,section)[0]['isExperimental'] and config['showExperimentalWarning']:
            Logger.log("This tool is experimental and may not work as expected.", LogLevel.WARNING)

        Logger.log(f"Running tool '{script}'", LogLevel.INFO)
        module = importlib.import_module(f"tools.{script}")
        output = module.run(parsed_args.tool_options)
        if output is not None:
            Logger.log(output, LogLevel.NONE)
    except Exception as e:
        Logger.log(f"Error: {e}", LogLevel.ERROR)
        return
    



if __name__ == "__main__":
    main()

