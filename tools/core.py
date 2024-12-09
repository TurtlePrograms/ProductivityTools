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

class Confirm:
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
