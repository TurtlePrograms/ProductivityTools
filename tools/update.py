import argparse
import os
import subprocess
from tools.core import ToolRegistry, Logger, LogLevel, GitClient, Path

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("update", "base")
    )
    parsed_args = parser.parse_args(args)

    os.chdir(Path.ROOT_DIR)
    Logger.log("Pulling latest changes from remote repository", LogLevel.INFO)
    GitClient.pull()

    if not os.path.exists(Path.VENV_DIR):
        Logger.log("Creating virtual environment", LogLevel.INFO)
        subprocess.run(["python", "-m", "venv", Path.VENV_DIR], check=True)
        Logger.log("Virtual environment created", LogLevel.INFO)
    else:
        Logger.log("Virtual environment already exists", LogLevel.INFO)
    
    Logger.log("Updating dependencies", LogLevel.INFO)
    subprocess.run([os.path.join(Path.VENV_DIR, "Scripts", "pip"), "install", "-r", "requirements.txt"], check=True)

    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
