import argparse
import subprocess
from tools.core import ToolRegistry, Logger, LogLevel,Path

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("open")
    )
    parser.add_argument(
        "--tool",
        type=str,
        choices=["vscode", "explorer"],
        default="vscode",
        help="The tool to open the project in",
    )
    parsed_args = parser.parse_args(args)
    match parsed_args.tool:
        case "vscode":
            subprocess.run(f"code {Path.ROOT_DIR}", shell=True)
        case "explorer":
            subprocess.run(f"explorer {Path.ROOT_DIR}", shell=True)
        case _:
            Logger.log("Not implemented yet",LogLevel.CRITICAL)
    return

if __name__ == "__main__":
    Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)

