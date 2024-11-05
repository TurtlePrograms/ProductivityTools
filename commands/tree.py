import os
import argparse
import time

# THIS SCIPT IS 90% MADE BY COPILOT
# AND 10% BY SOMEONE ELSE

class treeMap:
    tree = {}
    path = ''
    numFiles = 0
    numDirs = 0
    def __init__(self, path):
        self.path = path

def map_tree(args,startpath: str, depth: int = 0) -> dict:
    tree = {}
    if args.recrusion_limit and depth >= args.recrusion_limit:
        return None
    try:
        items = os.listdir(startpath)
        for item in items:
            path = os.path.join(startpath, item)
            if os.path.isdir(path):
                tree[item] = map_tree(args,path, depth + 1)
            elif args.map_files:
                tree[item] = None
        return tree
    except PermissionError:
        return None

def tree_to_list(tree: dict, prefix='') -> list:
    tree_list = []
    items = list(tree.keys())
    for index, item in enumerate(items):
        if index == len(items) - 1:
            connector = '\\-'
        else:
            connector = '|-'
        if isinstance(tree[item], dict):
            tree_list.append(f"{prefix}{connector}{item}/")
            new_prefix = prefix + ("  " if connector == '\\-' else "| ")
            tree_list.extend(tree_to_list(tree[item], new_prefix))
        else:
            tree_list.append(f"{prefix}{connector}{item}")
    return tree_list

def print_tree(tree: dict):
    tree_list = tree_to_list(tree)
    treestr = '\n'.join(tree_list)
    print(treestr)
    
    # print(f"\n{tree.numDirs} directories, {tree.numFiles} files")

def write_file(tree: dict, file, prefix=''):
    tree_list = tree_to_list(tree, prefix)
    treestr = '\n'.join(tree_list)
    file.write(treestr)
    

def run(command_args):
    parser = argparse.ArgumentParser(description='Generate and print directory tree.')
    parser.add_argument('-p', "--path", type=str, default='.', help='The root directory to start the tree from (default: current directory)')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file to write the tree to (optional)')
    parser.add_argument('-f', '--map-files', action='store_true', help='Include files in the tree')
    parser.add_argument('--no-print', action='store_true', help='Do not print the tree')
    parser.add_argument('-r', '--recrusion-limit', type=int, default=None, help='The maximum depth of the tree')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
    args = parser.parse_args(command_args)
    stime = time.time()
    start_directory = args.path
    print(f"Generating tree for {start_directory}") if args.debug else None
    tree_structure = map_tree(args,start_directory)
    print("Tree generated") if args.debug else None
    eTime = time.time()
    print(f"Time taken: {round(eTime - stime)} seconds") if args.debug else None
    
    if not args.no_print:
        print_tree(tree_structure)

    if args.output:
        with open(args.output, 'w') as file:
            write_file(tree_structure, file)