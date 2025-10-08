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

def getLocalBranches():
    try:
        result = subprocess.run(
            ["git", "branch"],
            capture_output=True,
            text=True,
            check=True
        )
        branches = [b.strip() for b in result.stdout.strip().split('\n') if not b.startswith('*')]
        return branches
    except Exception as e:
        Logger.log(f"Error getting local branches: {e}", LogLevel.ERROR)
        return []

def getRemoteBranches():
    try:
        # Update local info about remote branches
        subprocess.run(["git", "fetch", "--prune"], check=True, capture_output=True, text=True)
        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True,
            check=True
        )
        branches = []
        for b in result.stdout.strip().split('\n'):
            parts = b.strip().split('/')[1::]
            branch = "/".join(parts)
            branches.append(branch)
        return branches
    except Exception as e:
        Logger.log(f"Error getting remote branches: {e}", LogLevel.ERROR)
        return []

def getStaleLocalBranches():
    local_branches = getLocalBranches()
    remote_branches = getRemoteBranches()
    stale_branches = []
    for branch in local_branches:
        temp_branch = branch.lower()
        if temp_branch.startswith('main') or temp_branch.startswith('master'):
            continue
        if branch not in remote_branches:
            stale_branches.append(branch)
    return stale_branches

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("clean", "git")
    )
    parser.add_argument("-y", "--no-confirm", action="store_true", help="Skip confirmation prompts")
    parsed_args = parser.parse_args(args)

    try:
        # Step 1: Delete merged branches
        branches = getBranches()
        if branches:
            Logger.log("Merged branches to clean:", LogLevel.INFO)
            for branch in branches:
                Logger.log(f" - {branch}", LogLevel.INFO)
            confirmation = UserInput.confirm("Delete merged branches?", "y", "n") if not parsed_args.no_confirm else True
            if confirmation:
                for branch in branches:
                    try:
                        subprocess.run(["git", "branch", "-d", branch], check=True, capture_output=True, text=True)
                        Logger.log(f"Branch {branch} deleted successfully", LogLevel.INFO)
                    except subprocess.CalledProcessError as e:
                        Logger.log(f"Failed to delete branch {branch}: {e}", LogLevel.ERROR)
        else:
            Logger.log("No merged branches found",LogLevel.INFO)
        
        # Step 2: Delete stale branches
        stale_branches = getStaleLocalBranches()
        if stale_branches:
            Logger.log("Local branches not on remote:", LogLevel.INFO)
            for branch in stale_branches:
                Logger.log(f" - {branch}", LogLevel.INFO)
            confirmation = UserInput.confirm("Delete stale local branches?", "y", "n") if not parsed_args.no_confirm else True
            if confirmation:
                for branch in stale_branches:
                    try:
                        subprocess.run(["git", "branch", "-D", branch], check=True, capture_output=True, text=True)
                        Logger.log(f"Branch {branch} deleted successfully", LogLevel.INFO)
                    except subprocess.CalledProcessError as e:
                        Logger.log(f"Failed to delete branch {branch}: {e}", LogLevel.ERROR)
        else:
            Logger.log("No stale local branches found.", LogLevel.INFO)

    except Exception as e:
        Logger.log(f"Error while executing git clean: {e}", LogLevel.ERROR)
