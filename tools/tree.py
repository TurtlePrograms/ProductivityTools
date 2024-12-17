import argparse
from tools.core import ToolRegistry, Cache, Logger, LogLevel
import os
import time
from colorama import Fore, Style

folderIgnore = Cache.getCache('IgnoreFolders').get('folders', [])

class treeItem:
    Name = ""
    IsDir = False
    CanRead = False
    CanWrite = False
    CanExecute = False

def create_tree_item(path: str) -> treeItem:
    item = treeItem()
    item.Name = os.path.basename(path)
    item.IsDir = os.path.isdir(path)
    item.CanRead = os.access(path, os.R_OK)
    item.CanWrite = os.access(path, os.W_OK)
    item.CanExecute = os.access(path, os.X_OK)
    return item

def map_tree(args, startpath: str, depth: int = 0) -> dict:
    tree = {}
    if args.recrusion_limit and depth >= args.recrusion_limit:
        return tree
    try:
        items = os.listdir(startpath)
        for item in items:
            path = os.path.join(startpath, item)
            tree_item = create_tree_item(path)
            if os.path.isdir(path):
                if path.split("\\")[-1].startswith(".") or path.split("\\")[-1] in folderIgnore:
                    tree[tree_item.Name] = {}
                else:
                    tree[tree_item.Name] = map_tree(args, path, depth + 1)
            elif args.map_files:
                tree[tree_item.Name] = tree_item
        return tree
    except PermissionError:
        return tree

def tree_to_list(tree: dict, noColor: bool, prefix='') -> list:
    tree_list = []
    items = list(tree.keys())
    for index, item in enumerate(items):
        if index == len(items) - 1:
            connector = '\-'
        else:
            connector = '|-'
        tree_item = tree[item]
        if isinstance(tree_item, dict):
            if noColor:
                tree_list.append(f"{prefix}{connector}{item}")
            else:
                tree_list.append(f"{prefix}{connector}{Fore.LIGHTBLUE_EX}{item}/{Fore.RESET}")
            new_prefix = prefix + ("  " if connector == '\-' else "| ")
            tree_list.extend(tree_to_list(tree_item, noColor, new_prefix))
        else:
            if noColor:
                tree_list.append(f"{prefix}{connector}{item}")
            elif tree_item.CanRead and not tree_item.CanWrite:
                tree_list.append(f"{prefix}{connector}{Fore.LIGHTYELLOW_EX}{item}{Fore.RESET}")
            elif not tree_item.CanRead:
                tree_list.append(f"{prefix}{connector}{Fore.LIGHTRED_EX}{item}{Fore.RESET}")
            else:
                tree_list.append(f"{prefix}{connector}{item}")
    return tree_list

def print_tree(rootPath: str, tree: dict, noColor: bool):
    tree_list = tree_to_list(tree, noColor)
    base_root_path = os.path.basename(os.path.abspath(rootPath))
    if noColor:
        treestr = f"{base_root_path}/\n" + '\n'.join(tree_list)
    else:
        treestr = f"{Fore.LIGHTBLUE_EX}{base_root_path}/{Fore.RESET}\n" + '\n'.join(tree_list)
    Logger.log(treestr, LogLevel.NONE)
    
def write_file(rootPath: str, tree: dict, file):
    tree_list = tree_to_list(tree, True)
    base_root_path = os.path.basename(os.path.abspath(rootPath))
    treestr = f"{base_root_path}/\n" + '\n'.join(tree_list)
    file.write(treestr)


def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("tree")
    )
    parser.add_argument('-p', "--path", type=str, default='.', help='The root directory to start the tree from (default: current directory)')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file to write the tree to (optional)')
    parser.add_argument('-f', '--map-files', action='store_true', help='Include files in the tree')
    parser.add_argument('--no-print', action='store_true', help='Do not print the tree')
    parser.add_argument('-r', '--recrusion-limit', type=int, default=None, help='The maximum depth of the tree')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    parsed_args = parser.parse_args(args)
    stime = time.time()
    start_directory = parsed_args.path
    Logger.log(f"Generating tree for {start_directory}",LogLevel.DEBUG) if parsed_args.debug else None
    tree_structure = map_tree(parsed_args,start_directory)
    Logger.log("Tree generated",LogLevel.DEBUG) if parsed_args.debug else None
    eTime = time.time()
    Logger.log(f"Time taken: {round(eTime - stime)} seconds",LogLevel.DEBUG) if parsed_args.debug else None
    
    if not parsed_args.no_print:
        print_tree(parsed_args.path, tree_structure, parsed_args.no_color)

    if parsed_args.output:
        with open(parsed_args.output, 'w') as file:
            write_file(parsed_args.path, tree_structure, file)
    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
