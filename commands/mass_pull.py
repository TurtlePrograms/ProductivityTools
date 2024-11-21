import os
import argparse
import subprocess
from datetime import datetime
import sys
from tqdm import tqdm  # Import the tqdm library

def getPaths(args, startpath: str, depth: int = 0):
    startpath = os.path.abspath(startpath)
    paths = []
    
    # Check if recursion limit is reached
    if args.recrusion_limit and depth >= args.recrusion_limit:
        return paths
    
    try:
        items = os.listdir(startpath)
    except PermissionError:
        return paths

    for item in items:
        path = os.path.join(startpath, item)

        if os.path.isdir(path):
            
            if os.path.exists(os.path.join(path, ".git")):
                paths.append(path)  
            else:
                paths.extend(getPaths(args, path, depth + 1))
                
    return paths

def pull(paths):
    success_count = 0
    failure_count = 0
    failed = []

    start_time = datetime.now()

    # Using tqdm to display a progress bar
    for path in tqdm(paths, desc="Pulling repositories", unit="repo"):
        try:
            result = subprocess.run(["git", "pull"], cwd=path, capture_output=True, text=True)
            folder_name = os.path.basename(path)

            if result.returncode == 0:
                success_count += 1
            else:
                failure_count += 1
                failed.append([folder_name, result.stderr.strip()])
        except Exception as e:
            failure_count += 1
            folder_name = os.path.basename(path)
            failed.append([folder_name, str(e).strip()])

    end_time = datetime.now()
    elapsed_time = end_time - start_time

    # Summary Output
    print("\n========== Pull Summary ==========")
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time:   {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration:   {elapsed_time}")
    print(f"Total Repositories: {len(paths)}")
    print(f"Successful Pulls:   {success_count}")
    print(f"Failed Pulls:       {failure_count}")

    if failed:
        print("\n--- Failed Repositories ---")
        for folder_name, error in failed:
            print(f"- {folder_name}: {error}")
    
    print("========== End of Process ==========")




def run(command_args):
    parser = argparse.ArgumentParser(description='Git pull operation on multiple repositories.')
    parser.add_argument('-p', "--path", type=str, default='.', help='The root directory to start the operation from (default: current directory)')
    parser.add_argument('-r', '--recrusion-limit', type=int, default=None, help='The maximum depth to search for repositories')
    
    args = parser.parse_args(command_args)
    paths = getPaths(args, args.path)
    pull(paths)