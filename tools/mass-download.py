import argparse
from tools.core import ToolRegistry, Logger, LogLevel
import os
import queue
import subprocess
import threading
import time

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("mass-download", "base")
    )
    parser.add_argument("URL", type=str, default="", nargs="*", help="The URL(s) to download")
    parser.add_argument("-i", "--input", type=str, default="", help="The input file containing the list of files to download")
    parser.add_argument("-o", "--output", type=str, default=".", help="The output folder to download the files to")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads to use for downloading (default: 4)")

    parsed_args = parser.parse_args(args)

    if not parsed_args.URL and not parsed_args.input:
        Logger.log("No input provided", LogLevel.CRITICAL)
    
    if parsed_args.URL:
        urls = parsed_args.URL
    else:
        urls = parse_inputFile(parsed_args.input)

    start = time.time()
    download_files(urls, parsed_args.output, parsed_args.threads)
    end = time.time()

    Logger.log(f"Finished downloading files in {round(end-start, 2)} seconds", LogLevel.INFO)

    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)

def parse_inputFile(path:str) -> list[str]:
    if not os.path.exists(path):
        Logger.log(f"File {path} does not exist", LogLevel.CRITICAL)
    with open(path, 'r') as file:
        lines = [i.strip() for i in file.readlines()]
    return lines

def download_files(urls:list[str], output:str, threads:int):
    tasks = queue.Queue()
    for url in urls:
        tasks.put(url)

    thread_list = []

    def worker(threadNum:int):
        Logger.log(f"Thread {threadNum} started", LogLevel.DEBUG)
        while not tasks.empty():
            url = tasks.get()
            if url is None:
                # Logger.log(f"Thread {threadNum} finished (none)", LogLevel.DEBUG)
                break
            output_path = os.path.join(output, os.path.basename(url))
            # Logger.log(f"Thread {threadNum} downloading {url} to {output_path}", LogLevel.DEBUG)
            download_file(url, output_path)
        Logger.log(f"Thread {threadNum} finished", LogLevel.DEBUG)
    
    for thread in range(threads):
        thread_list.append(threading.Thread(target=worker, args=(thread,)))
        thread_list[thread].start()
    
    for thread in thread_list:
        thread.join()
    
    return


def download_file(url:str, output:str):
    try:
        subprocess.run(["curl", url, "-o", output, "--connect-timeout", "30"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        Logger.log(f"Error downloading {url}: {e}", LogLevel.ERROR)
