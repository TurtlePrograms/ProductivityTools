import argparse
from tools.core import ToolRegistry, Logger, LogLevel, Cache, UserInput

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("config", "base")
    )
    parser.add_argument("--show-experimental-warning", type=str, nargs='?', help="enable or disable the experimental warning")
    parsed_args = parser.parse_args(args)

    if parsed_args.show_experimental_warning is not None:
        try:
            enabled = UserInput.convertToBool(parsed_args.show_experimental_warning)
            config = Cache.getCache("config")
            config['showExperimentalWarning'] = enabled
            Cache.saveCache("config",config)
            if enabled:
                Logger.log("Experimental warning enabled", LogLevel.INFO)
            else:
                Logger.log("Experimental warning disabled", LogLevel.INFO)
        except ValueError:
            Logger.log("Invalid value. Use 'true' or 'false'", LogLevel.ERROR)
            return
    else:
        parser.print_help()
    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
