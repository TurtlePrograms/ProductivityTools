import argparse
import os
import subprocess
import webbrowser

from colorama import Fore, init

# Initialize colorama for cross-platform support
init(autoreset=True)

def confirm():
    print(Fore.RED + "WARNING: This action is destructive and cannot be undone!")
    confirmation = input(Fore.YELLOW + "Do you want to reset this repository? Type 'yes' to confirm: ").strip().lower()
    return confirmation == "yes"

def run_git_command(command, description="Git command"):
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )
        print(Fore.GREEN + result.stdout)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error while executing {description}:")
        print(Fore.RED + e.stderr)
        return e.returncode

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
        description="Resets the repository by deleting all files and performing a hard reset"
    )
    parsed_args = parser.parse_args(args)

    if not confirm():
        print(Fore.RED + "Action aborted by the user.")
        return

    if not os.path.exists(".git"):
        print(Fore.RED + "This directory is not a git repository.")
        return

    print(Fore.BLUE + "Resetting repository...")

    cwd = os.getcwd().split("\\")[-1]
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        delete_files(cwd)
    except Exception as e:
        print(Fore.RED + f"Error while resetting repository:")
        print(Fore.RED + str(e))
        return
    
    run_git_command(["git", "reset", "--hard"], "git reset")
    run_git_command(["git", "clean", "-fd"], "git clean")

    print(Fore.GREEN + "Repository reset successfully")
