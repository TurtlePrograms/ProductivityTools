import os
import argparse
import subprocess
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def getCache():
    try:
        with open(f"../pt-cache/helpcache.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def saveCache(cache):
    if not os.path.exists(f"../pt-cache"):
        os.makedirs(f"../pt-cache")
    with open(f"../pt-cache/helpcache.json", "w") as file:
        json.dump(cache, file)

def listBatFiles():
    bat_files = []
    for file in os.listdir("../"):
        if file.endswith(".bat"):
            bat_files.append(file)
    return bat_files

def getCommandHelp(batFile):
    try:
        result = subprocess.run([f"..\\{batFile}", "-h"], capture_output=True, text=True, check=True)
        output = result.stdout if result.stdout else "no help available"
    except subprocess.CalledProcessError:
        output = "no help available"
    return output

def getHelpFromBatList(batFiles, useCache=True):
    cache = getCache()
    if cache and useCache:
        return cache
    
    helpList = [] # [[command, help], [command, help], ...]
    for file in batFiles:
        helpList.append([file[:-4], getCommandHelp(file)])
    saveCache(helpList)
    return helpList

def getCommandDescriptions(batFiles, useCache=True):
    helpList = getHelpFromBatList(batFiles, useCache)

    for i in range(len(helpList)):
        helpLines = helpList[i][1].split('\n')

        descriptionLines = []

        foundStart = False
        for line in helpLines:
            if line == "":
                if foundStart:
                    break
                foundStart = True
            if foundStart:
                descriptionLines.append(line)
        
        helpList[i][1] = " ".join(descriptionLines)

    return helpList

def addIndentation(text:str, indentation:int):
    return "\n".join([f"{' '*indentation}{line}" for line in text.split("\n")])

def run(args):
    parser = argparse.ArgumentParser(
        description="Help command, lists all available commands and their descriptions",
    )
    parser.add_argument("-d", "--detailed", action="store_true", help="Show detailed help")
    parser.add_argument("--no-cache", action="store_true", help="Do not use cache / udpate cache")
    parser.add_argument("command", nargs="?", help="Command to get help for")

    parsed_args = parser.parse_args(args)

    try:
        if parsed_args.command:
            if os.path.exists(f"../{parsed_args.command}.bat"):
                print(getCommandHelp(f"{parsed_args.command}.bat"))
                return
            else:
                print(f"Command '{parsed_args.command}' does not exist")
                return
        if parsed_args.detailed:
            print("Detailed help:")
            for help in getHelpFromBatList(listBatFiles() if not parsed_args.command else [f"{parsed_args.command}.bat"], not parsed_args.no_cache):
                print(f"{help[0]}\n{addIndentation(help[1], 2)}")
        else:
            print("Help:")
            barPos = 15
            for help in getCommandDescriptions(listBatFiles() if not parsed_args.command else [f"{parsed_args.command}.bat"], not parsed_args.no_cache):
                print(f"{help[0]}{' ' * max(barPos - len(help[0]), 1)}|{help[1]}")
    except Exception as e:
        print(f"An error occurred: {e}")
        

    