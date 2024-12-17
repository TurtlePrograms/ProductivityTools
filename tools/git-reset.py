import argparse
import os

from colorama import Fore
from tools.core import ToolRegistry,GitClient,UserInput,Logger,LogLevel

def delete_files(path):
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if file == ".git":
            continue
        elif os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            delete_files(filepath)
            os.rmdir(filepath)


def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("git-reset")
    )
    parsed_args = parser.parse_args(args)

    if not os.path.exists(".git"):
        Logger.log("Not a git repository",LogLevel.CRITICAL)
        return
    
    GitClient.Status()

    UserInput.confirm("Are you sure you want to reset the repository? (Destructive and cant be undone)","yes","no")

    Logger.log("Resetting repository...",LogLevel.INFO)

    try:
        delete_files(os.getcwd())
    except Exception as e:
        Logger.log("Error while deleting files",LogLevel.ERROR)
        Logger.log(e,LogLevel.ERROR)
        return
    
    GitClient.Reset(["--hard"])
    GitClient.Clean(["-fd"])

    Logger.log("Repository reset successfully",LogLevel.INFO)
    return

if __name__ == "__main__":
    Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)

