import subprocess
import argparse
import os
import sys
import importlib
from pathlib import Path

def run(args):
    parser = argparse.ArgumentParser(
        description="Updates the project by pulling the latest changes from the repository"
    )
    parsed_args = parser.parse_args(args)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Change the current working directory to the script's directory
    os.chdir(script_dir)

    # Virtual environment setup
    venv_dir = os.path.join(os.path.dirname(script_dir), "venv")
    python_bin = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python")

    try:
        # Check if the virtual environment exists, if not, create it
        if not os.path.exists(venv_dir):
            print("Virtual environment not found. Creating one...")
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            print("Virtual environment created.")

        # Ensure pip is up to date in the virtual environment
        print("Updating pip in the virtual environment...")
        subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pip"], check=True)

        # Pull the latest changes from the repository
        print("Updating the project by pulling the latest changes from the repository...")
        result = subprocess.run(
            ["git", "pull"], check=True, capture_output=True, text=True
        )
        print(result.stdout)
        print("Update successful.")

        # Run requirements generation
        try:
            module = importlib.import_module("commands.generate_requirements")
            module.run(["./"])
        except:
            print("failed to import reuquirements")

        # Install the requirements
        print("Installing dependencies from requirements.txt...")
        requirements_path = os.path.join(script_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            subprocess.run([python_bin, "-m", "pip", "install", "-r", requirements_path], check=True)
        else:
            print("No requirements.txt file found, skipping installation.")

        # Re-import the help module to update the cache
        print("Refreshing the command list...")
        try:
            module = importlib.import_module("commands.help")
            module.run(["--no-cache"])
        except:
            print("failed to import help")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run(sys.argv[1:])
