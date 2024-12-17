import argparse
from tools.core import ToolRegistry, Logger, LogLevel
import os
import time
from colorama import Fore, Style
import fnmatch
from typing import Tuple

def searchFolder(path, pattern, include_folders, debug, countLines, depth=0, recursion_limit=None) -> Tuple[int, int]:
    matches = 0
    lineMatches = 0
    if recursion_limit is not None and depth >= recursion_limit:
        return matches
    
    try:
        items = os.listdir(path)
    except PermissionError:
        return matches
    
    for item in items:
        subpath = os.path.join(path, item)
        if os.path.isdir(subpath):
            if include_folders and fnmatch.fnmatch(item, pattern):
                Logger.log(f"{subpath}",LogLevel.DEBUG) if debug else None
                matches += 1
            (m, l) = searchFolder(subpath, pattern, include_folders, debug, countLines, depth + 1, recursion_limit)
            matches += m
            lineMatches += l
        elif fnmatch.fnmatch(item, pattern):
            Logger.log(Fore.GREEN + f"{subpath}",LogLevel.DEBUG) if debug else None
            lineMatches += CountLines(subpath) if countLines else 0
            matches += 1
    return (matches, lineMatches)

def CountLines(file_path):
    with open(file_path, 'r') as file:
        return len(file.readlines())
    
def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("file-count")
    )
    parser = argparse.ArgumentParser(description='Recursively counts files matching a pattern in a directory')
    parser.add_argument('-p', "--path", type=str, default='.', help='The directory to search from (default: current directory)')
    parser.add_argument('-r', '--recrusion-limit', type=int, default=None, help='The maximum recursion depth')
    parser.add_argument('-f', '--include-folders', action='store_true', help='Include folders in the count')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
    parser.add_argument('-l', '--count-lines', action='store_true', help='Count lines in files')
    parser.add_argument('pattern', nargs='?', default="*", help='Pattern to match files and folders (default: "*")')
    parsed_args = parser.parse_args(args)

    root_path = os.path.abspath(parsed_args.path)
    if not os.path.exists(root_path):
        Logger.log(f"Path '{root_path}' does not exist", LogLevel.CRITICAL)
        return
    
    if parsed_args.pattern:
        parsed_args.pattern = parsed_args.pattern.lower()
    
    Logger.log(f"Searching for '{parsed_args.pattern}' in '{root_path}'...", LogLevel.INFO)
    start_time = time.time()
    matches = searchFolder(root_path, parsed_args.pattern, parsed_args.include_folders, parsed_args.debug, parsed_args.count_lines, recursion_limit=parsed_args.recrusion_limit)
    end_time = time.time()
    elapsed_time = end_time - start_time

    if (parsed_args.count_lines):
        Logger.log(f"Search completed in {elapsed_time:.2f} seconds. Found {matches[0]} matches with a total of {matches[1]} lines.", LogLevel.INFO)
    else:
        Logger.log(f"Search completed in {elapsed_time:.2f} seconds. Found {matches[0]} matches.", LogLevel.INFO)
    return

if __name__ == "__main__":
    Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)

