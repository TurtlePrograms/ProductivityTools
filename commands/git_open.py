import argparse
import os
import subprocess
import webbrowser


def run(args):
    parser = argparse.ArgumentParser(
        description="Opens the remote repository in the browser"
    )
    parsed_args = parser.parse_args(args)
    result = subprocess.run(
            ["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True
        )
    url = result.stdout.strip().replace("\n","")
    webbrowser.open_new_tab(url)