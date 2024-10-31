import argparse
import os
import json
import subprocess


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def getCache(depth = 0):
    try:
        with open(f"../pt-cache/profiles.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        if depth == 0:
            
            default = {'profiles': {'pt': [{'type': 'browser', 'browser': 'msedge', 'tabs': ['https://www.google.com/']}, {'type': 'cmd', 'windows': [{'name': 'Productivity Tool', 'path': 'setPathHere', 'commands': ['code .']}],'path':'setPathHere'}]}}

            default['profiles']['pt'][1]['path'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            default['profiles']['pt'][1]['windows'][0]['path']= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            saveCache(default)
            return getCache(1)
        else:
            print("make a profiles file")

def saveCache(cache):
    if not os.path.exists(f"../pt-cache"):
        os.makedirs(f"../pt-cache")
    with open(f"../pt-cache/profiles.json", "w") as file:
        json.dump(cache, file)

def runCommand(command):  
    # Run the command asynchronously
    try:
        # Use `shell=True` to execute it as a command line string on Windows
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Collect standard output and error
        stdout, stderr = process.communicate()
        
        # Check for errors in stderr
        if stderr:
            print(f"Error running command: {stderr.decode()}")
        else:
            print("command ran successfully.")
    except Exception as e:
        print(f"An exception occurred: {e}")

def loadProfile(profileName:str):
    profiles = getCache()
    try:
        return Profile(True,profiles["profiles"][profileName])
    except KeyError:
        return Profile(False,"profile does not exist")

class Profile:
    loadedCorrectly = False
    profile= ""
    def __init__(self,LoadedCorrectly,profile):
        self.LoadedCorrectly =LoadedCorrectly
        self.profile = profile

class BrowserTask:
    BroswerName = "msedge"
    Tabs = []
    def __init__(self,task):
        try:
            self.BrowserName = task["browser"]; 
        except:
            print("could not load broswer name correctly, make sure to include a broswer name\n defaulting to msedge")
        try:
            for tab in task["tabs"]:
                tab = tab.replace("%20"," ")
                self.Tabs.append(tab)
        except:
            print("could not load tab list correctly, make sure to give a list of tabs\n defaulting to opening no tabs")        

class CMDTask:
    TerminalTabs = []
    def __init__(self,task):
        try:
            for window in task["windows"]:
                newtab = CMDTab(window["name"],window["path"],window["commands"])
                self.TerminalTabs.append(newtab)
        except:
            self.TerminalTabs.append(CMDTab("Default","C:\\",["echo Default tab in case no tabs were given/loaded"]))
            print("failed to load tabs")

class CMDTab:
    Name = ""
    Path = ""
    commands = []
    def __init__(self,name,path,commands):
        self.Name = name
        self.Path = path
        self.commands = commands


def runCMD(task):
    cmdTask = CMDTask(task)
    command = "wt"
    for tab in cmdTask.TerminalTabs:
        command += f" nt -p \"Command Prompt\" --title \"{tab.Name}\" -d \"{tab.Path}\" cmd /k \""
        for com in tab.commands:
            command += f"{com} && "
        command = command[:-4]
        command += "\";"
    command = command[:-1]
    runCommand(command)

def runBrowser(task):
    command = ["start", task["browser"]]
    browserTask = BrowserTask(task)
    for tab in browserTask.Tabs:
        command.append(tab)
    runCommand(command)


def run(args):
    parser = argparse.ArgumentParser(
        description="Run Command, runs a set profile. a profile contains one or more programs to start"
    )
    parser.add_argument("-p", "--profile",required=True, help="Show detailed help")
    parsed_args = parser.parse_args(args)
    profile = loadProfile(parsed_args.profile)
    if profile.LoadedCorrectly == False:
        print("Failed to load profile")
        return profile.profile
    for task in profile.profile:
        match task["type"]:
            case "cmd":
                runCMD(task)
            case "browser":
                runBrowser(task)
    