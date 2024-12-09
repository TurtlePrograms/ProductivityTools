import argparse
import tools.core as core


def run(args):
    parser = argparse.ArgumentParser(
        description="Quick Commit tool with optional push"
    )
    parser.add_argument("message", help="Commit message for the git commit")
    parser.add_argument("-p", "--push", action="store_true", help="Push after commit")
    parser.add_argument("-y", "--no-confirm", action="store_true", help="Skip confirmation")
    
    parsed_args = parser.parse_args(args)
    try:
        core.Logger.log("Staging changes...",core.LogLevel.INFO)
        core.GitClient.Add()

        core.Logger.log("Checking status of staged changes...",core.LogLevel.INFO)
        core.GitClient.Status()
        confirmation = core.Confirm.confirm("Do you want to commit the changes?","y","n") if not parsed_args.no_confirm else True

        if confirmation:
            core.Logger.log(f"Committing with message: '{parsed_args.message}'",core.LogLevel.INFO)
            core.GitClient.Commit(parsed_args.message)

            if parsed_args.push:
                core.Logger.log("Pushing to remote repository...",core.LogLevel.INFO)
                core.GitClient.Push()
        else:
            core.Logger.log("Commit aborted.",core.LogLevel.WARNING)
    except Exception as e:
        core.Logger.log(f"Error while executing command: {e}",core.LogLevel.CRITICAL)
        return
