import argparse
import os
import json
from enum import Enum
from colorama import Fore, Style, init
import subprocess
init(autoreset=True)

class Path:
    TOOLS_DIR = os.path.dirname(os.path.realpath(__file__))
    ROOT_DIR = os.path.dirname(TOOLS_DIR)
    CACHE_DIR = os.path.join(ROOT_DIR, "cache")
    CONFIG_DIR = os.path.join(ROOT_DIR, "config")

    def get_dir():
        return os.getcwd()

class Cache:

    AVAILABLE_CACHES = {
        "tool_registry": "tool_registry.json",
        "config": "config.json",
    }

    def getCache(cache_name:str)->dict:
        try:
            if not os.path.exists(Path.CACHE_DIR):
                os.makedirs(Path.CACHE_DIR)
        
            path = os.path.join(Path.CACHE_DIR, Cache.AVAILABLE_CACHES[cache_name])
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except KeyError:
            raise ValueError(f"Cache '{cache_name}' not found")
        except json.JSONDecodeError:
            return {}
        except PermissionError:
            return {}
        except Exception as e:
            raise e
    
    def saveCache(cache_name:str, cache:json)->bool:
        try:
            if not os.path.exists(Path.CACHE_DIR):
                os.makedirs(Path.CACHE_DIR)
        
            path = os.path.join(Path.CACHE_DIR, Cache.AVAILABLE_CACHES[cache_name])
            with open(path, "w") as file:
                json.dump(cache, file)
            return True
        except FileNotFoundError:
            return False
        except KeyError:
            raise ValueError(f"Cache '{cache_name}' not found")
        except json.JSONDecodeError:
            return False
        except PermissionError:
            return False
        except Exception as e:
            raise e

class ToolRegistry:
    
    @staticmethod
    def getScript(command:str)->str:
        try:
            tool_registry = Cache.getCache("tool_registry")
            return tool_registry[command]["script"]
        except KeyError:
            for key in tool_registry.keys():
                aliases = tool_registry[key].get("aliases", [])
                if command in aliases:
                    return tool_registry[key]["script"]
            return None
        except Exception as e:
            raise e
    
    @staticmethod
    def getToolInfo(command:str)->dict:
        try:
            tool_registry = Cache.getCache("tool_registry")
            return tool_registry[command]
        except KeyError:
            for key in tool_registry.keys():
                aliases = tool_registry[key].get("aliases", [])
                if command in aliases:
                    return tool_registry[key]
            return None
    
    @staticmethod
    def getTools()->dict:
        try:
            tool_registry = Cache.getCache("tool_registry")
            return tool_registry
        except Exception as e:
            raise e
    
    @staticmethod
    def getAllCommandsAndAliases()->list:
        try:
            tool_registry = Cache.getCache("tool_registry")
            commands = list(tool_registry.keys())
            for key in tool_registry.keys():
                aliases = tool_registry[key].get("aliases", [])
                commands += aliases
            return commands
        except Exception as e:
            raise e
    
    @staticmethod
    def doesToolExist(command:str)->bool:
        try:
            return command in ToolRegistry.getAllCommandsAndAliases()
        except Exception as e:
            raise e
    
    @staticmethod
    def setToolValue(tool_name:str, key:str, value:str)->bool:
        try:
            tool_registry = Cache.getCache("tool_registry")
            tool_registry[tool_name][key] = value
            Cache.saveCache("tool_registry", tool_registry)
        except Exception as e:
            raise e

    @staticmethod
    def registerTool(name:str, description:str, aliases:list=[])->bool:
        try:
            tool_registry = Cache.getCache("tool_registry")
            if ToolRegistry.doesToolExist(name):
                return False
            tool_registry[name] = {
                "description": description,
                "script": name,
                "aliases": [],
                "isExperimental": True,
            }
            for alias in aliases:
                if not ToolRegistry.doesToolExist(alias):
                    tool_registry[name]["aliases"].append(alias)

            Cache.saveCache("tool_registry", tool_registry)

            Documentation.createDocumentation(name, description)

            return True
        except Exception as e:
            raise e
        
    @staticmethod
    def getToolDescription(command:str)->str:
        try:
            info = ToolRegistry.getToolInfo(command)
            return info["description"]
        except Exception as e:
            raise e

