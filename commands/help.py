import os
import argparse
import subprocess

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

def getHelpFromBatList(batFiles):
    helpList = [] # [[command, help], [command, help], ...]
    for file in batFiles:
        helpList.append([file[:-4], getCommandHelp(file)])
    return helpList

def getCommandDescriptions(batFiles):
    helpList = getHelpFromBatList(batFiles)

    for i in range(len(helpList)):
        help = helpList[i]
        helpLines = help[1].split('\n')

        descriptionStart = 0
        for j in range(len(helpLines)):
            if helpLines[j] == "":
                descriptionStart = j + 1
                break
        descriptionEnd = 0
        for j in range(descriptionStart, len(helpLines)):
            if helpLines[j] == "":
                descriptionEnd = j
                break
        
        helpList[i][1] = " ".join(helpLines[descriptionStart:descriptionEnd])

    return helpList

def addIndentation(text:str, indentation:int):
    return "\n".join([f"{' '*indentation}{line}" for line in text.split("\n")])

def run(args):
    parser = argparse.ArgumentParser(
        description="Help command"
    )
    parser.add_argument("-d", "--detailed", action="store_true", help="Show detailed help")
    parser.add_argument("command", nargs="?", help="Command to get help for")

    parsed_args = parser.parse_args(args)

    # Change the current working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    try:
        if parsed_args.detailed:
            print("Detailed help:")
            for help in getHelpFromBatList(listBatFiles() if not parsed_args.command else [f"{parsed_args.command}.bat"]):
                print(f"{help[0]}\n{addIndentation(help[1], 2)}")
        else:
            print("Help:")
            barPos = 15
            for help in getCommandDescriptions(listBatFiles() if not parsed_args.command else [f"{parsed_args.command}.bat"]):
                print(f"{help[0]}{' ' * max(barPos - len(help[0]), 1)}|{help[1]}")
    except Exception as e:
        print(f"An error occurred: {e}")
        

    