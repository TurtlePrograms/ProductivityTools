import os
import argparse
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import Fore, Style

def getPathsHelper(path, paths):
    """Helper function to find all repositories in a directory."""
    try:
        items = os.listdir(path)
    except PermissionError:
        return

    for item in items:
        subpath = os.path.join(path, item)
        if os.path.isdir(subpath):
            if os.path.exists(os.path.join(subpath, ".git")):
                paths.append(subpath)
            else:
                getPathsHelper(subpath, paths)

def getPaths(args, startpath: str, depth: int = 0,max_workers:int=4):
    """Concurrent version to find all repository paths."""
    startpath = os.path.abspath(startpath)
    paths = []

    # Worker pool to perform path discovery concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Queue up path discovery tasks
        futures = [executor.submit(getPathsHelper, os.path.join(startpath, item), paths) for item in os.listdir(startpath)]
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            future.result()

    return paths

def pull_repository(path):
    """Performs 'git pull' in a single repository."""
    try:
        result = subprocess.run(["git", "pull"], cwd=path, capture_output=True, text=True)
        folder_name = os.path.basename(path)

        if result.returncode == 0:
            return (folder_name, True, "")
        else:
            return (folder_name, False, result.stderr.strip())
    except Exception as e:
        folder_name = os.path.basename(path)
        return (folder_name, False, str(e).strip())

def pull(paths, max_workers=4):
    success_count = 0
    failure_count = 0
    failed = []

    start_time = datetime.now()

    # Using ThreadPoolExecutor for concurrent 'git pull'
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(pull_repository, path): path for path in paths}

        # Progress bar with tqdm
        for future in tqdm(as_completed(future_to_path), total=len(paths), desc="Pulling repositories", unit="repo"):
            folder_name, success, message = future.result()
            if success:
                success_count += 1
            else:
                failure_count += 1
                failed.append([folder_name, message])

    end_time = datetime.now()
    elapsed_time = end_time - start_time

    # Enhanced Summary Output
    print(f"\n{Fore.CYAN}========== Pull Summary =========={Style.RESET_ALL}")
    print(f"{Fore.CYAN}Start Time:  {Style.RESET_ALL}{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.CYAN}End Time:    {Style.RESET_ALL}{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.CYAN}Duration:    {Style.RESET_ALL}{elapsed_time}")
    print(f"{Fore.GREEN}Total Repositories: {Style.RESET_ALL}{len(paths)}")
    print(f"{Fore.GREEN}Successful Pulls:   {Style.RESET_ALL}{success_count}")
    print(f"{Fore.RED}Failed Pulls:       {Style.RESET_ALL}{failure_count}")

    if failed:
        print(f"\n{Fore.RED}--- Failed Repositories ---{Style.RESET_ALL}")
        for folder_name, error in failed:
            print(f"- {Fore.YELLOW}{folder_name}{Style.RESET_ALL}: {error}")
    
    print(f"{Fore.CYAN}========== End of Process =========={Style.RESET_ALL}")

def run(command_args):
    parser = argparse.ArgumentParser(description='Git pull operation on multiple repositories.')
    parser.add_argument('-p', "--path", type=str, default='.', help='The root directory to start the operation from (default: current directory)')
    parser.add_argument('-r', '--recrusion-limit', type=int, default=None, help='The maximum depth to search for repositories')
    parser.add_argument('-w', '--workers', type=int, default=4, help='Number of concurrent workers for pulling repositories (default: 4)')
    
    args = parser.parse_args(command_args)
    paths = getPaths(args, args.path,args.workers)
    pull(paths, max_workers=args.workers)
