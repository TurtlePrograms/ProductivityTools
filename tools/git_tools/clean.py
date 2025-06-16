import argparse
import subprocess
from tools.core import ToolRegistry, Logger, LogLevel
from tools.core.Input import UserInput


def getBranches():
    try:
        result = subprocess.run(
            ["git", "branch", "--merged"],
            capture_output=True,
            text=True,
            check=True
        )
        all_merged_branches = result.stdout.strip().split('\n')
        filtered_branches = []
        for branch in all_merged_branches:
            branch = branch.strip()
            temp_branch = branch.lower()
            if not temp_branch or temp_branch.startswith('remotes/'):
                continue
            if temp_branch.startswith('*'):
                continue
            if temp_branch.startswith('main') or temp_branch.startswith('master'):
                continue
            filtered_branches.append(branch)
                
        return filtered_branches

      
    except Exception as e:
        Logger.log(f"Error while executing git clean: {e}", LogLevel.ERROR)
        return

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("clean", "git")
    )
    parser.add_argument("-y", "--no-confirm", action="store_true", help="If set, skip the confirmation prompt before committing")

    parsed_args = parser.parse_args(args)

    try:
        branches = getBranches()
        if not branches:
            Logger.log("No branches to clean", LogLevel.INFO)
            return
        Logger.log("Branches to clean:", LogLevel.INFO)
        for branch in branches:
            Logger.log(f" - {branch}", LogLevel.INFO)
        confirmation = UserInput.confirm("Do you want to commit the changes?","y","n") if not parsed_args.no_confirm else True

        if confirmation:
            Logger.log("Cleaning branches...", LogLevel.INFO)
            for branch in branches:
                Logger.log(f"Deleting branch: {branch}", LogLevel.INFO)
                try:
                    subprocess.run(["git", "branch", "-d", branch], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    Logger.log(f"Failed to delete branch {branch}: {e}", LogLevel.ERROR)
                    continue
                Logger.log(f"Branch {branch} deleted successfully", LogLevel.INFO)
        else:
            Logger.log("Branch cleaning aborted.", LogLevel.WARNING)
      
    except Exception as e:
        Logger.log(f"Error while executing git clean: {e}", LogLevel.ERROR)
        return

    Logger.log("Not implemented yet",LogLevel.CRITICAL)
    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
