from enum import Enum
from colorama import Fore, Style, init


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