import argparse
from tools.core import ToolRegistry, Logger, LogLevel,Cache
import webbrowser
import os

class task():
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

class Browser():
    def __init__(self):
        self.tabs = []
    
    def addTab(self, url):
        self.tabs.append(url)

    def open(self):
        if len(self.tabs) == 0:
            Logger.log("No tabs to open", LogLevel.CRITICAL)
        for tab in self.tabs:
            if not webbrowser.open_new_tab(tab):
                Logger.log(f"Failed to open tab '{tab}'", LogLevel.CRITICAL)


BROWSER = None

def parseTask(content):
    tasks = []
    lines = content.split("\n")
    current_task = None
    for line in lines:
        if line.startswith("task"):
            if current_task is not None:
                Logger.log("A task was not closed", LogLevel.WARNING)
                return None
            current_task = task(line.split(" ")[1], [])
        elif line.startswith("end"):
            if current_task is None:
                Logger.log("An end was found without a task", LogLevel.WARNING)
                return None
            tasks.append(current_task)
            current_task = None
        elif current_task is not None:
            current_task.steps.append(line)
    if current_task is not None:
        Logger.log("Unexpected end of file", LogLevel.WARNING)
    return tasks

def runBrowserCommand(command):
    global BROWSER
    keyword = command.split(" ")[0]
    if keyword == "new":
        if BROWSER is not None:
            Logger.log("Browser already open", LogLevel.CRITICAL)
            return
        BROWSER = Browser()
    elif keyword == "close":
        if BROWSER is None:
            Logger.log("Browser not open", LogLevel.CRITICAL)
            return
        BROWSER = None
    elif keyword == "open":
        if BROWSER is None:
            Logger.log("Browser not open", LogLevel.CRITICAL)
            return
        BROWSER.open()
    else:
        if BROWSER is None:
            Logger.log("Browser not open", LogLevel.CRITICAL)
            return
        BROWSER.addTab(url=command)

def runCMDCommand(command):
    name, *args = command.split(" ")
    os.system(f'start cmd /k "title {name} && {" ".join(args)}"')

def runTask(taskName,Tasks):
    for task in Tasks:
        if task.name == taskName:
            for step in task.steps:
                if step.startswith("end"):
                    return
                if step.startswith("run "):
                    runTask(step.split(" ")[1],Tasks)
                elif step.startswith("echo "):
                    Logger.log(step.split(" ",1)[1],LogLevel.INFO)
                elif step.startswith("browser"):
                    runBrowserCommand(step[8:])
                elif step.startswith("cmd"):
                    runCMDCommand(step[4:])
                else:
                    Logger.log(f"Unknown command '{step}'",LogLevel.CRITICAL)
            return
    Logger.log(f"Task '{taskName}' not found", LogLevel.CRITICAL)

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("run", "base")
    )
    parser.add_argument(
        "task",
        help="The task to run",
        type=str
    )
    parser.add_argument(
        "--file",
        help="The file to find the task in (default is {{cache}}/run.txt)",
        default=None,
        type=str
    )
    parsed_args = parser.parse_args(args)

    content = None
    if parsed_args.file is not None:
        with open(parsed_args.file, "r") as file:
            content = file.read()
    else:
        content = Cache.getCache("tasks")
    
    if content is None:
        Logger.log("No tasks found", LogLevel.CRITICAL)
        return
    
    tasks = parseTask(content)
    if tasks is None:
        Logger.log("Failed to parse tasks", LogLevel.CRITICAL)
        return
    
    runTask(parsed_args.task,tasks)

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
