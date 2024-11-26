import os

# Base directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
COMMANDS_DIR = os.path.join(PROJECT_ROOT, "commands")
CACHE_DIR = os.path.join(PROJECT_ROOT, "pt-cache")

# Utility functions
def get_command_path(command_name):
    """Get the path to a specific command file."""
    return os.path.join(COMMANDS_DIR, f"{command_name}.py")

def get_cache_file(cache_name):
    """Get the path to a specific cache file."""
    return os.path.join(CACHE_DIR, f"{cache_name}.json")

def change_to_root_dir():
    change_to_dir(PROJECT_ROOT)

def change_to_commands_dir():
    change_to_dir(COMMANDS_DIR)

def change_to_cache_dir():
    change_to_dir(CACHE_DIR)

def change_to_dir(directory):
    os.chdir(directory)