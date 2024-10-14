import os
import argparse
import subprocess
import json
import time
import sys
import math

# found = 
# {
#   "filename": [
#       [
#           "foundLine"
#           lineNR,
#           columnNR
#       ],
#       [
#           "foundLine",
#           lineNR,
#           columnNR
#       ]
#   ],
#   "filename": [
#       [
#           "foundLine"
#           lineNR,
#           columnNR
#       ]
#   ]
# }

def searchFile(file, keyword, isExact, found = {}):
    try:
        with open(file, "r") as f:
            for i, line in enumerate(f.readlines()):
                if isExact:
                    if keyword in line:
                        if file not in found:
                            found[file] = []
                        found[file].append([line, i, line.index(keyword)])
                else:
                    if keyword.lower() in line.lower():
                        if file not in found:
                            found[file] = []
                        found[file].append([line, i, line.lower().index(keyword.lower())])
    except UnicodeDecodeError:
        pass
    except OSError:
        pass
    except PermissionError:
        pass
    return found

def searchFolder(path, keyword, recursive, isExact, depth, found = {}):
    if os.path.isfile(path):
        return searchFile(path, keyword, isExact)
    if os.path.isdir(path) and recursive and (depth > 0 or depth <= -20):
        try:
            for file in os.listdir(path):
                found = searchFolder(os.path.join(path, file), keyword, recursive, isExact, depth - 1, found)
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
    return found

def printResults(results: list):
    for file, lines in results.items():
        print(f"File: {file}")
        for line in lines:
            print(f"  Line {line[1]}: {line[0].strip()}")
        print()

def run(raw_args):
    parser = argparse.ArgumentParser(
        description="search for keywords"
    )
    parser.add_argument("-p", "--path", help="path to search", default="./", type=str)
    parser.add_argument("-r", "--recursive", action="store_true", help="search recursively")
    parser.add_argument("-e", "--exact", action="store_true", help="search for exact keyword")
    parser.add_argument("-d", "--recursion-depth", help="recursion depth", default= -20, type=int)
    parser.add_argument("keyword", nargs="?", help="keyword to search for")
    args = parser.parse_args(raw_args)

    sTime = time.time()
    result = searchFolder(args.path, args.keyword, args.recursive, args.exact, args.recursion_depth)
    eTime = time.time()
    printResults(result)
    dt = eTime - sTime # dt = delta time in sec
    print(f"time taken: {math.floor(dt/60)}:{math.floor(dt%60)}") # minutes:seconds:miliseconds