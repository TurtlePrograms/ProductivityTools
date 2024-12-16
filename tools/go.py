import argparse
import webbrowser
from tools.core import ToolRegistry, GitClient

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("go")
    )
    parsed_args = parser.parse_args(args)

    webbrowser.open_new_tab(GitClient.getRemoteUrl())
    return

if __name__ == "__main__":
    run()
