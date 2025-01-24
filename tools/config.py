import argparse
from tools.core import ToolRegistry, Logger, LogLevel, Cache, UserInput

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("config", "base")
    )
    parser.add_argument("--show-experimental-warning", type=str, nargs='?', help="enable or disable the experimental warning")
    parser.add_argument("--set-verbosity", type=int, nargs='?', help=f"set the verbosity level")
    # is either the name of the enum or the value of the enum
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
    elif parsed_args.set_verbosity is not None:
        try:
            value = int(parsed_args.set_verbosity)
            if value < 0 or value > 5:
                raise ValueError
            
            level = LogLevel.from_value()
            config = Cache.getCache("config")
            config['LogLevel'] = level.value
            Cache.saveCache("config",config)
            Logger.set_verbosity(level)
            Logger.log(f"Verbosity level set to {level.name}", LogLevel.INFO)
        except ValueError:
            message = "Invalid value. Use a number between 0 and 5. standing for: "
            for level in LogLevel:
                message += f"{level.name}={level.value}, "
            message = message[:-2]
            print(message)
            return
    else:
        parser.print_help()
    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
