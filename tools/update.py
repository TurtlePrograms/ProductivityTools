import argparse
import os
import subprocess
from tools.core import ToolRegistry, Logger, LogLevel, GitClient, Path,Cache
import json

CONFIG_DEFAULT = {
    "showExperimentalWarning": True,
    "LogLevel": LogLevel.DEBUG.value
}
IGNORE_FOLDERS_DEFAULT = {"folders":[
    "node_modules",
    "bower_components",
    "dist",
    "build",
    "out",
    "target",
    "tmp",
    "temp",
    "__pycache__",
    ".vscode",	
    ".git"
]}


def initConfig(reset=False):
    if not os.path.exists(Path.CONFIG_DIR):
        os.makedirs(Path.CONFIG_DIR)
        Logger.log("Configuration directory created", LogLevel.INFO)
    
    if not os.path.exists(Path.CACHE_DIR):
        os.makedirs(Path.CACHE_DIR)
        Logger.log("Cache directory created", LogLevel.INFO)

    if not os.path.exists(Cache.getFilePath("config")) or reset:
        with open(Cache.getFilePath("config"), "w") as f:
            f.write(json.dumps(CONFIG_DEFAULT))
            Logger.log("Configuration file created", LogLevel.INFO)
    
    config = {}
    with open(Cache.getFilePath("config"), "r") as f:
        config = json.load(f)
        for key in CONFIG_DEFAULT:
            if key not in config:
                config[key] = CONFIG_DEFAULT[key]
    with open(Cache.getFilePath("config"), "w") as f:
        f.write(json.dumps(config))
        Logger.log("Configuration file updated", LogLevel.INFO)
        

    
    if not os.path.exists(Cache.getFilePath("IgnoreFolders")) or reset:
        with open(Cache.getFilePath("IgnoreFolders"), "w") as f:
            f.write(json.dumps(IGNORE_FOLDERS_DEFAULT))
            Logger.log("IgnoreFolders file created", LogLevel.INFO)

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("update", "base")
    )
    parser.add_argument("--reset", action="store_true", help="Reset configuration files")
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
    Logger.log("Dependencies updated", LogLevel.INFO)

    initConfig(parsed_args.reset)

    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
