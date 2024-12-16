import argparse
import webbrowser
from tools.core import ToolRegistry, Logger, LogLevel, GitClient

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("go")
    )
    # Add your arguments here

    parsed_args = parser.parse_args(args)

    webbrowser.open_new_tab(GitClient.getRemoteUrl())

    Logger.log("Not implemented yet",LogLevel.CRITICAL)
    return

if __name__ == "__main__":
    run()
