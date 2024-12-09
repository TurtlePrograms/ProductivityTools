import argparse
from tools.core import GitClient, Logger, LogLevel, Confirm

def run(args):
    parser = argparse.ArgumentParser(
        description="Quick Commit tool with optional push"
    )
    parser.add_argument("message", help="Commit message for the git commit")
    parser.add_argument("-p", "--push", action="store_true", help="Push after commit")
    parser.add_argument("-y", "--no-confirm", action="store_true", help="Skip confirmation")
    
    parsed_args = parser.parse_args(args)
    try:
        Logger.log("Staging changes...",LogLevel.INFO)
        GitClient.Add()

        Logger.log("Checking status of staged changes...",LogLevel.INFO)
        GitClient.Status()
        confirmation = Confirm.confirm("Do you want to commit the changes?","y","n") if not parsed_args.no_confirm else True

        if confirmation:
            Logger.log(f"Committing with message: '{parsed_args.message}'",LogLevel.INFO)
            GitClient.Commit(parsed_args.message)

            if parsed_args.push:
                Logger.log("Pushing to remote repository...",LogLevel.INFO)
                GitClient.Push()
        else:
            Logger.log("Commit aborted.",LogLevel.WARNING)
    except Exception as e:
        Logger.log(f"Error while executing command: {e}",LogLevel.CRITICAL)
        return
