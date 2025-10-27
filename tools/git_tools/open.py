import argparse
import webbrowser
from tools.core import ToolRegistry, GitClient, Logger, LogLevel


def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("open", "git")
    )
    parser.add_argument(
        "-b",
        "--branch",
        type=str,
        nargs="?",
        const="CURRENT_BRANCH",  # Used if -b is provided but no value
        help="open git to this branch",
    )

    parsed_args = parser.parse_args(args)
    url = GitClient.getRemoteUrl()

    if parsed_args.branch is not None:
        if parsed_args.branch == "CURRENT_BRANCH":
            branch = GitClient.getCurrentBranch()
        else:
            branch = parsed_args.branch
        url = url + "/tree/" + branch

    webbrowser.open_new_tab(url)


if __name__ == "__main__":
    Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
