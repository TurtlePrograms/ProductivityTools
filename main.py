import sys
import importlib
import argparse
import tools.core as core


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Run a tool or list available tools")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="List available tools")
    group.add_argument("tool", nargs="?", help="The tool to run")
    
    parser.add_argument("tool_options", nargs=argparse.REMAINDER, help="Options for the tool")
    
    parsed_args = parser.parse_args(args)

    if parsed_args.list:
        try:
            tools = core.Cache.getCache("tool_registry")
            grouped_tools = {}
            for tool_name, tool_info in tools.items():
                script = tool_info["script"]
                if script not in grouped_tools:
                    grouped_tools[script] = {
                        "description": tool_info["description"],
                        "tools": []
                    }
                grouped_tools[script]["tools"].append(tool_name)

            # Display the tools
            core.Logger.log("Available tools:")
            core.Logger.log("----------------")

            for script, info in grouped_tools.items():
                tool_names = ", ".join(info["tools"])
                core.Logger.log(f"Tools: {tool_names}")
                core.Logger.log(f"  Description: {info['description']}")
                core.Logger.log()
        except Exception as e:
            core.Logger.log(f"Error: {e}", core.LogLevel.ERROR)
            return        
    elif parsed_args.tool:
        try:
            tools = core.Cache.getCache("tool_registry")

            if (parsed_args.tool not in tools):
                core.Logger.log(f"Tool '{parsed_args.tool}' not found.", core.LogLevel.ERROR)
                return
            
            tool = tools.get(parsed_args.tool)
            if tool is None:
                core.Logger.log(f"Tool '{parsed_args.tool}' not found.", core.LogLevel.ERROR)
                return
            core.Logger.log(f"Running tool '{parsed_args.tool}'", core.LogLevel.INFO)
            module = importlib.import_module(f"tools.{tool["script"]}")
            module.run(parsed_args.tool_options)
        except Exception as e:
            core.Logger.log(f"Error: {e}", core.LogLevel.ERROR)
            return
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
