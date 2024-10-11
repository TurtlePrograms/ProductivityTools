import subprocess
import argparse


def confirm_commit():
    confirmation = input("Do you want to commit these changes? [y/n]: ").strip().lower()
    return confirmation == "y"


def run(args):
    parser = argparse.ArgumentParser(
        description="Quick Commit tool with optional push"
    )
    parser.add_argument("message", help="Commit message for the git commit")
    parser.add_argument("--push", "-p", action="store_true", help="Push after commit")
    parser.add_argument("-y", action="store_true", help="Skip confirmation")

    parsed_args = parser.parse_args(args)

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "status", "-s"])

    # Ask for confirmation
    if confirm_commit() or parsed_args.y:
        print(f"Committing with message: {parsed_args.message}")
        subprocess.run(["git", "commit", "-m", parsed_args.message])

        # Push only if --push flag is provided
        if parsed_args.push:
            print("Pushing to remote repository...")
            subprocess.run(["git", "push"])
    else:
        print("Aborting commit.")
