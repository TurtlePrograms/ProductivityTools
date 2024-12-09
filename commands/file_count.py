import os
import argparse
import time
from colorama import Fore, Style
import fnmatch

def searchFolder(path, pattern, include_folders, debug, depth=0, recursion_limit=None) -> int:
    matches = 0
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
                print(Fore.BLUE + f"{subpath}") if debug else None
                matches += 1
            matches += searchFolder(subpath, pattern, include_folders, debug, depth + 1, recursion_limit)
        elif fnmatch.fnmatch(item, pattern):
            print(Fore.GREEN + f"{subpath}") if debug else None
            matches += 1
    return matches

def run(command_args):
    parser = argparse.ArgumentParser(description='Generate and print directory tree.')
    parser.add_argument('-p', "--path", type=str, default='.', help='The root directory to start the tree from (default: current directory)')
    parser.add_argument('-r', '--recrusion-limit', type=int, default=None, help='The maximum recursion depth')
    parser.add_argument('-f', '--include-folders', action='store_true', help='Include folders in the tree')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
    parser.add_argument('pattern', nargs='?', default=None, help='Pattern to match files and folders')
    args = parser.parse_args(command_args)

    root_path = os.path.abspath(args.path)
    if not os.path.exists(root_path):
        print(Fore.RED + f"Error: Path '{root_path}' does not exist.")
        return
    
    if args.pattern:
        args.pattern = args.pattern.lower()
    
    print(Fore.CYAN + f"Searching for '{args.pattern}' in '{root_path}'...")
    start_time = time.time()
    matches = searchFolder(root_path, args.pattern, args.include_folders, args.debug, recursion_limit=args.recrusion_limit)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(Fore.CYAN + f"Search completed in {elapsed_time:.2f} seconds. Found {matches} matches.")
    print(Style.RESET_ALL)

    