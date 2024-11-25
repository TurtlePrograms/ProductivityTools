import subprocess
import argparse
import datetime
import os
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

cwd = os.getcwd().split("\\")[-1]
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def confirm_commit():
    confirmation = input(Fore.YELLOW + "Do you want to commit these changes? [y/n]: ").strip().lower()
    return confirmation == "y"

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

def run(args):
    parser = argparse.ArgumentParser(
        description="Quick Commit tool with optional push"
    )
    parser.add_argument("message", help="Commit message for the git commit")
    parser.add_argument("-p", "--push", action="store_true", help="Push after commit")
    parser.add_argument("-y", "--no-confirm", action="store_true", help="Skip confirmation")
    
    parsed_args = parser.parse_args(args)

    print(Fore.BLUE + "Staging changes...")
    if run_git_command(["git", "add", "."], "git add") != 0:
        print(Fore.RED + "Failed to stage changes. Exiting.")
        return

    print(Fore.BLUE + "Checking status of staged changes...")
    if run_git_command(["git", "status", "-s"], "git status") != 0:
        print(Fore.RED + "Failed to get status. Exiting.")
        return

    confirmation = confirm_commit() if not parsed_args.no_confirm else True
    if confirmation:
        print(Fore.BLUE + f"Committing with message: '{parsed_args.message}'")
        if run_git_command(["git", "commit", "-m", parsed_args.message], "git commit") != 0:
            print(Fore.RED + "Failed to commit changes. Exiting.")
            return

        try:
            subprocess.run(
                ["python", f"{script_dir}/main.py", "note", f"{datetime.date.today()}-commits", f"{cwd} : {parsed_args.message}"],
                check=True
            )
            print(Fore.GREEN + "Note logged successfully.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "Error while logging note:")
            print(Fore.RED + str(e))

        if parsed_args.push:
            print(Fore.BLUE + "Pushing to remote repository...")
            if run_git_command(["git", "push"], "git push") != 0:
                print(Fore.RED + "Failed to push changes.")
    else:
        print(Fore.YELLOW + "Commit aborted.")

# For clarity, the script uses these colors:
# - GREEN for success
# - RED for errors
# - BLUE for progress/status messages
# - YELLOW for warnings or prompts
