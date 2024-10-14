import subprocess
import argparse
import os
import importlib

def run(args):
    parser = argparse.ArgumentParser(
        description="Updates the project by pulling the latest changes from the repository"
    )
    parsed_args = parser.parse_args(args)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Change the current working directory to the script's directory
    os.chdir(script_dir)

    try:
        print(
            "Updating the project by pulling the latest changes from the repository..."
        )
        # Run the `git pull` command
        result = subprocess.run(
            ["git", "pull"], check=True, capture_output=True, text=True
        )
        print(result.stdout)
        print("Update successful.")

        # Re-import the help module to update the cache
        print("command list:")
        module = importlib.import_module("commands.help")
        module.run(["--no-cache"])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while updating: {e.stderr}")