class Documentation:
    @staticmethod
    def createDocumentation(tool_name:str, description:str):
        try:
            doc_dir = os.path.join(Path.ROOT_DIR, "Docs")
            if not os.path.exists(doc_dir):
                os.makedirs(doc_dir)
            
            doc_path = os.path.join(doc_dir,"tools", f"{tool_name}.md")
            with open(doc_path, "w") as file:
                file.write(f"# {tool_name}\n\n")
                file.write(f"# Description\n\n")
                file.write(f"{description}\n\n")
                file.write("## Usage\n")
        except Exception as e:
            raise e
        finally:
            relative_doc_path = os.path.relpath(doc_path, Path.ROOT_DIR)
            ToolRegistry.setToolValue(tool_name, "documentation", relative_doc_path)

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5
    NONE = 0  # Special level for messages not tied to verbosity

class Logger:
    init(autoreset=True)
    verbosity_level = LogLevel.DEBUG

    @staticmethod
    def set_verbosity(level: LogLevel):
        if level == LogLevel.NONE:
            Logger.log("Setting verbosity to NONE will enable all logging")
        Logger.verbosity_level = level

    @staticmethod
    def log(message: str = "", level: LogLevel = LogLevel.NONE):
        if level == LogLevel.NONE:
            Logger._logPrint(message)
            return

        if level.value >= Logger.verbosity_level.value:  # Compare the 'value' of the Enum
            # Dispatch to the correct log method based on level
            if level == LogLevel.DEBUG:
                Logger._logDebug(message)
            elif level == LogLevel.INFO:
                Logger._logInfo(message)
            elif level == LogLevel.WARNING:
                Logger._logWarning(message)
            elif level == LogLevel.ERROR:
                Logger._logError(message)
            elif level == LogLevel.CRITICAL:
                Logger._logCritical(message)

    @staticmethod
    def _logPrint(message: str = ""):
        print(message)

    @staticmethod
    def _logDebug(message: str = ""):
        print(f"{Fore.WHITE}{Style.BRIGHT}[{LogLevel.DEBUG.name}] {message}")

    @staticmethod
    def _logInfo(message: str = ""):
        print(f"{Fore.CYAN}{Style.BRIGHT}[{LogLevel.INFO.name}] {message}")

    @staticmethod
    def _logWarning(message: str = ""):
        print(f"{Fore.YELLOW}{Style.BRIGHT}[{LogLevel.WARNING.name}] {message}")

    @staticmethod
    def _logError(message: str = ""):
        print(f"{Fore.RED}{Style.BRIGHT}[{LogLevel.ERROR.name}] {message}")

    @staticmethod
    def _logCritical(message: str = ""):
        print(f"{Fore.MAGENTA}{Style.BRIGHT}[{LogLevel.CRITICAL.name}] {message}")

class UserInput:
    init(autoreset=True)
    @staticmethod
    def confirm(message: str, confirm_message:str="y",decline_message:str="n")->bool:
        confirmation = input(Fore.YELLOW + f"{message} ({confirm_message}/{decline_message}): ").strip().lower()
        return (confirmation == confirm_message)
    
class GitClient:
    init(autoreset=True)
    @staticmethod
    def Add(path = ".")->int:
        try:
            result = subprocess.run(
                ["git","add",path], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git add:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode

    def Status()->int:
        try:
            result = subprocess.run(
                ["git","status","-s"], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git status:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def Commit(message:str)->int:
        try:
            result = subprocess.run(
                ["git","commit","-m",message], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git commit:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode

    def Push()->int:
        try:
            result = subprocess.run(
                ["git","push"], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git push:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def getLatestTag()->str:
        try:
            result = subprocess.run(
                ['git', 'tag', '--list', '--sort=-creatordate'], capture_output=True, text=True, check=True
            )
            return result.stdout.splitlines()[0]
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git describe --tags:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
        
    def Tag(tag:str)->int:
        try:
            result = subprocess.run(
                ["git","tag",tag], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git tag:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def PushTag(tag:str)->int:
        try:
            result = subprocess.run(
                ["git","push","origin",tag], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git push origin tag:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def getAllCommitMessageSinceCommit(commit:str)->str:
        try:
            result = subprocess.run(
                ["git","log","--pretty=format:%s",commit], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git log --pretty=format:%s -1 {commit}:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""

    def getCommitIdFromTag(tag:str)->str:
        try:
            result = subprocess.run(
                ['git', 'log', tag, '-n', '1', '--pretty=format:%H'], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git log --pretty=format:%s -1 {tag}:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
    
    def getCommitsSinceID(commitID:str)->list:
        try:
            result = subprocess.run(
                ['git', 'log', '--pretty=format:%s', f'{commitID}..HEAD'], capture_output=True, text=True, check=True
            )
            return result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git log --pretty=format:%s {commitID}..HEAD:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
        
    def CheckoutBranch(branch:str):
        try:
            result = subprocess.run(
                ["git","checkout",branch], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git checkout:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode