import argparse
import webbrowser
from tools.core import ToolRegistry, GitClient, Logger, LogLevel

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("open","git")
    )
    parsed_args = parser.parse_args(args)
    webbrowser.open_new_tab(GitClient.getRemoteUrl())
    return

if __name__ == "__main__":
    Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)

