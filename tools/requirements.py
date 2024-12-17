import argparse
import subprocess
from tools.core import ToolRegistry, Logger, LogLevel

def installRequirements(file:str):
    subprocess.run(f"pip install -r {file}", shell=True)

def updateRequirements(file:str):
    subprocess.run(f"pip install --upgrade -r {file}", shell=True)

def generateRequirements(file:str):
     subprocess.run(f"pip freeze > {file}", shell=True)


def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("requirements")
    )
    parser.add_argument("mode", choices=["install", "update","generate"], help="The mode to run the requirements in")
    parser.add_argument("--file", type=str, help="The requirements file to use", default="requirements.txt")
    parsed_args = parser.parse_args(args)

    match parsed_args.mode:
        case "install":
            installRequirements(parsed_args.file)
        case "update":
            updateRequirements(parsed_args.file)
        case "generate":
            generateRequirements(parsed_args.file)
              
    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
