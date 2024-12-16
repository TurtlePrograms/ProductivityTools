from colorama import Fore, init

class UserInput:
    init(autoreset=True)
    @staticmethod
    def confirm(message: str, confirm_message:str="y",decline_message:str="n")->bool:
        confirmation = input(Fore.YELLOW + f"{message} ({confirm_message}/{decline_message}): ").strip().lower()
        return (confirmation == confirm_message)