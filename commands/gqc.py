import subprocess
import argparse
import datetime
import os

cwd = os.getcwd().split("\\")[-1]

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def confirm_commit():
    confirmation = input("Do you want to commit these changes? [y/n]: ").strip().lower()
    return confirmation == "y"


def run(args):
    parser = argparse.ArgumentParser(
        description="Quick Commit tool with optional push"
    )
    parser.add_argument("message", help="Commit message for the git commit")
    parser.add_argument("-p", "--push", action="store_true", help="Push after commit")
    parser.add_argument("-y", "--no-confirm", action="store_true", help="Skip confirmation")
    
    parsed_args = parser.parse_args(args)

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "status", "-s"])
    
    # Ask for confirmation
    confirmation = confirm_commit() if not parsed_args.no_confirm else True
    if confirmation:
        print(f"Committing with message: {parsed_args.message}")
        subprocess.run(["git", "commit", "-m", parsed_args.message])
        subprocess.run(["python",f"{script_dir}/main.py","note",str(datetime.date.today())+"-commits",cwd+" : "+parsed_args.message,"-a"])
        # Push only if --push flag is provided
        if parsed_args.push:
            print("Pushing to remote repository...")
            subprocess.run(["git", "push"])
    else:
        print("Aborting commit.")
    
    
