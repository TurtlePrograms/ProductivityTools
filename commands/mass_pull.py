import os
import argparse
import subprocess
from datetime import datetime

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

def pull(paths, summary_only=False):
    success_count = 0
    failure_count = 0
    
    if not summary_only:
        print("========== Git Pull Process Started ==========")
    
    for path in paths:
        if not summary_only:
            print(f"\n--- Pulling Repository at: {path} ---")
            print("Start Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        try:
            result = subprocess.run(["git", "pull"], cwd=path, capture_output=True, text=True)
            
            if result.returncode == 0:
                success_count += 1
                if not summary_only:
                    print("\n[Success] Pull completed successfully.")
                    print("Output:\n" + "-"*40)
                    print(result.stdout.strip())
                    print("-"*40 + "\n")
            else:
                failure_count += 1
                if not summary_only:
                    print("\n[Error] Pull failed.")
                    print("Error Details:\n" + "-"*40)
                    print(result.stderr.strip())
                    print("-"*40 + "\n")
                
        except Exception as e:
            failure_count += 1
            if not summary_only:
                print("\n[Exception] Failed to pull in:", path)
                print("Exception Details:\n" + "-"*40)
                print(str(e))
                print("-"*40 + "\n")
        
        if not summary_only:
            print("End Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Summary
    print("\n========== Summary ==========")
    print(f"Total Repositories Pulled: {len(paths)}")
    print(f"Successful Pulls: {success_count}")
    print(f"Failed Pulls: {failure_count}")
    print("========== End of Process ==========")

def run(command_args):
    parser = argparse.ArgumentParser(description='Git pull operation on multiple repositories.')
    parser.add_argument('-p', "--path", type=str, default='.', help='The root directory to start the operation from (default: current directory)')
    parser.add_argument('-r', '--recrusion-limit', type=int, default=None, help='The maximum depth to search for repositories')
    parser.add_argument('-s', '--summary-only', action='store_true', help='If set, only prints the summary of the pull operations')
    
    args = parser.parse_args(command_args)
    paths = getPaths(args, args.path)
    pull(paths, summary_only=args.summary_only)