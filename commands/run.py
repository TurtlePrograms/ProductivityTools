import argparse
import os
import json
import subprocess
from typing import Tuple, List

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
class Profile:
    profile= ""
    def __init__(self,profile):
        self.profile = profile

class Template:
    template = ""
    name = ""
    def __init__(self,name,template):
        self.template = template
        self.name = name

class Data:
    failed = False
    profile:Profile = None
    templates = []
    
    def __init__(self,profile:Profile = None,templates:List[Template] = []):
        if (profile == None or templates == []):
            self.failed = True
            return
        
        self.profile = profile
        self.templates = templates

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
        self.TerminalTabs = []
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


def getCache() -> Tuple[bool, str]:
    try:
        with open(f"../pt-cache/profiles.json", "r") as file:
            return (True,json.load(file))
    except FileNotFoundError:
        default = {'profiles': {'default': [{'type': 'browser', 'browser': 'msedge', 'tabs': ['https://www.google.com/']}, {'type': 'cmd', 'windows': [{'name': 'Productivity Tool', 'path': 'setPathHere', 'commands': ['code .']}],'path':'setPathHere'}],"example": {"type": "alias","profile": "default"}}}

        default['profiles']['default'][1]['path'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default['profiles']['default'][1]['windows'][0]['path']= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        saveCache(default)
        return (False,f"a default profile has been created at {script_dir}\\pt-cache\\profiles.json")
        
def saveCache(cache:str):
    if not os.path.exists(f"../pt-cache"):
        os.makedirs(f"../pt-cache")
    with open(f"../pt-cache/profiles.json", "w") as file:
        json.dump(cache, file)

def runCommand(command:str):  
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

def loadProfile(profileName:str)->Data:
    success, profiles = getCache()
    if (success):
        try:
            profile =  Profile(profiles["profiles"][profileName])
            templates = profiles["templates"]
            templateList = []
            for template in templates:
                templateList.append(Template(template,profiles["templates"][template]))
            return Data(profile,templateList)
        except KeyError:
            return Data()
    else:
        return Data()




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

def runAlias(task):
    runProfile(task["profile"])

def runTemplate(task, data:Data,id):
    templateToUse = None
    
    for template in data.templates:
        if template.name == task['name']:
            templateToUse = template
            break
            
    if templateToUse is None:
        print("failed to load template")
        return
    
    commands = templateToUse.template
    
    parameters = task['parameters']
    
    filled_commands = fill_parameters(commands, parameters)
    print(data.profile.profile[id])
    data.profile.profile[id] = filled_commands
    print(data.profile.profile[id])
    print()
    # runTasks(Profile([filled_commands]),data)

def fill_parameters(commands, parameters):
    if isinstance(commands, dict):
        for key, value in commands.items():
            if isinstance(value, str):
                for param_key, param_value in parameters.items():
                    value = value.replace(f'${param_key}', param_value)
                commands[key] = value
            elif isinstance(value, list):
                for index in range(len(value)):
                    if isinstance(value[index], str):
                        for param_key, param_value in parameters.items():
                            value[index] = value[index].replace(f'${{{param_key}}}', param_value)
                    elif isinstance(value[index], dict):
                        fill_parameters(value[index], parameters)
    elif isinstance(commands, list):
        for item in commands:
            fill_parameters(item, parameters)

    return commands



def runProfile(profileName):
    data = loadProfile(profileName)
    if data.failed == True:
        print("Failed to load profile")
        return
    runTasks(data.profile,data)
    
def runTasks(profile:Profile,data:Data):
    for id, task in enumerate(profile.profile):
        if (task["type"] == "template"):
            runTemplate(task,data,id)
    for id, task in enumerate(profile.profile):
        match task["type"]:
            case "cmd":
                runCMD(task)
            case "browser":
                runBrowser(task) 
            case "alias":
                runAlias(task)

def getTypeInfo(step):
    Steptype = step["type"]
    if (Steptype == "alias"):
        Steptype += "->"
        Steptype += step["profile"]
    return Steptype

def run(args):
    parser = argparse.ArgumentParser(
        description="Run Command, runs a set profile. a profile contains one or more programs to start"
    )
    parser.add_argument("profile", help="Show detailed help", type=str, nargs='?', default="default")
    parser.add_argument("-l", "--list", help="List all profiles", action="store_true")
    parsed_args = parser.parse_args(args)
    
    if parsed_args.list:
        success, profiles = getCache()
        if (success):
            print("Available profiles:")
            for profile in profiles["profiles"]:
                types = []
                if (type(profiles["profiles"][profile]) == type({"test":"test"})):
                    types.append(getTypeInfo(profiles["profiles"][profile]))
                elif (type(profiles["profiles"][profile]) == type([])):
                    for step in profiles["profiles"][profile]:
                        types.append(getTypeInfo(step))
                output = f"  {profile} - "
                output += ":".join(types)
                print(output)
            return
        else:
            print(profiles)
    runProfile(parsed_args.profile)

run(["my-project-setup"])